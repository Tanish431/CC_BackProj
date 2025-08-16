def get_request_info(parsed_logs):
    total_requests = 0
    status_counts = {}
    endpoint_counts = {}

    for entry in parsed_logs:
        if entry["type"] == "request":
            total_requests += 1

            # Count status
            status = entry["status"]
            status_counts[status] = status_counts.get(status, 0) + 1

            # Endpoint GET vs POST
            endpoint = entry["endpoint"]
            method = entry["method"]

            if endpoint not in endpoint_counts:
                endpoint_counts[endpoint] = {"GET": 0, "POST": 0}

            endpoint_counts[endpoint][method] += 1

    return {
        "total_requests": total_requests,
        "status_counts": status_counts,
        "endpoint_counts": endpoint_counts
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

def get_application_insights(parsed_logs):
    strategy = None
    generation_attempts = 0
    total_found = 0
    strategy_counts = {}

    for entry in parsed_logs:
        if entry["type"] == "algorithm":
            strategy = entry["algo"]

        elif entry["type"] == "summary":
            generation_attempts += 1
            total_found += entry["found"]

            used = strategy if strategy else "Unknown"
            strategy_counts[used] = strategy_counts.get(used, 0) + 1

            strategy = None

    avg_found = total_found / generation_attempts if generation_attempts else 0

    return {
        "total_found": total_found,
        "generation_attempts": generation_attempts,
        "avg_found": avg_found,
        "strategy_counts": strategy_counts
    }

def get_misc_info(parsed_logs):
    malformed_count = 0
    connect_count = 0
    recaptcha_errors = 0
    recaptcha_fails = 0
    recaptcha_fail_scores = []
    recaptcha_fail_actions = {}

    for entry in parsed_logs:
        if entry["type"] == "malformed":
            malformed_count += 1

        elif entry["type"] == "connect":
            connect_count += 1

        elif entry["type"] == "recaptcha_error":
            recaptcha_errors += 1

        elif entry["type"] == "recaptcha_fail":
            recaptcha_fails += 1
            recaptcha_fail_scores.append(entry["score"])
            action = entry["action"] or "unknown"
            recaptcha_fail_actions[action] = recaptcha_fail_actions.get(action, 0) + 1

    return {
        "malformed_requests": malformed_count,
        "connect_attempts": connect_count,
        "recaptcha_errors": recaptcha_errors,
        "recaptcha_fails": recaptcha_fails,
        "recaptcha_fail_scores": recaptcha_fail_scores,
        "recaptcha_fail_actions": recaptcha_fail_actions
    }
