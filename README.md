# CC Backend Project: Log Analysis
This is my attempt in making a python project for analysing the Timetable Generator Application. It includes detailed reporting on data and some visualisations about API Usage, performance, user informations and more.

## All Features:
- **Traffic & Usage Analysis:** See total requests, status codes, and endpoint popularity with help of a Pie chart too.
- **Performance Metrics:** Average and maximum response times for successful and failed requests.
- **User Analysis:** Unique user IDs with their Year information.
- **Timetable Generation/Application Insights:** Attempts, timetables found, and strategy usage.
- **Miscellaneous:** Malformed requests, connect attempts, reCAPTCHA errors/fails.

## Usage:

Make sure to place your log file at `data/timetable.log`.

Run the report script with desired call generation arguments:
```sh
python report.py [options]
```

### Options

- `--endpoints`    Show endpoint popularity 
- `--performance`  Show performance metrics
- `--users`        Show user stats
- `--app`          Show app insights
- `--misc`         Show misc info
- `--all`          Show full report (default if no options given)
- `--graph`        Shows only pie chart (use with --endpoints or --app)

**Example:**
```sh
python report.py --endpoints --graph
```

## How It Works

1. **Parsing:** Each log line is parsed into a dictionary (`src/parser.py`).
2. **Analysis:** Parsed logs are analyzed for calculations and evaluations (`src/analysis.py`).
3. **Reporting:** Results are printed to the console (`report.py`).
4. **Visualization:** Pie charts are generated for endpoint and strategy usage (`src/visuals.py`).
