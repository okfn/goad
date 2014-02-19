# GOAD - A Badging Server

Goad is a small [OpenBadges](http://openbadges.org) badging server built
for the [Open Knowledge Foundation](http://okfn.org).

Check it out at
[badges.schoolofdata.org](http://badges.schoolofdata.org)

## Features

* API to issue Badges from within Programs
* Simple Claim interface

## Contributing

Contributions are highly welcome. What you can do:

* Try it out and file issues
* Write documentation 
* Improve the Code - try to stick to ```pep8```
* Improve the design of templates 

## Setup

### Dependencies

* virtualenv
* python2
* [Django](http://djangoproject.com)

### Installation for development

Create a virtualenv then:

```
pip install -r requirements.dev.txt
```

### Initialize the database

```
DATABASE_URL=sqlite:///goad.sqlite python manage.py syncdb
DATABASE_URL=sqlite:///goad.sqlite python manage.py migrate 
```

### Run

```
DATABASE_URL=sqlite:///goad.sqlite honcho run
```

