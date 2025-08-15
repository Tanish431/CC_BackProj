def get_request_info(parsed_logs):
    total_requests = 0
    status_counts ={}
    endp_counts = {}

    for entry in parsed_logs:
        if entry["type"] == "request":
            total_requests+=1
            endp_counts[entry["endpoint"]] = endp_counts.get(entry["endpoint"], 0) + 1
            status_counts[entry['status']] = status_counts.get(entry['status'],0) + 1

            if entry["endpoint"] not in endp_counts:
                endp_counts[entry["endpoint"]] = {"GET": 0, "POST": 0}

            endp_counts[entry["endpoint"]][entry["method"]] += 1
    return {
        "total_requests":total_requests,
        "status_counts": status_counts,
        "endpoint_counts": endp_counts
    }

def get_performance_metrics(parsed_logs):
    times_success = {}
    times_fail = {}

    for entry in parsed_logs:
        if entry["type"] == "request":
            endpoint = entry["endpoint"]
            t = entry["time_ms"]
            status = entry["status"]

            if status == 200:
                if endpoint not in times_success:
                    times_success[endpoint] = []
                times_success[endpoint].append(t)
            else:
                if endpoint not in times_fail:
                    times_fail[endpoint] = []
                times_fail[endpoint].append(t)

    # Build stats
    def make_stats(time_list):
        return {
            "avg": sum(time_list) / len(time_list),
            "max": max(time_list)
        } if time_list else {"avg": None, "max": None}

    success_metrics = {ep: make_stats(vals) for ep, vals in times_success.items()}
    fail_metrics = {ep: make_stats(vals) for ep, vals in times_fail.items()}

    return {
        "success": success_metrics,
        "fail": fail_metrics
    }


def get_user_info(parsed_logs):
    unique_users = set()
    user_yearwise ={}
    for entry in parsed_logs:
        if entry["type"]=="user":
            user_id = entry['user_id']
            year = user_id[:4]

            unique_users.add(user_id)
            user_yearwise[year] = user_yearwise.get(year, set())
            user_yearwise[year].add(user_id)

    user_year_count={year: len(ids) for year, ids in user_yearwise.items()}
    return{
        "unique_users":len(unique_users),
        "users_yearwise":user_year_count
    }