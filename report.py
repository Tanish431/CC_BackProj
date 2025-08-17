import argparse
from src.parser import parse_line
from src.analysis import (
    get_request_info,
    get_performance_metrics,
    get_user_info,
    get_app_insights,
    get_misc_info,
)
from src.visuals import (
    plot_endpoint_pie,
    plot_strategy_pie,
)

def report_endpoints(parsed):
    req_info = get_request_info(parsed)
    print("-----------------------------------")
    print("📈 Traffic & Usage Analysis")
    print("-----------------------------------")
    print(f"  Total API Requests logged: {req_info['total_requests']}")
    print("  HTTP Status Codes:")
    for status, count in req_info["status_counts"].items():
        print(f"    - {status}: {count} times")

    #Compare GET vs POST
    print("  Endpoint Popularity:")
    for endpoint, data in sorted(req_info["endpoint_counts"].items(),
                                 key=lambda x: x[1]["percent"],
                                 reverse=True):
        print(f"  Endpoint: {endpoint}")
        print(f"    - Total Requests: {data['total']} ({data['percent']:.2f}%)")
        if data["GET"] > 0:
            print(f"    - GET: {data['GET']}")
        if data["POST"] > 0:
            print(f"    - POST: {data['POST']}")

def report_performance(parsed):
    perf = get_performance_metrics(parsed)
    print("\n-----------------------------------")
    print("🚀 Performance Metrics")
    print("-----------------------------------")
    print("  Success (200):")
    for endpoint, stats in perf["success"].items():
        print(f"  Endpoint: {endpoint}")
        print(f"    - Average Response Time: {stats['avg']:.3f} ms")
        print(f"    - Max Response Time: {stats['max']:.3f} ms")
    print("  Failures and others (!=200):")
    for endpoint, stats in perf["fail"].items():
        print(f"  Endpoint: {endpoint}")
        print(f"    - Average Response Time: {stats['avg']:.6f} ms")
        print(f"    - Max Response Time: {stats['max']:.6f} ms")

def report_users(parsed):
    users = get_user_info(parsed)
    print("\n-----------------------------------")
    print("👤 Unique ID Analysis")
    print("-----------------------------------")
    print(f"  Total Unique IDs found: {users['unique_users']}")
    print("  By Year:")
    for year, count in sorted(users["users_yearwise"].items()):
        print(f"    Batch of {year}: {count} unique IDs")

def report_app(parsed):
    app = get_app_insights(parsed)
    print("\n-----------------------------------")
    print("📅 Timetable Generation Insights")
    print("-----------------------------------")
    print(f"  Total Attempts: {app['generation_attempts']}")
    print(f"  Total Timetables Found: {app['total_found']}")
    print(f"  Average Found per /generate Attempt: {app['avg_found']:.2f}")
    print("  Strategy Usage:")
    for strat, count in app["strategy_counts"].items():
        print(f"    {strat}: {count}")

def report_misc(parsed):
    misc = get_misc_info(parsed)
    print("\n-----------------------------------")
    print("🛠 Miscellaneous")
    print("-----------------------------------")
    print(f"  Malformed Requests: {misc['malformed_requests']}")
    print(f"  CONNECT Attempts: {misc['connect_attempts']}")
    print(f"  reCAPTCHA Errors: {misc['recaptcha_errors']}")
    print(f"  reCAPTCHA Fails: {misc['recaptcha_fails']}")

    #All other things in the log file
    if misc["recaptcha_fails"] > 0:
        avg_score = sum(misc["recaptcha_fail_scores"]) / len(misc["recaptcha_fail_scores"])
        print(f"    Avg reCAPTCHA Score: {avg_score:.2f}")
        print("    Actions:")
        for action, count in misc["recaptcha_fail_actions"].items():
            print(f"      {action}: {count}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="log analysis reports")
    parser.add_argument("--endpoints", action="store_true", help="Show endpoint popularity")
    parser.add_argument("--performance", action="store_true", help="Show performance metrics")
    parser.add_argument("--users", action="store_true", help="Show user stats")
    parser.add_argument("--app", action="store_true", help="Show app insights")
    parser.add_argument("--misc", action="store_true", help="Show misc info")
    parser.add_argument("--all", action="store_true", help="Show full report")
    parser.add_argument("--graph", action="store_true", help="Show graph")

    args = parser.parse_args()
    #For running python report.py
    if not any(vars(args).values()):
        args.all = True
    
    #Reader
    try:
        with open("data/timetable.log") as f:
            lines = f.readlines()
    except FileNotFoundError:
        print("Error: Log file 'data/timetable.log' not found.")
        exit(1)
    except Exception as e:
        print(f"Error reading log file: {e}")
        exit(1)

    #Parse logs
    parsed_logs = []
    for line in lines:
        try:
            parsed = parse_line(line)
            if parsed is not None:
                parsed_logs.append(parsed)
        except Exception as e:
            print(f"Warning: Failed to parse line: {line.strip()}\n  Reason: {e}")

    #For argparse
    try:
        if not parsed_logs:
            raise ValueError("No valid log entries found.")
        if args.endpoints and args.graph:
            plot_endpoint_pie(get_request_info(parsed_logs))
        elif args.all or args.endpoints:
            report_endpoints(parsed_logs)
            plot_endpoint_pie(get_request_info(parsed_logs))
        if args.all or args.performance:
            report_performance(parsed_logs)
        if args.all or args.users:
            report_users(parsed_logs)
        if args.app and args.graph:
            plot_strategy_pie(get_app_insights(parsed_logs))
        elif args.all or args.app:
            report_app(parsed_logs)
            plot_strategy_pie(get_app_insights(parsed_logs))
        if args.all or args.misc:
            report_misc(parsed_logs)
    except Exception as e:
        print(f"An unexpected error occurred during reporting: {e}")
