# IGN Notes

http://www.ign.com/xbox-360
http://www.ign.com/xbox-one
http://www.ign.com/ps3
http://www.ign.com/ps4
http://www.ign.com/wii-u
http://www.ign.com/pc
http://www.ign.com/ps-vita
http://www.ign.com/ds
http://www.ign.com/wireless

Scratch that, here's a list of all their games, and the ajax method to pull them quickly

http://www.ign.com/games
http://www.ign.com/games/all-ajax?startIndex=150

## Scraping

    # will parse the IGN game index create a video game for each url it finds
    ./manage.py 001_scrape_games_list

    # will iterate all non-scraped video games in the database and pull info from their ign_url
    ./manage.py 002_populate_game_details
