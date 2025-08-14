def get_endpoint_popularity(parsed_logs):
    counts = {}
    for entry in parsed_logs:
        if entry["type"] == "request":
            counts[entry["endpoint"]] = counts.get(entry["endpoint"], 0) + 1
    return counts
