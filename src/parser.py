import re

# Regex patterns
REQ_RE = re.compile(
    r'(?P<method>GET|POST)\s+(?P<endpoint>/[a-zA-Z0-9_]+)\s+(?P<status>\d{3})\s+(?P<time>[\d\.]+)(µs|Âµs|us|ms)'
)

USER_RE = re.compile(
    r'\[(?P<user_id>\d{4}[A-Z0-9]+)\]'
)

ALGO_RE = re.compile(
    r'Using (?P<algo>.+?) Strategy'
)

SUMMARY_RE = re.compile(
    r'Found (?P<found>\d+) timetables.*returning (?P<returned>\d+)'
)

def parse_line(line: str) -> dict:
    if m := REQ_RE.search(line):
        return {
            "type": "request",
            "method": m.group("method"),
            "endpoint": m.group("endpoint"),
            "status": int(m.group("status")),
            "time": float(m.group("time")),
            "unit": "µs" if "µs" in line else "ms"
        }

    # User IDs
    if m := USER_RE.search(line):
        return {"type": "user", "user_id": m.group("user_id")}

    # Algorithm usage
    if m := ALGO_RE.search(line):
        return {"type": "algorithm", "algo": m.group("algo")}

    # Timetable summary
    if m := SUMMARY_RE.search(line):
        return {"type": "summary", "found": int(m.group("found")), "returned": int(m.group("returned"))}

    return {"type": "other", "raw": line}

