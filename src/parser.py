import re

# RE Patters
REQ_RE = re.compile(r'(?P<method>GET|POST)\s+(?P<endpoint>/\S*)\s+(?P<status>\d{3})\s+(?P<time>[\d\.]+)(µs|Âµs|us|ms|ns)')

USER_RE = re.compile(r'\[(?P<user_id>\d{4}[A-Z0-9]+)\]')

ALGO_RE = re.compile(r'Using (?P<algo>.+?) Strategy')

SUMMARY_RE = re.compile(r'Found (?P<found>\d+) timetables.*returning (?P<returned>\d+)')

MALFORMED_REQ_RE = re.compile(r'Malformed req: (?P<message>.+)')

CONNECT_RE = re.compile(r'CONNECT\s+(?P<status>\d{3})\s+(?P<time>[\d\.]+)(µs|Âµs|us|ms|ns)')

RECAPTCHA_ERROR_RE = re.compile(r'Error verifying reCAPTCHA token: (?P<message>.+)')

RECAPTCHA_FAIL_RE = re.compile(r'reCAPTCHA Failed!\s+score:\s+(?P<score>[\d\.]+),\s+action:\s*(?P<action>\w*)')


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
        return {"type": "summary", "found": int(m.group("found"))}

    # Malformed Requests
    if m := MALFORMED_REQ_RE.search(line):
        return {"type": "malformed", "message": m.group("message")}
    
    #CONNECT calls
    if m := CONNECT_RE.search(line):
        time_val = float(m.group("time"))
        unit = m.group(3)
        if unit in ("µs", "Âµs", "us"): time_val /= 1000
        elif unit == "ns": time_val /= 1000000
        return {"type": "connect", "status": int(m.group("status")), "time_ms": time_val}
    
    #reCAPTCHA error
    if m := RECAPTCHA_ERROR_RE.search(line):
        return {"type": "recaptcha_error", "message": m.group("message")}
    
    #reCAPTCHA fail
    if m := RECAPTCHA_FAIL_RE.search(line):
        return {"type": "recaptcha_fail", "score": float(m.group("score")), "action": m.group("action")}
    return {"type": "other", "raw": line}

