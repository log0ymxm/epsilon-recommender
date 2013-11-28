from django.core.management.base import BaseCommand, CommandError
from bs4 import BeautifulSoup
import urllib2
import time

from recommender.models import VideoGame

games_list_url = 'http://www.ign.com/games/all-ajax?startIndex=%i'

class Command(BaseCommand):
    help = 'IGN scraper pass one, let\'s populate our games using their game index pages'

    def handle(self, *args, **options):
        i = 0
        scraping = True

        while scraping:
            usock = urllib2.urlopen(games_list_url % i)
            data = usock.read()
            usock.close()

            if 'No Results.' in data:
                scraping = False
                continue

            soup = BeautifulSoup(data)
            game_links = soup.find_all('a')

            self.stdout.write("We found %s games on offset %s" % (len(game_links), i))
            for link in game_links:
                v, created = VideoGame.objects.get_or_create(ign_url=link.get('href'))
                if created:
                    self.stdout.write('New link: %s' % link.get('href'))

            seconds = 3
            self.stdout.write('Sleeping for %s seconds' % seconds)
            time.sleep(seconds)
            i += 50
