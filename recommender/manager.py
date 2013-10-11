from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class CustomUserManager(BaseUserManager):
    def get_twitter_user_info(self, screen_name):
        # TODO
        MY_TWITTER_CREDS = os.path.expanduser('~/.my_app_credentials')
        if not os.path.exists(MY_TWITTER_CREDS):
            oauth_dance("Fast Food Friday Test App", settings.TWITTER_CONSUMER_KEY, settings.TWITTER_CONSUMER_SECRET,
                    MY_TWITTER_CREDS)

        oauth_token, oauth_secret = read_token_file(MY_TWITTER_CREDS)

        t = Twitter(
            auth=OAuth(oauth_token, oauth_secret,
                       settings.TWITTER_CONSUMER_KEY, settings.TWITTER_CONSUMER_SECRET)
           )
        lookup = t.users.lookup(screen_name=screen_name, _timeout=1)

        return lookup[0]

    def create_user(self, email, screen_name, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        twitter_info = self.get_twitter_user_info(screen_name)
        #print twitter_info

        user = self.model(
            email=PSUserManager.normalize_email(email),
            twitter_id=twitter_info['id'],
            verified=twitter_info['verified'],
            profile_image_url=twitter_info['profile_image_url'],
            profile_sidebar_fill_color=twitter_info['profile_sidebar_fill_color'],
            profile_text_color=twitter_info['profile_text_color'],
            followers_count=twitter_info['followers_count'],
            profile_sidebar_border_color=twitter_info['profile_sidebar_border_color'],
            profile_background_color=twitter_info['profile_background_color'],
            listed_count=twitter_info['listed_count'],
            profile_background_image_url=twitter_info['profile_background_image_url'],
            utc_offset=twitter_info['utc_offset'],
            statuses_count=twitter_info['statuses_count'],
            description=twitter_info['description'],
            friends_count=twitter_info['friends_count'],
            location=twitter_info['location'],
            profile_link_color=twitter_info['profile_link_color'],
            geo_enabled=twitter_info['geo_enabled'],
            name=twitter_info['name'],
            lang=twitter_info['lang'],
            profile_background_tile=twitter_info['profile_background_tile'],
            favourites_count=twitter_info['favourites_count'],
            screen_name=twitter_info['screen_name'],
            url=twitter_info['url'],
            created_at=parse_twitter_date(twitter_info['created_at']),
            time_zone=twitter_info['time_zone']
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, screen_name, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(email,
            screen_name=screen_name,
            password=password,
        )
        user.is_active = True
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
