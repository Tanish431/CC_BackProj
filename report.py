from src.parser import parse_line
from src.analysis import get_endpoint_popularity

def main():
    with open("data/timetable.log") as f:
        lines = f.readlines()

    parsed = [parse_line(line) for line in lines]
    popularity = get_endpoint_popularity(parsed)

    print("Endpoint Popularity:", popularity)

if __name__ == "__main__":
    main()
