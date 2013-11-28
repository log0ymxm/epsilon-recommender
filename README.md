## Setting up a development environment

Installing and creating the database. We'll use postgres in production. Here are the commands to set this up on an Ubunut linux machine. On OSX or Windows you'll have to visit the postgres site and find an installer.

    # ubuntu only
    sudo apt-get install postgres pgadmin3
    sudo apt-get install libatlas-base-dev gfortran
    sudo apt-get install graphviz
    sudo apt-get install libgraphviz-dev
    sudo apt-get install graphviz-dev

    # running the psql command as the postgres user, we will
    # execute SQL to create our db user, and project database
    sudo -u postgres psql -c "CREATE USER epsilon WITH PASSWORD '1SnEAizt07np4mawMYOsWrP7cwQowSRuZA64CAo9lj';"
    sudo -u postgres psql -c "CREATE DATABASE epsilon_recommender;"
    sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE epsilon_recommender TO epsilon;"

Setting up the project for local development

    # Create & use a virtual python environment
    sudo easy_install virtualenv
    virtualenv venv
    source venv/bin/activate

    # Install dependencies
    pip install numpy==1.7.1
    pip install scipy==0.12.0
    pip install -r requirements.txt

    # Setup database
    ./manage.py syncdb
    ./manage.py migrate recommender # run our migrations first
    ./manage.py migrate # run all migrations, includes any 3rd-party migrations
    ./manage.py createsuperuser

## Running in development

    # fetch any new changes, and rebase your changes cleanly
    git pull --rebase origin master

    # enter venv, migrate database, and start server
    source venv/bin/activate
    recomender/manage.py migrate
    recommender/manage.py runserver

## External Documentation

- [Python](http://docs.python.org/2/) - The language we're using
- [Virtual Env](http://www.virtualenv.org/en/latest/) - Tool for encapsulating your development work, and making it more portable
- [Pip](http://www.pip-installer.org/en/latest/) - The preferred package manager for python
- [Django Documentation Site](https://docs.djangoproject.com/en/1.5/) - The web framework (just a bunch of libraries)
- [South](http://south.readthedocs.org/en/latest/) - A tool for managing database changes in an agile project
- [Tastypie](http://django-tastypie.readthedocs.org/en/latest/) - Create a RESTful API from any django model
- [Django-ratings](https://github.com/dcramer/django-ratings) - Let's us easily use star ratings in our project
- [Django-recommends](http://django-recommends.readthedocs.org/en/latest/) - Plugin for abstracting how recommendations are done
- [Django-attributes](https://github.com/powellc/django-attributes) - Allows adding dynamic attributes to any model easily

- [SciKit Learn](http://scikit-learn.org/stable/documentation.html) - Machine Learning libraries for python
- [Python Recsys](https://github.com/ocelma/python-recsys) - Recommendation library that uses a support vector machine under the scenes

- [Twitter Bootstrap](http://getbootstrap.com/) - CSS & JS files to simplify front-end layouts, and presentation
- [jQuery](http://api.jquery.com/) - Javascript library for simplifying DOM access, and other common js things
- [Angular JS](http://angularjs.org/) - Javascript framework for easing data binding, and structuring a js app

- [Github](https://help.github.com/) - Git hosting, with some great documentation
