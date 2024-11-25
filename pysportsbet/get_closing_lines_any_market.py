import requests
import openpyxl
from datetime import datetime, timedelta

# Configuration constants
SPREADSHEET_FILE = 'odds_data.xlsx'  # Path to the output Excel file
SHEET_NAME = 'Sheet1'  # Name of the sheet in the Excel file
API_KEY = 'YOUR_API_KEY'  # Replace with your API key from The Odds API
SPORT_KEY = 'baseball_mlb'  # The sport key for the desired sport
MARKETS = 'batter_home_runs'  # Comma-separated list of betting markets
REGIONS = 'us'  # Comma-separated list of regions for bookmakers
BOOKMAKERS = ''  # Optional: Specific bookmakers instead of regions
ODDS_FORMAT = 'american'  # Format of the odds: 'american' or 'decimal'
FROM_DATE = '2024-04-03T00:00:00Z'  # Start date for historical data
TO_DATE = '2024-04-04T00:00:00Z'  # End date for historical data
INTERVAL_MINS = 60 * 24  # Interval between historical snapshots in minutes

# Column headers for the Excel output
HEADERS = [
    'timestamp', 'id', 'commence_time', 'bookmaker', 'last_update',
    'home_team', 'away_team', 'market', 'name', 'description', 'price', 'point'
]

def fetch_events(api_key, sport_key, timestamp):
    """
    Fetch historical events from The Odds API for a given sport and timestamp.
    """
    url = f"https://api.the-odds-api.com/v4/historical/sports/{sport_key}/events"
    params = {
        'apiKey': api_key,
        'date': timestamp
    }
    response = requests.get(url, params=params)
    response.raise_for_status()  # Raise an exception for HTTP errors
    return response.json()

def fetch_event_odds(api_key, sport_key, regions, bookmakers, markets, odds_format, timestamp, event_id):
    """
    Fetch odds for a specific event from The Odds API.
    """
    bookmakers_param = f"bookmakers={bookmakers}" if bookmakers else f"regions={regions}"
    url = f"https://api.the-odds-api.com/v4/historical/sports/{sport_key}/events/{event_id}/odds"
    params = {
        'apiKey': api_key,
        bookmakers_param: bookmakers_param,
        'markets': markets,
        'oddsFormat': odds_format,
        'date': timestamp
    }
    response = requests.get(url, params=params)
    response.raise_for_status()  # Raise an exception for HTTP errors
    return response.json()

def extract_commence_times(events, from_date, to_date):
    """
    Extract commence times for events within the specified date range.
    """
    event_commence_times = {}
    for event in events:
        if from_date <= event['commence_time'] <= to_date:
            # Store event ID and its commence time
            event_commence_times[event['id']] = event['commence_time']
    return event_commence_times

def format_event_output(response):
    """
    Format the API response into rows suitable for writing to a spreadsheet.
    """
    rows = []
    event = response['data']
    for bookmaker in event.get('bookmakers', []):
        for market in bookmaker.get('markets', []):
            for outcome in market.get('outcomes', []):
                rows.append([
                    response['timestamp'], event['id'], event['commence_time'],
                    bookmaker['key'], bookmaker['last_update'],
                    event['home_team'], event['away_team'],
                    market['key'], outcome['name'], outcome.get('description'),
                    outcome['price'], outcome.get('point')
                ])
    return rows

def main():
    """
    Main function to query data from The Odds API and save it to an Excel spreadsheet.
    """
    # Initialize a new workbook and select the active sheet
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = SHEET_NAME

    # Write headers to the first row of the sheet
    ws.append(HEADERS)

    # Parse FROM_DATE and TO_DATE into datetime objects
    from_datetime = datetime.fromisoformat(FROM_DATE[:-1])
    to_datetime = datetime.fromisoformat(TO_DATE[:-1])
    current_datetime = from_datetime

    # Dictionary to store event commence times
    event_commence_times = {}

    # Fetch events in intervals within the date range
    while current_datetime <= to_datetime:
        formatted_timestamp = current_datetime.isoformat() + 'Z'
        print(f"Gathering games {formatted_timestamp}")
        events_response = fetch_events(API_KEY, SPORT_KEY, formatted_timestamp)
        event_commence_times.update(
            extract_commence_times(events_response.get('data', []), FROM_DATE, TO_DATE)
        )
        current_datetime += timedelta(minutes=INTERVAL_MINS)

    # Iterate through event commence times and fetch odds
    for commence_time, event_ids in event_commence_times.items():
        print(f"Querying closing lines for commence time {commence_time}")
        for event_id in event_ids:
            odds_response = fetch_event_odds(API_KEY, SPORT_KEY, REGIONS, BOOKMAKERS, MARKETS, ODDS_FORMAT, commence_time, event_id)
            formatted_rows = format_event_output(odds_response)
            for row in formatted_rows:
                ws.append(row)  # Append each row to the spreadsheet

    # Save the spreadsheet to the specified file
    wb.save(SPREADSHEET_FILE)
    print(f"Data saved to {SPREADSHEET_FILE}")

if __name__ == "__main__":
    main()
