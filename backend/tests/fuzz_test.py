import requests
import time
import random

# Payloads used for fuzz testing
PAYLOADS = [
    "' OR '1'='1",                 # SQL injection
    "<script>alert(1)</script>",   # XSS
    "../etc/passwd",               # path traversal
    "A" * 2000,                    # buffer / input overflow
    "NULL\x00BYTE"                 # null byte injection
]


def run_fuzz_test(url, headers, progress_callback=None):

    results = {
        "payloads": [],
        "vulnerabilities": []
    }

    try:

        for i, payload in enumerate(PAYLOADS):

            try:

                r = requests.post(
                    url,
                    json={"input": payload},
                    headers=headers,
                    timeout=7
                )

                reflection = payload in r.text

                results["payloads"].append({
                    "payload": payload,
                    "status_code": r.status_code,
                    "reflection": reflection,
                    "response_snippet": r.text[:200]
                })

                # detect reflection vulnerability
                if reflection:
                    results["vulnerabilities"].append(
                        f"Payload reflected in response (possible XSS): {payload}"
                    )

                # detect server crash
                if r.status_code >= 500:
                    results["vulnerabilities"].append(
                        f"Server error triggered by payload: {payload}"
                    )

            except Exception as e:

                results["payloads"].append({
                    "payload": payload,
                    "error": str(e)
                })

            if progress_callback:
                progress_callback(int((i + 1) / len(PAYLOADS) * 90))

            time.sleep(0.6 + random.random() * 0.3)

        results["summary"] = "Fuzz test completed"

        if progress_callback:
            progress_callback(100)

        return results

    except Exception as e:
        return {"error": str(e)}