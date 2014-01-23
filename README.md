# GOAD - A Badging Server

Goad is a small [OpenBadges](http://openbadges.org) badging server built
for the [Open Knowledge Foundation](http://okfn.org).

Check it out at
[badges.schoolofdata.org](http://badges.schoolofdata.org)

## Features

* API to issue Badges from within Programs
* Simple Claim interface

## Setup

### Dependencies

* [Foreman](http://theforeman.org/)
* [Django](http://djangoproject.com)

### Install

Create a virtualenv then:

```
pip install -r requirements.txt
```

### Initialize the database

```
DATABASE_URL=<dburl> python manage.py syncdb
DATABASE_URL=<dburl> python manage.py migrate okbadger --fake
```

*dburl* can be something like: sqlite://test.sqlite

### Run

```
foreman start
```


## Contributing

Contributions are highly welcome. What you can do:

* Try it out and file issues
* Write documentation 
* Improve the Code - try to stick to ```pep8```
* Improve the design of templates 

