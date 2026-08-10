import requests
import time


def run_basic_test(url, headers, progress_callback=None):
    results = {"checks": []}

    try:

        # HTTPS check
        if url.startswith("https://"):
            results["checks"].append({"name": "https", "ok": True})
        else:
            results["checks"].append({"name": "https", "ok": False, "note": "Not HTTPS"})

        if progress_callback:
            progress_callback(20)

        time.sleep(0.8)

        # CORS check
        try:
            r = requests.options(url, headers=headers, timeout=6)
            cors = r.headers.get("access-control-allow-origin", None)
            results["checks"].append({"name": "cors", "value": cors})
        except Exception as e:
            results["checks"].append({"name": "cors", "error": str(e)})

        if progress_callback:
            progress_callback(50)

        time.sleep(0.8)

        # Security headers + status check
        try:
            r = requests.get(url, headers=headers, timeout=8)

            resp_headers = r.headers
            status_code = r.status_code

            sec = {}

            for h in [
                "x-frame-options",
                "content-security-policy",
                "strict-transport-security",
                "x-content-type-options"
            ]:
                sec[h] = resp_headers.get(h, None)

            results["checks"].append({
                "name": "security_headers",
                "value": sec,
                "status_code": status_code
            })

        except Exception as e:
            results["checks"].append({"name": "security_headers", "error": str(e)})

        if progress_callback:
            progress_callback(80)

        time.sleep(0.8)

        # vulnerability analysis
        vulns = []

        for c in results["checks"]:

            if c.get("name") == "https" and c.get("ok") is False:
                vulns.append("Insecure transport (no HTTPS)")

            if c.get("name") == "security_headers":

                hv = c.get("value", {})
                status = c.get("status_code")

                if not hv.get("content-security-policy"):
                    vulns.append("Missing Content-Security-Policy header")

                if status == 500:
                    vulns.append("Server error (500) detected – possible backend vulnerability")

                if status == 401:
                    vulns.append("Unauthorized response (401) – authentication required or misconfigured")

                if status == 403:
                    vulns.append("Forbidden response (403) – possible access control restriction")

        results["vulnerabilities"] = vulns
        results["summary"] = "Completed basic checks"

        if progress_callback:
            progress_callback(100)

        return results

    except Exception as e:
        return {"error": str(e)}