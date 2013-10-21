from django.core.management.base import BaseCommand, CommandError
from bs4 import BeautifulSoup
import urllib2
import time

from recommender.models import VideoGame

ign_base_url = 'http://www.ign.com%s'


class Command(BaseCommand):
    help = 'IGN scraper pass one, let\'s populate our games using their game index pages'

    def debug(self, header, obj):
        self.stdout.write('--- %s: %s' % (header, obj))

    def handle(self, *args, **options):
        games = VideoGame.objects.filter(ign_url__isnull=False,
                                         description='')
        self.stdout.write('Games to scrape: %s' % len(games))

        for i in range(len(games)):
            game = games[i]
            self.stdout.write('--------------------------------------------------')
            self.stdout.write('Scraping url: %s' % game.ign_url)
            self.stdout.write('--------------------------------------------------')
            usock = urllib2.urlopen(ign_base_url % game.ign_url)
            data = usock.read()
            usock.close()

            self.stdout.write("Response length: %s" % len(data))
            self.stdout.write('----------')

            soup = BeautifulSoup(data)

            title = soup.find(class_='contentTitle').a.string.strip()
            self.debug('title', title)

            ign_image = soup.find(attrs={'property': 'og:image'}).get('content')
            self.debug('ign_image', ign_image)

            description = soup.find(attrs={'property': 'og:description'}).get('content')
            self.debug('description', description)

            platforms = soup.find(class_="contentPlatformsText").find_all('span')
            for i in range(len(platforms)):
                platforms[i] = platforms[i].a.string
            self.debug('platforms', platforms)

            release_date = soup.find(class_="releaseDate").strong.string
            self.debug('release', release_date)

            ign_rating = soup.find(class_="ignRating").find(class_="ratingValue").string
            self.debug('ign_rating', ign_rating)

            ign_community_rating = soup.find(class_="communityRating").find(class_="ratingValue").string
            if ign_community_rating:
                ign_community_rating = ign_community_rating.strip()
            self.debug('ign_community_rating', ign_community_rating)

            ign_community_rating_count = soup.find(class_="communityRating").find(class_="ratingCount")
            if ign_community_rating_count:
                ign_community_rating_count = ign_community_rating_count.b.string
            self.debug('ign_community_rating_count', ign_community_rating_count)

            ign_articlesubHeadline = soup.find(class_="articlesubHeadline")
            #self.debug('ign_articlesubHeadline', ign_articlesubHeadline)
            if ign_articlesubHeadline:
                ign_subheadline = ign_articlesubHeadline.find(class_="text").string
            else:
                ign_subheadline = None
            self.debug('ign_subheadline', ign_subheadline)

            ign_wiki_edits = soup.find(class_="wikiEditCount").string.replace(' Edits', '')
            self.debug('ign_wiki_edits', ign_wiki_edits)

            summary = soup.find(id="summary").find(class_="gameInfo").find_all('p')
            self.debug('summary len', len(summary))
            for i in range(len(summary)):
                self.debug('summary[i]', summary[i])
                summary_string = summary[i].string
                self.debug('summary[i] string', summary[i])
                self.debug('sum[i] string type', type(summary_string))
                #summary[i] = summary[i].string.strip()
            self.debug('summary p', summary)

            # TODO maturity rating
            #summary_section = soup.find(id="summary")
            #self.debug('summary_section', summary_section)
            #if summary:
            #    game_info_section = summary.find(class_="gameInfo")
            #    self.debug('game_info_section', game_info_section)
            #    if game_info_section:
            #        maturity_rating = game_info_section.find('p').a.get('href')
            #    else:
            #        maturity_rating = None
            #else:
            #    maturity_rating = None
            #self.debug('maturity_rating', maturity_rating)

            # TODO
            leftColumn_divs = soup.find(class_="gameInfo-list leftColumn").find_all('div')
            self.debug('leftColumn_divs', leftColumn_divs)
            #self.debug('leftColumn_divs len', len(leftColumn_divs))
            #if len(leftColumn_divs[0].find_all('div')) > 1:
            #    divs = leftColumn_divs[0].find_all('div')
            #    self.debug('leftColunmn divs', divs)
            #if len(leftColumn_divs) > 1:
            #    divs = leftColumn_divs[1].find_all('div')
            #    self.debug('leftColunmn divs', leftColumn_divs[1])
            #    self.debug('leftColunmn divs', divs)
            #    rating_notes = divs[1].string
            #    self.debug('rating_notes', rating_notes)

            gameInfo_list = soup.find_all(class_="gameInfo-list")
            #self.debug('gameInfo_list', gameInfo_list[1].find_all('div')[0])
            genre = gameInfo_list[1].find_all('div')[0].a.string.strip()
            self.debug('genre', genre)

            publisher = gameInfo_list[1].find_all('div')[1].a.string.strip()
            self.debug('publisher', publisher)

            publisher_url = gameInfo_list[1].find_all('div')[1].a.get('href')
            self.debug('publisher_url', publisher_url)

            developer = gameInfo_list[1].find_all('div')[2].a.string.strip()
            self.debug('developer', developer)

            developer_url = gameInfo_list[1].find_all('div')[2].a.get('href')
            self.debug('developer_url', developer_url)

            # TODO features
            features = soup.find(class_="featureList")
            self.debug('features', features)

            specifications = soup.find(id="specifications")
            if specifications:
                specifications = specifications.find_all('li')
                for i in range(len(specifications)):
                    if specifications[i].strong:
                        specifications[i] = specifications[i].strong.string
                    else:
                        specifications[i] = specifications[i].string.strip()
            self.debug('specifications', specifications)

            ign_games_you_may_like = soup.find_all(class_='gamesYouMayLike-game')
            self.debug('ign_games_you_may_like', ign_games_you_may_like)

            # TODO create all attributes & modify videogame model with appropriate fields
            # --- PE NOTE we may want to reduce the use of seperate attributes for simplicity
            #     and efficiency. We can just create appropriate fields on the video game model.

            # TODO save the game

            if i > 10:
                break
            # Break for now while debugging the scraper

            seconds = 10
            self.stdout.write('Sleeping for %s seconds' % seconds)
            time.sleep(seconds)
