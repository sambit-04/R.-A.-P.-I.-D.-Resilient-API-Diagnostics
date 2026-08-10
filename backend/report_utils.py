MITIGATIONS = {

    "Insecure transport (no HTTPS)": {
        "mitigation": "Use HTTPS with TLS encryption to protect data in transit.",
        "severity": "High",
        "cvss": "7.4"
    },

    "Missing Content-Security-Policy header": {
        "mitigation": "Implement a strict Content-Security-Policy header to reduce risk of XSS.",
        "severity": "Medium",
        "cvss": "5.4"
    },

    "Missing X-Frame-Options header": {
        "mitigation": "Add X-Frame-Options header to prevent clickjacking attacks.",
        "severity": "Medium",
        "cvss": "4.3"
    },

    "Resource instability": {
        "mitigation": "Implement rate limiting and optimize server resource management.",
        "severity": "Medium",
        "cvss": "5.0"
    },

    "Potential BOLA": {
        "mitigation": "Implement object-level authorization checks on the server.",
        "severity": "Critical",
        "cvss": "9.1"
    }
}


def convert_results_to_findings(results):

    findings = []

    vulns = results.get("vulnerabilities", [])

    for v in vulns:

        info = MITIGATIONS.get(v, {
            "mitigation": "Review API security configuration.",
            "severity": "Low",
            "cvss": "3.0"
        })

        findings.append({
            "description": v,
            "mitigation": info["mitigation"],
            "severity": info["severity"],
            "cvss": info["cvss"]
        })

    return findings