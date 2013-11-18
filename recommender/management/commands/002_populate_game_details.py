from django.core.management.base import BaseCommand, CommandError
from django.utils.encoding import smart_str
from django.db import IntegrityError
from bs4 import BeautifulSoup
from django.template.defaultfilters import slugify
import urllib2
import time
import datetime

from recommender.models import VideoGame, Platform, Feature, Specification, Genre, Company

ign_base_url = 'http://www.ign.com%s'

class Command(BaseCommand):
    help = 'IGN scraper pass one, let\'s populate our games using their game index pages'

    def debug(self, header, obj):
        self.stdout.write('--- %s: %s' % (header, obj))

    def handle(self, *args, **options):
        games = VideoGame.objects.filter(ign_url__isnull=False,
                                         ign_image__isnull=True
                                         ).order_by('?')
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
            game.slug=slugify(title)
            game.description=description
            game.ign_image = soup.find(attrs={'property': 'og:image'}).get('content')

            platforms = soup.find(class_="contentPlatformsText").find_all('span')


            if platforms[0]:
                platform = platforms[0].a
                platform = smart_str(platform.string)
                print 'this is the platform', platform
                try:
                    p, created = Platform.objects.get_or_create(name=platform
                                                                ,slug=slugify(platform))
                except IntegrityError:
                    p = Platform.objects.get(name=platform)
                    p.slug = slugify(platform)
                    p.save()
                game.platforms.add(p)

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

            ign_rating = soup.find(class_="ignRating")
            if ign_rating:
                game.ign_rating = ign_rating.find(class_="ratingValue").string

            ign_community_rating = soup.find(class_="communityRating")
            if ign_community_rating:
                ign_community_rating = ign_community_rating.find(class_="ratingValue").string
            if ign_community_rating:
                game.ign_community_rating = ign_community_rating.strip()

            ign_community_rating_count = soup.find(class_="communityRating")
            if ign_community_rating_count:
                ign_community_rating_count = ign_community_rating_count.find(class_="ratingCount")
            if ign_community_rating_count:
                game.ign_community_rating_count = ign_community_rating_count.b.string

            ign_articlesubHeadline = soup.find(class_="articlesubHeadline")
            if ign_articlesubHeadline:
                game.ign_subheadline = ign_articlesubHeadline.find(class_="text").string

            ign_wiki_edits = soup.find(class_="wikiEditCount")
            if ign_wiki_edits:
                game.ign_wiki_edits = ign_wiki_edits.string.replace(' Edits', '')

            summary = soup.find(id="summary").find(class_="gameInfo").find_all('p')
            for i in range(len(summary)):
                summary_string = summary[i].string
            # TODO
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

            # TODO
            leftColumn_divs = soup.find(class_="gameInfo-list leftColumn").find_all('div')

            gameInfo_list = soup.find_all(class_="gameInfo-list")

            if len(gameInfo_list) > 1:
                genre = gameInfo_list[1]
                if genre:
                    genre = genre.find_all('div')[0].a.string.strip()
                    try:
                        g, created = Genre.objects.get_or_create(name=genre
                                                                    ,slug=slugify(genre))
                    except IntegrityError:
                        g = Genre.objects.get(name=genre)
                        g.slug = slugify(genre)
                        g.save()
                    game.genre = g

            if len(gameInfo_list) > 1:
                publisher = gameInfo_list[1].find_all('div')
                if len(publisher) > 1:
                    publisher = publisher[1].a.string.strip()
                    try:
                        p, created = Company.objects.get_or_create(name=publisher, slug=slugify(publisher))
                    except IntegrityError:
                        p = Company.objects.get(name=publisher)
                        p.slug = slugify(publisher)
                        p.save()
                    game.publisher.add(p)

            if len(gameInfo_list) > 1:
                publisher_url = gameInfo_list[1].find_all('div')
                if len(publisher_url) > 1:
                    publisher_url = publisher_url[1].a.get('href')
                    if p:
                      p.url = publisher_url
                      p.save()

            if len(gameInfo_list) > 1:
                developer = gameInfo_list[1].find_all('div')
                if len(developer) > 2:
                    developer = developer[2].a.string.strip()
                    try:
                        d, created = Company.objects.get_or_create(name=developer, slug=slugify(developer))
                    except IntegrityError:
                        d = Company.objects.get(name=developer)
                        d.slug = slugify(developer)
                        d.save()
                    game.developer.add(d)

            if len(gameInfo_list) > 1:
                developer_url = gameInfo_list[1].find_all('div')
                if len(developer_url) > 2:
                    developer_url = developer_url[2].a.get('href')
                    if d:
                      d.url = developer_url
                      d.save()

            features = soup.find(class_="featureList")
            if features:
                features = features.find_all('li')
                for i in range(len(features)):
                    f = smart_str(features[i].string)
                    feature, c = Feature.objects.get_or_create(name=f)
                    game.features.add(feature)

            specifications = soup.find(id="specifications")
            if specifications:
                specifications = specifications.find_all('li')
                for i in range(len(specifications)):
                    name = specifications[i]
                    if name.strong:
                        name = smart_str(name.strong.string)
                    elif name.string:
                        name = smart_str(name.string.strip())

                    try:
                        s, created = Specification.objects.get_or_create(name=name)
                    except IntegrityError:
                        s = Specification.objects.get(name=name)
                        s.slug = slugify(name)
                        s.save()
                    game.specifications.add(s)

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

            seconds = 3
            self.stdout.write('Sleeping for %s seconds' % seconds)
            time.sleep(seconds)
