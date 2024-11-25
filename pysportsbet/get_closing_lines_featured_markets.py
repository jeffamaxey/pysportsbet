import requests
import openpyxl
from datetime import datetime, timedelta

# Configuration constants
SPREADSHEET_FILE = "odds_data.xlsx"  # Path to the output Excel file
SHEET_NAME = "Sheet1"  # Name of the sheet in the Excel file
API_KEY = "YOUR_API_KEY"  # Replace with your API key from The Odds API
SPORT_KEY = "icehockey_nhl"  # The sport key for the desired sport
MARKETS = "h2h"  # Supported markets: h2h, spreads, totals
REGIONS = "us"  # Supported regions: us, uk, eu, au
BOOKMAKERS = "betonlineag"  # Optional: Specific bookmaker
ODDS_FORMAT = "american"  # Format of the odds: 'american' or 'decimal'
FROM_DATE = "2023-12-31T00:00:00Z"  # Start date for data retrieval
TO_DATE = "2024-01-01T00:00:00Z"  # End date for data retrieval
INTERVAL_MINS = 60 * 24  # Interval between historical snapshots

# Column headers for the Excel output
HEADERS = [
    "timestamp", "id", "commence_time", "bookmaker", "last_update",
    "home_team", "away_team", "market", "label_1", "odd_1", "point_1",
    "label_2", "odd_2", "point_2", "odd_draw"
]


def fetch_events(api_key, sport_key, timestamp):
    """
    Fetch historical events from The Odds API.
    """
    url = f"https://api.the-odds-api.com/v4/historical/sports/{sport_key}/events"
    params = {"apiKey": api_key, "date": timestamp}
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()


def fetch_odds(api_key, sport_key, regions, bookmakers, markets, odds_format, timestamp, event_ids):
    """
    Fetch odds for specific events from The Odds API.
    """
    bookmakers_param = f"bookmakers={bookmakers}" if bookmakers else f"regions={regions}"
    event_ids_param = f"&eventIds={','.join(event_ids)}" if event_ids else ""
    url = f"https://api.the-odds-api.com/v4/historical/sports/{sport_key}/odds"
    params = {
        "apiKey": api_key,
        bookmakers_param: bookmakers_param,
        "markets": markets,
        "oddsFormat": odds_format,
        "date": timestamp,
    }
    response = requests.get(url + event_ids_param, params=params)
    response.raise_for_status()
    return response.json()


def extract_commence_times(events, from_date, to_date):
    """
    Extract event commence times within a specified range.
    """
    event_commence_times = {}
    for event in events:
        if from_date <= event["commence_time"] <= to_date:
            event_commence_times[event["id"]] = event["commence_time"]
    return event_commence_times


def format_event_output(response):
    """
    Format API response into rows suitable for Excel output.
    """
    rows = []
    for event in response["data"]:
        for bookmaker in event.get("bookmakers", []):
            for market in bookmaker.get("markets", []):
                outcome_home = None
                outcome_away = None
                outcome_draw = None

                if market["key"] == "totals":
                    outcome_home = next((o for o in market["outcomes"] if o["name"] == "Over"), {})
                    outcome_away = next((o for o in market["outcomes"] if o["name"] == "Under"), {})
                    outcome_draw = {}
                else:
                    outcome_home = next((o for o in market["outcomes"] if o["name"] == event["home_team"]), {})
                    outcome_away = next((o for o in market["outcomes"] if o["name"] == event["away_team"]), {})
                    outcome_draw = next((o for o in market["outcomes"] if o["name"] == "Draw"), {})

                rows.append([
                    response["timestamp"], event["id"], event["commence_time"], bookmaker["key"],
                    bookmaker["last_update"], event["home_team"], event["away_team"], market["key"],
                    outcome_home.get("name"), outcome_home.get("price"), outcome_home.get("point"),
                    outcome_away.get("name"), outcome_away.get("price"), outcome_away.get("point"),
                    outcome_draw.get("price")
                ])
    return rows


def main():
    """
    Main function to query data and save it to an Excel spreadsheet.
    """
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = SHEET_NAME

    # Write headers
    ws.append(HEADERS)

    # Parse dates and initialize variables
    from_datetime = datetime.fromisoformat(FROM_DATE[:-1])
    to_datetime = datetime.fromisoformat(TO_DATE[:-1])
    current_datetime = from_datetime
    event_commence_times = {}

    # Fetch events over the date range
    while current_datetime <= to_datetime:
        formatted_timestamp = current_datetime.isoformat() + "Z"
        print(f"Gathering games {formatted_timestamp}")
        events_response = fetch_events(API_KEY, SPORT_KEY, formatted_timestamp)
        event_commence_times.update(
            extract_commence_times(events_response.get("data", []), FROM_DATE, TO_DATE)
        )
        current_datetime += timedelta(minutes=INTERVAL_MINS)

    # Group events by commence time
    grouped_events = {}
    for commence_time in set(event_commence_times.values()):
        grouped_events[commence_time] = [
            event_id for event_id, time in event_commence_times.items() if time == commence_time
        ]

    # Fetch odds and write to the spreadsheet
    for commence_time, event_ids in grouped_events.items():
        print(f"Querying closing lines for commence time {commence_time}")
        odds_response = fetch_odds(API_KEY, SPORT_KEY, REGIONS, BOOKMAKERS, MARKETS, ODDS_FORMAT, commence_time,
                                   event_ids)
        formatted_rows = format_event_output(odds_response)
        for row in formatted_rows:
            ws.ap
