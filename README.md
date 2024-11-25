<!--  DELETE THE LINES ABOVE THIS AND WRITE YOUR PROJECT README BELOW -->

---
# pysportsbet

[![codecov](https://codecov.io/gh/jeffamaxey/pysportsbet/branch/main/graph/badge.svg?token=pysportsbet_token_here)](https://codecov.io/gh/jeffamaxey/pysportsbet)
[![CI](https://github.com/jeffamaxey/pysportsbet/actions/workflows/main.yml/badge.svg)](https://github.com/jeffamaxey/pysportsbet/actions/workflows/main.yml)

Awesome pysportsbet created by jeffamaxey

---
## Install it from PyPI

```bash
pip install pysportsbet
```

---
## Usage

```py
from pysportsbet import BaseClass
from pysportsbet import base_function

BaseClass().base_method()
base_function()
```

```bash
$ python -m pysportsbet
#or
$ pysportsbet
```

---
## Sports Odds APIs
An API key for The-Odds.com  gives access to all available sports. These sports are covered by the API when in season:

[Swagger API](https://app.swaggerhub.com/apis-docs/the-odds-api/odds-api/4#/)

|      **Group**     	|       **League / Tournament**       	|       **Sport Key (use in the API)**       	| **Scores & Results** 	|
|:------------------:	|:-----------------------------------:	|:------------------------------------------:	|:--------------------:	|
| American Football  	| CFL                                 	| americanfootball_cfl                       	| ✔                    	|
| American Football  	| NCAAF                               	| americanfootball_ncaaf                     	| ✔                    	|
| American Football  	| NCAAF Championship Winner           	| americanfootball_ncaaf_championship_winner 	|                      	|
| American Football  	| NFL                                 	| americanfootball_nfl                       	| ✔                    	|
| American Football  	| NFL Preseason                       	| americanfootball_nfl_preseason             	| ✔                    	|
| American Football  	| NFL Super Bowl Winner               	| americanfootball_nfl_super_bowl_winner     	|                      	|
| American Football  	| UFL                                 	| americanfootball_ufl                       	| ✔                    	|
| Aussie Rules       	| AFL                                 	| aussierules_afl                            	| ✔                    	|
| Baseball           	| MLB                                 	| baseball_mlb                               	| ✔                    	|
| Baseball           	| MLB Preseason                       	| baseball_mlb_preseason                     	|                      	|
| Baseball           	| MLB World Series Winner             	| baseball_mlb_world_series_winner           	|                      	|
| Baseball           	| Minor League Baseball               	| baseball_milb                              	|                      	|
| Baseball           	| NPB                                 	| baseball_npb                               	|                      	|
| Baseball           	| KBO League                          	| baseball_kbo                               	|                      	|
| Baseball           	| NCAA Baseball                       	| baseball_ncaa                              	|                      	|
| Basketball         	| Basketball Euroleague               	| basketball_euroleague                      	| ✔                    	|
| Basketball         	| NBA                                 	| basketball_nba                             	| ✔                    	|
| Basketball         	| NBA Championship Winner             	| basketball_nba_championship_winner         	|                      	|
| Basketball         	| WNBA                                	| basketball_wnba                            	| ✔                    	|
| Basketball         	| NCAAB                               	| basketball_ncaab                           	| ✔                    	|
| Basketball         	| NCAAB Championship Winner           	| basketball_ncaab_championship_winner       	|                      	|
| Boxing             	| Boxing                              	| boxing_boxing                              	|                      	|
| Cricket            	| Big Bash                            	| cricket_big_bash                           	|                      	|
| Cricket            	| Caribbean Premier League            	| cricket_caribbean_premier_league           	|                      	|
| Cricket            	| ICC World Cup                       	| cricket_icc_world_cup                      	|                      	|
| Cricket            	| International Twenty20              	| cricket_international_t20                  	|                      	|
| Cricket            	| IPL                                 	| cricket_ipl                                	|                      	|
| Cricket            	| One Day Internationals              	| cricket_odi                                	|                      	|
| Cricket            	| Pakistan Super League               	| cricket_psl                                	|                      	|
| Cricket            	| T20 Blast                           	| cricket_t20_blast                          	|                      	|
| Cricket            	| Test Matches                        	| cricket_test_match                         	|                      	|
| Golf               	| Masters Tournament Winner           	| golf_masters_tournament_winner             	|                      	|
| Golf               	| PGA Championship Winner             	| golf_pga_championship_winner               	|                      	|
| Golf               	| The Open Winner                     	| golf_the_open_championship_winner          	|                      	|
| Golf               	| US Open Winner                      	| golf_us_open_winner                        	|                      	|
| Ice Hockey         	| NHL                                 	| icehockey_nhl                              	| ✔                    	|
| Ice Hockey         	| NHL Championship Winner             	| icehockey_nhl_championship_winner          	|                      	|
| Ice Hockey         	| SHL                                 	| icehockey_sweden_hockey_league             	|                      	|
| Ice Hockey         	| HockeyAllsvenskan                   	| icehockey_sweden_allsvenskan               	|                      	|
| Lacrosse           	| Premier Lacrosse League             	| lacrosse_pll                               	|                      	|
| Mixed Martial Arts 	| MMA                                 	| mma_mixed_martial_arts                     	|                      	|
| Politics           	| US Presidential Elections Winner    	| politics_us_presidential_election_winner   	|                      	|
| Rugby League       	| NRL                                 	| rugbyleague_nrl                            	| ✔                    	|
| Soccer             	| Africa Cup of Nations               	| soccer_africa_cup_of_nations               	|                      	|
| Soccer             	| Primera División - Argentina        	| soccer_argentina_primera_division          	| ✔                    	|
| Soccer             	| A-League                            	| soccer_australia_aleague                   	| ✔                    	|
| Soccer             	| Austrian Football Bundesliga        	| soccer_austria_bundesliga                  	| ✔                    	|
| Soccer             	| Belgium First Div                   	| soccer_belgium_first_div                   	| ✔                    	|
| Soccer             	| Brazil Série A                      	| soccer_brazil_campeonato                   	| ✔                    	|
| Soccer             	| Brazil Série B                      	| soccer_brazil_serie_b                      	| ✔                    	|
| Soccer             	| Primera División - Chile            	| soccer_chile_campeonato                    	| ✔                    	|
| Soccer             	| Super League - China                	| soccer_china_superleague                   	| ✔                    	|
| Soccer             	| Denmark Superliga                   	| soccer_denmark_superliga                   	| ✔                    	|
| Soccer             	| Championship                        	| soccer_efl_champ                           	| ✔                    	|
| Soccer             	| EFL Cup                             	| soccer_england_efl_cup                     	| ✔                    	|
| Soccer             	| League 1                            	| soccer_england_league1                     	| ✔                    	|
| Soccer             	| League 2                            	| soccer_england_league2                     	| ✔                    	|
| Soccer             	| EPL                                 	| soccer_epl                                 	| ✔                    	|
| Soccer             	| FA Cup                              	| soccer_fa_cup                              	| ✔                    	|
| Soccer             	| FIFA World Cup                      	| soccer_fifa_world_cup                      	| ✔                    	|
| Soccer             	| FIFA Women's World Cup              	| soccer_fifa_world_cup_womens               	| ✔                    	|
| Soccer             	| FIFA World Cup Winner               	| soccer_fifa_world_cup_winner               	|                      	|
| Soccer             	| Veikkausliiga - Finland             	| soccer_finland_veikkausliiga               	| ✔                    	|
| Soccer             	| Ligue 1 - France                    	| soccer_france_ligue_one                    	| ✔                    	|
| Soccer             	| Ligue 2 - France                    	| soccer_france_ligue_two                    	| ✔                    	|
| Soccer             	| Bundesliga - Germany                	| soccer_germany_bundesliga                  	| ✔                    	|
| Soccer             	| Bundesliga 2 - Germany              	| soccer_germany_bundesliga2                 	| ✔                    	|
| Soccer             	| 3. Liga - Germany                   	| soccer_germany_liga3                       	| ✔                    	|
| Soccer             	| Super League - Greece               	| soccer_greece_super_league                 	| ✔                    	|
| Soccer             	| Serie A - Italy                     	| soccer_italy_serie_a                       	| ✔                    	|
| Soccer             	| Serie B - Italy                     	| soccer_italy_serie_b                       	| ✔                    	|
| Soccer             	| J League                            	| soccer_japan_j_league                      	| ✔                    	|
| Soccer             	| K League 1                          	| soccer_korea_kleague1                      	| ✔                    	|
| Soccer             	| League of Ireland                   	| soccer_league_of_ireland                   	| ✔                    	|
| Soccer             	| Liga MX                             	| soccer_mexico_ligamx                       	| ✔                    	|
| Soccer             	| Dutch Eredivisie                    	| soccer_netherlands_eredivisie              	| ✔                    	|
| Soccer             	| Eliteserien - Norway                	| soccer_norway_eliteserien                  	| ✔                    	|
| Soccer             	| Ekstraklasa - Poland                	| soccer_poland_ekstraklasa                  	| ✔                    	|
| Soccer             	| Primeira Liga - Portugal            	| soccer_portugal_primeira_liga              	| ✔                    	|
| Soccer             	| La Liga - Spain                     	| soccer_spain_la_liga                       	| ✔                    	|
| Soccer             	| La Liga 2 - Spain                   	| soccer_spain_segunda_division              	| ✔                    	|
| Soccer             	| Premiership - Scotland              	| soccer_spl                                 	| ✔                    	|
| Soccer             	| Allsvenskan - Sweden                	| soccer_sweden_allsvenskan                  	| ✔                    	|
| Soccer             	| Superettan - Sweden                 	| soccer_sweden_superettan                   	| ✔                    	|
| Soccer             	| Swiss Superleague                   	| soccer_switzerland_superleague             	| ✔                    	|
| Soccer             	| Turkey Super League                 	| soccer_turkey_super_league                 	| ✔                    	|
| Soccer             	| UEFA Europa Conference League       	| soccer_uefa_europa_conference_league       	| ✔                    	|
| Soccer             	| UEFA Champions League               	| soccer_uefa_champs_league                  	| ✔                    	|
| Soccer             	| UEFA Champions League Qualification 	| soccer_uefa_champs_league_qualification    	| ✔                    	|
| Soccer             	| UEFA Europa League                  	| soccer_uefa_europa_league                  	| ✔                    	|
| Soccer             	| UEFA Euro 2024                      	| soccer_uefa_european_championship          	| ✔                    	|
| Soccer             	| UEFA Euro Qualification             	| soccer_uefa_euro_qualification             	| ✔                    	|
| Soccer             	| UEFA Nations League                 	| soccer_uefa_nations_league                 	|                      	|
| Soccer             	| Copa América                        	| soccer_conmebol_copa_america               	| ✔                    	|
| Soccer             	| Copa Libertadores                   	| soccer_conmebol_copa_libertadores          	| ✔                    	|
| Soccer             	| MLS                                 	| soccer_usa_mls                             	| ✔                    	|
| Tennis             	| ATP Australian Open                 	| tennis_atp_aus_open_singles                	|                      	|
| Tennis             	| ATP Canadian Open                   	| tennis_atp_canadian_open                   	|                      	|
| Tennis             	| ATP China Open                      	| tennis_atp_china_open                      	|                      	|
| Tennis             	| ATP Cincinnati Open                 	| tennis_atp_cincinnati_open                 	|                      	|
| Tennis             	| ATP French Open                     	| tennis_atp_french_open                     	|                      	|
| Tennis             	| ATP Paris Masters                   	| tennis_atp_paris_masters                   	|                      	|
| Tennis             	| ATP Shanghai Masters                	| tennis_atp_shanghai_masters                	|                      	|
| Tennis             	| ATP US Open                         	| tennis_atp_us_open                         	|                      	|
| Tennis             	| ATP Wimbledon                       	| tennis_atp_wimbledon                       	|                      	|
| Tennis             	| WTA Australian Open                 	| tennis_wta_aus_open_singles                	|                      	|
| Tennis             	| WTA Canadian Open                   	| tennis_wta_canadian_open                   	|                      	|
| Tennis             	| WTA China Open                      	| tennis_wta_china_open                      	|                      	|
| Tennis             	| WTA Cincinnati Open                 	| tennis_wta_cincinnati_open                 	|                      	|
| Tennis             	| WTA French Open                     	| tennis_wta_french_open                     	|                      	|
| Tennis             	| WTA US Open                         	| tennis_wta_us_open                         	|                      	|
| Tennis             	| WTA Wimbledon                       	| tennis_wta_wimbledon                       	|                      	|
| Tennis             	| WTA Wuhan Open                      	| tennis_wta_wuhan_open                      	|                      	|

```py
import argparse

import requests


# Obtain the api key that was passed in from the command line
parser = argparse.ArgumentParser(description='Sample V4')
parser.add_argument('--api-key', type=str, default='')
args = parser.parse_args()


# An api key is emailed to you when you sign up to a plan
# Get a free API key at https://api.the-odds-api.com/
API_KEY = args.api_key or 'YOUR_API_KEY'

# Sport key
# Find sport keys from the /sports endpoint below, or from https://the-odds-api.com/sports-odds-data/sports-apis.html
# Alternatively use 'upcoming' to see the next 8 games across all sports
SPORT = 'upcoming'

# Bookmaker regions
# uk | us | us2 | eu | au. Multiple can be specified if comma delimited.
# More info at https://the-odds-api.com/sports-odds-data/bookmaker-apis.html
REGIONS = 'us'

# Odds markets
# h2h | spreads | totals. Multiple can be specified if comma delimited
# More info at https://the-odds-api.com/sports-odds-data/betting-markets.html
# Note only featured markets (h2h, spreads, totals) are available with the odds endpoint.
MARKETS = 'h2h,spreads'

# Odds format
# decimal | american
ODDS_FORMAT = 'decimal'

# Date format
# iso | unix
DATE_FORMAT = 'iso'

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
#
# First get a list of in-season sports
#   The sport 'key' from the response can be used to get odds in the next request
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

sports_response = requests.get('https://api.the-odds-api.com/v4/sports', params={
    'api_key': API_KEY
})


if sports_response.status_code != 200:
    print(f'Failed to get sports: status_code {sports_response.status_code}, response body {sports_response.text}')

else:
    print('List of in season sports:', sports_response.json())



# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
#
# Now get a list of live & upcoming games for the sport you want, along with odds for different bookmakers
# This will deduct from the usage quota
# The usage quota cost = [number of markets specified] x [number of regions specified]
# For examples of usage quota costs, see https://the-odds-api.com/liveapi/guides/v4/#usage-quota-costs
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

odds_response = requests.get(f'https://api.the-odds-api.com/v4/sports/{SPORT}/odds', params={
    'api_key': API_KEY,
    'regions': REGIONS,
    'markets': MARKETS,
    'oddsFormat': ODDS_FORMAT,
    'dateFormat': DATE_FORMAT,
})

if odds_response.status_code != 200:
    print(f'Failed to get odds: status_code {odds_response.status_code}, response body {odds_response.text}')

else:
    odds_json = odds_response.json()
    print('Number of events:', len(odds_json))
    print(odds_json)

    # Check the usage quota
    print('Remaining requests', odds_response.headers['x-requests-remaining'])
    print('Used requests', odds_response.headers['x-requests-used'])
```



---
## Development

Read the [CONTRIBUTING.md](CONTRIBUTING.md) file.



