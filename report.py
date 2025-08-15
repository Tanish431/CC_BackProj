from src.parser import parse_line
from src.analysis import get_request_info, get_user_info

def main():
    with open("data/timetable.log") as f:
        lines = f.readlines()

    parsed = [parse_line(line) for line in lines]
    popularity = get_request_info(parsed)
    user_info = get_user_info(parsed)

    print("Endpoint Popularity:", popularity)
    
    print("\nUnique Users:", user_info['unique_users'])
    for year,count in sorted(user_info['users_yearwise'].items()):
        print(year , "-" , count)

if __name__ == "__main__":
    main()
