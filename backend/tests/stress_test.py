import asyncio
import aiohttp
import time


async def _do_requests(url, headers, n):
    timeout = aiohttp.ClientTimeout(total=10)

    async with aiohttp.ClientSession(timeout=timeout, headers=headers) as session:
        tasks = []

        for _ in range(n):
            tasks.append(session.get(url))

        res = await asyncio.gather(*tasks, return_exceptions=True)
        return res


def run_stress_test(url, headers, progress_callback=None):

    results = {"attempts": []}

    try:

        steps = [5, 10, 20]
        total = len(steps)

        for i, c in enumerate(steps):

            start = time.time()

            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

            res = loop.run_until_complete(
                _do_requests(url, headers, c)
            )

            dur = time.time() - start

            errors = sum(
                1 for r in res
                if isinstance(r, Exception) or
                (hasattr(r, "status") and getattr(r, "status", 0) >= 500)
            )

            results["attempts"].append({
                "concurrency": c,
                "duration": dur,
                "errors": errors
            })

            if progress_callback:
                progress_callback(int((i + 1) / total * 90))

            time.sleep(0.6)

        failures = sum(a.get("errors", 0) for a in results["attempts"])

        results["vulnerabilities"] = (
            ["Resource instability detected under load"] if failures > 0 else []
        )

        results["summary"] = "Stress test completed"

        if progress_callback:
            progress_callback(100)

        return results

    except Exception as e:
        return {"error": str(e)}