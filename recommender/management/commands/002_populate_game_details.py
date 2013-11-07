from django.core.management.base import BaseCommand, CommandError
from django.utils.encoding import smart_str
from bs4 import BeautifulSoup
import urllib2
import time
import datetime

from recommender.models import VideoGame, Platform, Feature, Specification

ign_base_url = 'http://www.ign.com%s'

class Command(BaseCommand):
    help = 'IGN scraper pass one, let\'s populate our games using their game index pages'

    def debug(self, header, obj):
        self.stdout.write('--- %s: %s' % (header, obj))

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
            print 'game id', game.id

            soup = BeautifulSoup(data)

            title = soup.find(class_='contentTitle').a.string.strip()
            description = soup.find(attrs={'property': 'og:description'})
            if description:
                description = description.get('content')
            else:
                description = ''

            game.name=title
            game.description=description
            game.ign_image = soup.find(attrs={'property': 'og:image'}).get('content')

            platforms = soup.find(class_="contentPlatformsText").find_all('span')
            #self.debug('platforms len', len(platforms))
            for i in range(len(platforms)):
                platform = platforms[i].a
                if platform:
                    platform = smart_str(platform.string)
                    p, created = Platform.objects.get_or_create(name=platform)
                    #print '---', p, created
                    game.platforms.add(p)

            ####
            release_date = soup.find(class_="releaseDate")
            if release_date:
                release_date = smart_str(release_date.strong.string)
                try:
                    release_date = datetime.datetime.strptime(release_date, "%B %d, %Y")
                except ValueError:
                    pass
                if isinstance(release_date, basestring):
                    try:
                        release_date = datetime.datetime.strptime(release_date, "%B %Y")
                    except ValueError:
                        pass
                if isinstance(release_date, basestring):
                    try:
                        release_date = datetime.datetime.strptime(release_date, "%Y")
                    except ValueError:
                        pass
                if isinstance(release_date, basestring):
                    game.release_date_malformed = release_date
                    release_date = None

            if release_date:
                game.release_date = release_date

            ###
            ign_rating = soup.find(class_="ignRating")
            if ign_rating:
                game.ign_rating = ign_rating.find(class_="ratingValue").string

            ###
            ign_community_rating = soup.find(class_="communityRating")
            if ign_community_rating:
                ign_community_rating = ign_community_rating.find(class_="ratingValue").string
            if ign_community_rating:
                game.ign_community_rating = ign_community_rating.strip()

            ###
            ign_community_rating_count = soup.find(class_="communityRating")
            if ign_community_rating_count:
                ign_community_rating_count = ign_community_rating_count.find(class_="ratingCount")
            if ign_community_rating_count:
                game.ign_community_rating_count = ign_community_rating_count.b.string
                print 'len', game.ign_community_rating_count

            ###
            ign_articlesubHeadline = soup.find(class_="articlesubHeadline")
            #self.debug('ign_articlesubHeadline', ign_articlesubHeadline)
            if ign_articlesubHeadline:
                game.ign_subheadline = ign_articlesubHeadline.find(class_="text").string

            ###
            ign_wiki_edits = soup.find(class_="wikiEditCount")
            if ign_wiki_edits:
                game.ign_wiki_edits = ign_wiki_edits.string.replace(' Edits', '')

            ### TODO
            summary = soup.find(id="summary").find(class_="gameInfo").find_all('p')
            #self.debug('summary len', len(summary))
            for i in range(len(summary)):
                #self.debug('summary[i]', summary[i])
                summary_string = summary[i].string
                #self.debug('summary[i] string', summary[i])
                #self.debug('sum[i] string type', type(summary_string))
                #summary[i] = summary[i].string.strip()
            #game.summary = summary

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
            #self.debug('leftColumn_divs', leftColumn_divs)
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
            #self.debug('gameInfo_list', gameInfo_list[1].find_all('div')[0])
            print '-----'

            if len(gameInfo_list) > 1:
                game.genre = gameInfo_list[1].find_all('div')[0].a.string.strip()

            ###
            if len(gameInfo_list) > 1:
                publisher = gameInfo_list[1].find_all('div')
                if len(publisher) > 1:
                    publisher = publisher[1].a.string.strip()
                    game.publisher = publisher

            ###
            if len(gameInfo_list) > 1:
                publisher_url = gameInfo_list[1].find_all('div')
                if len(publisher_url) > 1:
                    publisher_url = publisher_url[1].a.get('href')
                    game.publisher_url = publisher_url

            ###
            if len(gameInfo_list) > 1:
                developer = gameInfo_list[1].find_all('div')
                if len(developer) > 2:
                    developer = developer[2].a.string.strip()
                    game.developer = developer

            ###
            if len(gameInfo_list) > 1:
                developer_url = gameInfo_list[1].find_all('div')
                if len(developer_url) > 2:
                    developer_url = developer_url[2].a.get('href')
                    game.developer_url

            ###
            # TODO features
            features = soup.find(class_="featureList")
            #print '--- features', features
            if features:
                features = features.find_all('li')
                for i in range(len(features)):
                    f = smart_str(features[i].string)
                    print '--- f', f
                    feature, c = Feature.objects.get_or_create(name=f)
                    try:
                        print '--- feature', feature, c
                    except:
                        pass
                    game.features.add(feature)

            ###
            specifications = soup.find(id="specifications")
            #print '--- specifications', specifications
            if specifications:
                specifications = specifications.find_all('li')
                for i in range(len(specifications)):
                    name = specifications[i]
                    print '--- spec', name
                    if name.strong:
                        name = smart_str(name.strong.string)
                    elif name.string:
                        name = smart_str(name.string.strip())

                    s, created = Specification.objects.get_or_create(name=name)
                    print '--- s', s, created
                    game.specifications.add(s)

            ###
            ign_games_you_may_like = soup.find_all(class_='gamesYouMayLike-game')
            if ign_games_you_may_like:
                for i in range(len(ign_games_you_may_like)):
                    game_you_may_like = ign_games_you_may_like[i]
                    related_game_url = game_you_may_like.find('a').get('href').replace('http://www.ign.com', '')
                    related_game, c = VideoGame.objects.get_or_create(
                        ign_url=related_game_url
                        )
                    game.ign_games_you_may_like.add(related_game)

            print '--- game', game.__dict__

            game.save()

            #if i > 10:
            #    break

            seconds = 3
            self.stdout.write('Sleeping for %s seconds' % seconds)
            time.sleep(seconds)
