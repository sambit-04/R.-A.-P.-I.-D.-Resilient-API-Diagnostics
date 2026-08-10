from flask import Flask, request, jsonify, send_from_directory, send_file
from flask_cors import CORS
from flask_jwt_extended import JWTManager, jwt_required
from auth import auth_bp
from encryption import encrypt_data, decrypt_data
import os, sqlite3, uuid, time, json, threading


from tests.basic_test import run_basic_test
from tests.stress_test import run_stress_test
from tests.fuzz_test import run_fuzz_test
from tests.bola_test import run_bola_test

from report_generator import generate_report
from report_utils import convert_results_to_findings

BASE_DIR = os.path.dirname(__file__)
DB_PATH = os.path.join(BASE_DIR, "history.db")

# ------------------- FLASK APP SETUP -------------------
app = Flask(__name__, static_folder="static", template_folder="templates")
CORS(app)

# ------------------- DATABASE SETUP -------------------
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS tests (
            id TEXT PRIMARY KEY,
            url TEXT,
            type TEXT,
            status TEXT,
            created_at TEXT,
            encrypted_summary TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

def save_test_record(record):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("INSERT INTO tests VALUES (?,?,?,?,?,?)",
                (record["id"], record["url"], record["type"], record["status"],
                 record["created_at"], record["encrypted_summary"]))
    conn.commit()
    conn.close()

def update_test_record_summary(task_id, status, encrypted_summary):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("UPDATE tests SET status=?, encrypted_summary=? WHERE id=?",
                (status, encrypted_summary, task_id))
    conn.commit()
    conn.close()

# ------------------- TASK MANAGEMENT -------------------
TASKS = {}

@app.route("/api/test", methods=["POST"])
# @jwt_required()
def start_test():
    data = request.json or {}

    url = data.get("url")
    test_type = data.get("type", "basic")
    api_key = data.get("apiKey")
    auth_type = data.get("authType", "none")

    headers = {}

    if not url:
        return jsonify({"error": "url required"}), 400

    # attach API key in header
    if api_key and auth_type == "header":
        headers["x-api-key"] = api_key

    # attach API key in query
    if api_key and auth_type == "query":
        separator = "&" if "?" in url else "?"
        url = f"{url}{separator}api_key={api_key}"

    task_id = str(uuid.uuid4())
    now = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())

    TASKS[task_id] = {
        "id": task_id,
        "url": url,
        "type": test_type,
        "status": "running",
        "progress": 0,
        "created_at": now
    }

    save_test_record({
        "id": task_id,
        "url": url,
        "type": test_type,
        "status": "running",
        "created_at": now,
        "encrypted_summary": ""
    })

    def runner():
        try:
            print(f"Starting {test_type.upper()} test on {url}")

            if test_type == "basic":
                res = run_basic_test(
                    url,
                    headers,
                    lambda p: TASKS[task_id].update({"progress": p})
                )

            elif test_type == "stress":
                res = run_stress_test(
                    url,
                    headers,
                    lambda p: TASKS[task_id].update({"progress": p})
                )

            elif test_type == "fuzz":
                res = run_fuzz_test(
                    url,
                    headers,
                    lambda p: TASKS[task_id].update({"progress": p})
                )

            elif test_type == "bola":
                res = run_bola_test(
                    url,
                    headers,
                    lambda p: TASKS[task_id].update({"progress": p})
                )

            else:
                raise Exception("Unknown test type")

            TASKS[task_id]["status"] = "completed"
            TASKS[task_id]["progress"] = 100

            enc = encrypt_data(json.dumps(res))
            TASKS[task_id]["encrypted_summary"] = enc

            update_test_record_summary(task_id, "completed", enc)

            print(f"Test {task_id} completed")

        except Exception as e:
            TASKS[task_id]["status"] = "failed"
            TASKS[task_id]["progress"] = 100

            enc = encrypt_data(json.dumps({"error": str(e)}))
            TASKS[task_id]["encrypted_summary"] = enc

            update_test_record_summary(task_id, "failed", enc)

            print(f"Test {task_id} failed: {str(e)}")

    threading.Thread(target=runner, daemon=True).start()

    return jsonify({"task_id": task_id}), 202


@app.route("/api/status/<task_id>")
# @jwt_required()
def status(task_id):
    t = TASKS.get(task_id)
    if t:
        return jsonify({"id": t["id"], "status": t["status"], "progress": t["progress"]})

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT status FROM tests WHERE id=?", (task_id,))
    row = cur.fetchone()
    conn.close()
    if not row:
        return jsonify({"error": "not found"}), 404
    return jsonify({"id": task_id, "status": row[0], "progress": 100 if row[0] == "completed" else 0})


@app.route("/api/result/<task_id>")
# @jwt_required()
def result(task_id):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT encrypted_summary FROM tests WHERE id=?", (task_id,))
    row = cur.fetchone()
    conn.close()
    if not row:
        return jsonify({"error": "not found"}), 404
    return jsonify(json.loads(decrypt_data(row[0])))

@app.route("/api/report/<task_id>")
def download_report(task_id):

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT url,type,encrypted_summary FROM tests WHERE id=?", (task_id,))
    row = cur.fetchone()
    conn.close()

    if not row:
        return jsonify({"error": "report not found"}), 404

    url = row[0]
    test_type = row[1]

    results = json.loads(decrypt_data(row[2]))

    findings = convert_results_to_findings(results)

    report_path = generate_report(
        task_id,
        url,
        test_type,
        findings
    )

    return send_file(report_path, as_attachment=True)


@app.route("/api/history")
# @jwt_required()
def history():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT id,url,type,status,created_at FROM tests ORDER BY created_at DESC")
    rows = cur.fetchall()
    conn.close()
    return jsonify([{"id": r[0], "url": r[1], "type": r[2], "status": r[3], "created_at": r[4]} for r in rows])


# ------------------- BACKEND TERMINAL UI -------------------
@app.route("/admin")
def admin_ui():
    return send_from_directory("templates", "admin.html")


# ------------------- SERVE FRONTEND -------------------
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_spa(path):
    if path and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    return send_from_directory(app.static_folder, 'index.html')


# ------------------- RUN APP -------------------
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True, use_reloader=False)
