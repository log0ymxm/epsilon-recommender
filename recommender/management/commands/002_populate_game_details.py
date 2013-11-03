from django.core.management.base import BaseCommand, CommandError
from django.utils.encoding import smart_str
from bs4 import BeautifulSoup
import urllib2
import time

from recommender.models import VideoGame, VideoGameAttribute
from attributes.models import AttributeOption

ign_base_url = 'http://www.ign.com%s'

class Command(BaseCommand):
    help = 'IGN scraper pass one, let\'s populate our games using their game index pages'

    def debug(self, header, obj):
        self.stdout.write('--- %s: %s' % (header, obj))

    def store_attribute(self, video_game, value, description, name,
                        validation='attributes.utils.validation_simple'):
        print 'store_attribute'
        if True:
            self.debug(name, value)
        option, created = AttributeOption.objects.get_or_create(
            description=description,
            name=name,
            validation=validation
            )
        if created:
            self.debug('- option created -', option)
        attribute, created = VideoGameAttribute.objects.get_or_create(
            value=smart_str(value),
            option=option,
            video_game=video_game
            )
        if created:
            self.debug('- attribute created -', attribute)

    def handle(self, *args, **options):
        games = VideoGame.objects.filter(ign_url__isnull=False)
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
            description = soup.find(attrs={'property': 'og:description'})
            if description:
                description = description.get('content')
            else:
                description = ''


            game.name=title
            game.description=description

            self.debug('title', title)
            self.debug('description', description)

            ###
            ign_image = soup.find(attrs={'property': 'og:image'}).get('content')
            self.store_attribute(game, ign_image, 'IGN Image', 'ign_image')

            ###
            platforms = soup.find(class_="contentPlatformsText").find_all('span')
            self.debug('platforms len', len(platforms))
            for i in range(len(platforms)):
                platform = platforms[i].a
                if platform:
                    platform = platform.string
                    self.store_attribute(game, platform, 'Platform', 'platform')

            ###
            release_date = soup.find(class_="releaseDate")
            if release_date:
                release_date = release_date.strong.string
                self.store_attribute(game, release_date, 'Release Date', 'release_date')

            ###
            ign_rating = soup.find(class_="ignRating")
            if ign_rating:
                ign_rating = ign_rating.find(class_="ratingValue").string
                self.store_attribute(game, ign_rating, 'IGN Rating', 'ign_rating')

            ###
            ign_community_rating = soup.find(class_="communityRating")
            if ign_community_rating:
                ign_community_rating = ign_community_rating.find(class_="ratingValue").string
            if ign_community_rating:
                ign_community_rating = ign_community_rating.strip()
                self.store_attribute(game, ign_community_rating, 'IGN Community Rating', 'ign_community_rating')

            ###
            ign_community_rating_count = soup.find(class_="communityRating")
            if ign_community_rating_count:
                ign_community_rating_count = ign_community_rating_count.find(class_="ratingCount")
            if ign_community_rating_count:
                ign_community_rating_count = ign_community_rating_count.b.string
                self.store_attribute(game, ign_community_rating_count, 'IGN Community Rating Count', 'ign_community_rating_count')

            ###
            ign_articlesubHeadline = soup.find(class_="articlesubHeadline")
            #self.debug('ign_articlesubHeadline', ign_articlesubHeadline)
            if ign_articlesubHeadline:
                ign_subheadline = ign_articlesubHeadline.find(class_="text").string
                self.store_attribute(game, ign_subheadline, 'IGN Sub-Headline', 'ign_subheadline')

            ###
            ign_wiki_edits = soup.find(class_="wikiEditCount")
            if ign_wiki_edits:
                ign_wiki_edits = ign_wiki_edits.string.replace(' Edits', '')
                self.store_attribute(game, ign_wiki_edits, 'Number of wiki edits for this game on IGN', 'ign_wiki_edits')

            ###
            summary = soup.find(id="summary").find(class_="gameInfo").find_all('p')
            self.debug('summary len', len(summary))
            for i in range(len(summary)):
                self.debug('summary[i]', summary[i])
                summary_string = summary[i].string
                self.debug('summary[i] string', summary[i])
                self.debug('sum[i] string type', type(summary_string))
                #summary[i] = summary[i].string.strip()
            self.store_attribute(game, summary, 'Summary', 'summary')

            ###
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
            #self.store_attribute(game, ign, '', '')
            #self.debug('maturity_rating', maturity_rating)

            ###
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

            ###
            gameInfo_list = soup.find_all(class_="gameInfo-list")
            self.debug('gameInfo_list', gameInfo_list[1].find_all('div')[0])
            print '-----'

            if len(gameInfo_list) > 1:
                genre = gameInfo_list[1].find_all('div')[0].a.string.strip()
                self.store_attribute(game, genre, 'Genre', 'genre')

            ###
            if len(gameInfo_list) > 1:
                publisher = gameInfo_list[1].find_all('div')
                if len(publisher) > 1:
                    publisher = publisher[1].a.string.strip()
                self.store_attribute(game, publisher, 'Publisher', 'publisher')

            ###
            if len(gameInfo_list) > 1:
                publisher_url = gameInfo_list[1].find_all('div')
                if len(publisher_url) > 1:
                    publisher_url = publisher_url[1].a.get('href')
                self.store_attribute(game, publisher_url, 'Publisher URL', 'publisher_url')

            ###
            if len(gameInfo_list) > 1:
                developer = gameInfo_list[1].find_all('div')
                if len(developer) > 2:
                    developer = developer[2].a.string.strip()
                self.store_attribute(game, developer, 'Developer', 'developer')

            ###
            if len(gameInfo_list) > 1:
                developer_url = gameInfo_list[1].find_all('div')
                if len(developer_url) > 2:
                    developer_url = developer_url[2].a.get('href')
                self.store_attribute(game, developer_url, 'Developer URL', 'developer_url')

            ###
            # TODO features
            features = soup.find(class_="featureList")
            self.store_attribute(game, features, 'Features', 'features')

            ###
            specifications = soup.find(id="specifications")
            if specifications:
                specifications = specifications.find_all('li')
                for i in range(len(specifications)):
                    if specifications[i].strong:
                        specifications[i] = specifications[i].strong.string
                    elif specifications[i].string:
                        specifications[i] = specifications[i].string.strip()
            self.store_attribute(game, specifications, 'Specifications', 'specifications')

            ###
            ign_games_you_may_like = soup.find_all(class_='gamesYouMayLike-game')
            self.store_attribute(game, ign_games_you_may_like, 'IGN Games You May Like', 'ign_games_you_may_like')

            game.save()

            #if i > 10:
            #    break

            seconds = 3
            self.stdout.write('Sleeping for %s seconds' % seconds)
            time.sleep(seconds)
