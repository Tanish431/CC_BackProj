from src.parser import parse_line
from src.analysis import (
    get_request_info,
    get_performance_metrics,
    get_user_info,
    get_application_insights,
    get_misc_info,
)


def main():
    # Load logs
    with open("data/timetable.log") as f:
        lines = f.readlines()

    # Parse logs
    parsed = [parse_line(line) for line in lines]

    # --- API Request Info ---
    req_info = get_request_info(parsed)
    print("📊 API Requests")
    print(f"  Total Requests: {req_info['total_requests']}")
    print("  Status Codes:")
    for status, count in req_info["status_counts"].items():
        print(f"    {status}: {count}")
    print("  Endpoint Popularity (GET vs POST):")
    for endpoint, methods in req_info["endpoint_counts"].items():
        print(f"    {endpoint}: GET={methods['GET']}, POST={methods['POST']}")

    # --- Performance Metrics ---
    perf = get_performance_metrics(parsed)
    print("\n⚡ Performance Metrics")
    print("  Success (200):")
    for endpoint, stats in perf["success"].items():
        print(f"    {endpoint}: avg={stats['avg']:.3f} ms, max={stats['max']:.3f} ms")
    print("  Failures (!=200):")
    for endpoint, stats in perf["fail"].items():
        print(f"    {endpoint}: avg={stats['avg']:.6f} ms, max={stats['max']:.6f} ms")

    # --- Unique Users ---
    users = get_user_info(parsed)
    print("\n👤 Unique Users")
    print(f"  Total Unique Users: {users['unique_users']}")
    print("  By Year:")
    for year, count in sorted(users["users_yearwise"].items()):
        print(f"    {year}: {count}")

    # --- Application Insights (Timetable Generation) ---
    app = get_application_insights(parsed)
    print("\n📅 Timetable Generation Insights")
    print(f"  Total Attempts: {app['generation_attempts']}")
    print(f"  Total Timetables Found: {app['total_found']}")
    print(f"  Average Found per Attempt: {app['avg_found']:.2f}")
    print("  Strategy Usage:")
    for strat, count in app["strategy_counts"].items():
        print(f"    {strat}: {count}")

    # --- Miscellaneous ---
    misc = get_misc_info(parsed)
    print("\n🛠 Miscellaneous")
    print(f"  Malformed Requests: {misc['malformed_requests']}")
    print(f"  CONNECT Attempts: {misc['connect_attempts']}")
    print(f"  reCAPTCHA Errors: {misc['recaptcha_errors']}")
    print(f"  reCAPTCHA Fails: {misc['recaptcha_fails']}")

    if misc["recaptcha_fails"] > 0:
        avg_score = sum(misc["recaptcha_fail_scores"]) / len(misc["recaptcha_fail_scores"])
        print(f"    Avg reCAPTCHA Score: {avg_score:.2f}")
        print("    Actions:")
        for action, count in misc["recaptcha_fail_actions"].items():
            print(f"      {action}: {count}")


if __name__ == "__main__":
    main()
