import requests
import re
import time


def extract_object_id(url):
    """
    Detect numeric object ID in the URL.
    Example:
    /user/101
    /orders/5501
    """
    match = re.search(r"/(\d+)(?:/)?$", url)
    if match:
        return int(match.group(1))
    return None


def build_test_urls(url, base_id, attempts=5):
    """
    Generate URLs with modified object IDs
    """
    urls = []
    for i in range(1, attempts + 1):
        new_id = base_id + i
        urls.append(url.replace(f"/{base_id}", f"/{new_id}"))
    return urls


def run_bola_test(url, headers, progress_callback=None):

    results = {
        "attempts": [],
        "vulnerabilities": []
    }

    try:

        base_id = extract_object_id(url)

        if base_id is None:
            return {
                "summary": "No object identifier detected in endpoint",
                "attempts": [],
                "vulnerabilities": []
            }

        test_urls = build_test_urls(url, base_id)

        for i, test_url in enumerate(test_urls):

            try:
                r = requests.get(test_url, headers=headers, timeout=8)

                snippet = r.text[:150]

                results["attempts"].append({
                    "url": test_url,
                    "status_code": r.status_code,
                    "response_snippet": snippet
                })

                # Detect possible BOLA
                if r.status_code == 200:
                    results["vulnerabilities"].append(
                        f"Potential BOLA: object accessible at {test_url}"
                    )

            except Exception as e:

                results["attempts"].append({
                    "url": test_url,
                    "error": str(e)
                })

            if progress_callback:
                progress_callback(int((i + 1) / len(test_urls) * 90))

            time.sleep(0.6)

        results["summary"] = "BOLA test completed"

        if progress_callback:
            progress_callback(100)

        return results

    except Exception as e:
        return {"error": str(e)}