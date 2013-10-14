## Migration Files

The migration files are in the app directory under migrations. I.E. `recommender/migrations`

Most of them are automatically generated though it's simple to write your own for more complex changes & updates.

## Automatically Generating Migrations For Model Changes

    ./manage.py schemamigration recommender --auto

## Data Migrations

    ./manage.py datamigration recommender migration-name-here

## Running Migrations

    ./manage.py migrate
    ./manage.py migrate app-name
    ./manage.py migrate app-name 0001-migration-name

## Skipping A Migration That May Have Run Already

    ./manage.py migrate recommender 0001 --fake
