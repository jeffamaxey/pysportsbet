import requests
import openpyxl

# Configuration constants
SPREADSHEET_FILE = "odds_data.xlsx"  # Path to the output Excel file
SHEET_NAME = "Sheet1"  # Name of the sheet in the Excel file
API_KEY = "YOUR_API_KEY"  # Replace with your API key from The Odds API
SPORT_KEY = "americanfootball_nfl"  # Sport key for querying events
MARKETS = "player_pass_tds,player_pass_yds,player_pass_completions"  # Betting markets
REGIONS = "us"  # Supported regions: us, uk, eu, au
BOOKMAKERS = ""  # Optional: Specific bookmakers
ODDS_FORMAT = "american"  # Odds format: 'american' or 'decimal'
DATE_FORMAT = "iso"  # Date format: 'iso' or 'unix'


def fetch_events(api_key, sport_key, markets, regions, bookmakers, odds_format, date_format):
    """
    Fetch live and upcoming events for a specified sport.

    Args:
        api_key (str): The Odds API key.
        sport_key (str): Sport key (e.g., 'americanfootball_nfl').
        markets (str): Comma-separated list of betting markets.
        regions (str): Comma-separated list of regions (e.g., 'us').
        bookmakers (str): Comma-separated list of bookmakers.
        odds_format (str): Format of the odds ('american' or 'decimal').
        date_format (str): Format of the date ('iso' or 'unix').

    Returns:
        list: A list of events from the API response.
    """
    bookmakers_param = f"bookmakers={bookmakers}" if bookmakers else f"regions={regions}"
    url = (
        f"https://api.the-odds-api.com/v4/sports/{sport_key}/odds?"
        f"apiKey={api_key}&{bookmakers_param}&markets={markets}&oddsFormat={odds_format}&dateFormat={date_format}"
    )
    response = requests.get(url, headers={"content-type": "application/json"})
    response.raise_for_status()
    return response.json()


def fetch_event_markets(api_key, sport_key, markets, regions, bookmakers, odds_format, date_format, event_id):
    """
    Fetch market odds for a specific event.

    Args:
        api_key (str): The Odds API key.
        sport_key (str): Sport key (e.g., 'americanfootball_nfl').
        markets (str): Comma-separated list of betting markets.
        regions (str): Comma-separated list of regions (e.g., 'us').
        bookmakers (str): Comma-separated list of bookmakers.
        odds_format (str): Format of the odds ('american' or 'decimal').
        date_format (str): Format of the date ('iso' or 'unix').
        event_id (str): The ID of the event.

    Returns:
        dict: A dictionary containing metadata and event data.
    """
    bookmakers_param = f"bookmakers={bookmakers}" if bookmakers else f"regions={regions}"
    url = (
        f"https://api.the-odds-api.com/v4/sports/{sport_key}/events/{event_id}/odds?"
        f"apiKey={api_key}&{bookmakers_param}&markets={markets}&oddsFormat={odds_format}&dateFormat={date_format}"
    )
    response = requests.get(url, headers={"content-type": "application/json"})
    response.raise_for_status()
    return {
        "metaData": format_response_meta_data(response.headers),
        "eventData": format_event_output(response.json()),
    }


def format_event_output(event):
    """
    Format a single event's data into a tabular structure for Excel output.

    Args:
        event (dict): Event data from the API.

    Returns:
        list: A 2D list of formatted rows.
    """
    rows = []
    for bookmaker in event.get("bookmakers", []):
        for market in bookmaker.get("markets", []):
            for outcome in market.get("outcomes", []):
                rows.append([
                    event["id"],
                    event["commence_time"],
                    bookmaker["key"],
                    market["last_update"],
                    event["home_team"],
                    event["away_team"],
                    market["key"],
                    outcome.get("name"),
                    outcome.get("description"),
                    outcome.get("price"),
                    outcome.get("point"),
                ])
    return rows


def format_response_meta_data(headers):
    """
    Extract metadata from the response headers.

    Args:
        headers (dict): Response headers from the API request.

    Returns:
        list: A list of metadata rows for Excel output.
    """
    return [
        ["Requests Used", headers.get("x-requests-used")],
        ["Requests Remaining", headers.get("x-requests-remaining")],
    ]


def main():
    """
    Main function to fetch player props and save them to an Excel file.

    This function fetches events, queries markets for each event, and writes the aggregated
    data into a single spreadsheet.

    Writes:
        An Excel file with metadata and event data saved to `SPREADSHEET_FILE`.
    """
    # Fetch events
    events = fetch_events(API_KEY, SPORT_KEY, "h2h", REGIONS, BOOKMAKERS, ODDS_FORMAT, DATE_FORMAT)

    if not events:
        print("No events found")
        return

    # Initialize the output list
    output = []
    meta_data = None

    # Fetch markets for each event
    for event in events:
        market_response = fetch_event_markets(API_KEY, SPORT_KEY, MARKETS, REGIONS, BOOKMAKERS, ODDS_FORMAT, DATE_FORMAT, event["id"])
        output.extend(market_response["eventData"])
        meta_data = market_response["metaData"]

    # Add headers to the output
    headers = [
        "id", "commence_time", "bookmaker", "last_update", "home_team",
        "away_team", "market", "label", "description", "price", "point"
    ]
    output.insert(0, headers)

    # Initialize the Excel workbook
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = SHEET_NAME

    # Write metadata
    for row in meta_data:
        ws.append(row)

    # Add an empty row for spacing
    ws.append([])

    # Write event data
    for row in output:
        ws.append(row)

    # Save the workbook to a file
    wb.save(SPREADSHEET_FILE)
    print(f"Data saved to {SPREADSHEET_FILE}")


if __name__ == "__main__":
    main()
