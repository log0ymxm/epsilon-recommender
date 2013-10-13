
## Conventions

### Commas - when in doubt add another comma

It's common practice in Python to leave extra commas, you'll see things like

    item = ('something',)

    # or
    items = (
             ('a', 'few', 'things',),
             ('more', 'things',),
            )

In the first example the extra comma ensures that we want a tuple of strings, and not a tuple of characters, 's' 'o' 'm' 'e'... etc. Most the time for lists and tuples it's best to leave that trailing comma, as not having it can at times lead to unintended effects.
