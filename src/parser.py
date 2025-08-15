import re

# RE Patters
REQ_RE = re.compile(
    r'(?P<method>GET|POST)\s+(?P<endpoint>/[a-zA-Z0-9_]+)\s+(?P<status>\d{3})\s+(?P<time>[\d\.]+)(µs|Âµs|us|ms|ns)'
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
        time_val = float(m.group("time"))
        unit = m.group(5)

        # microseconds -> milliseconds
        if unit in ("µs", "Âµs", "us"):
            time_val /= 1000.0  
        if unit=="ns":
            time_val /= 1000000.0
        return {
            "type": "request",
            "method": m.group("method"),
            "endpoint": m.group("endpoint"),
            "status": int(m.group("status")),
            "time_ms": time_val
        }

    # User id
    if m := USER_RE.search(line):
        return {"type": "user", "user_id": m.group("user_id")}

    # Algorithm 
    if m := ALGO_RE.search(line):
        return {"type": "algorithm", "algo": m.group("algo")}

    # Timetable summary
    if m := SUMMARY_RE.search(line):
        return {"type": "summary", "found": int(m.group("found")), "returned": int(m.group("returned"))}

    return {"type": "other", "raw": line}

