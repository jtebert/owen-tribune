# Owen Tribune
*The Owen Tribune, tremendous news source*

This is a news/magazine/blog backend and template. The design is heavily inspired by *The New Yorker* and *The New York Times*. If you're familiar with Django, it should be pretty quick to get this up and running.

## Setup (Ubuntu Linux):

- Install system packages: `sudo apt install libpq-dev postgresql python3-dev python3-venv`
- Create a virtual environment: `python3 -m venv venv`
- Activate the virtual environment: `source venv/bin/activate` (deactivate with `deactivate`)
- Install python packages: `pip3 install wheel; pip3 install -r requirements.txt`
- Start postgresql (if not already running): `sudo service postgresql start`
- Create database (`tribune_db`):
  - Run as postgres user: `sudo -i -u postgres`
  - Create database: `createdb tribune_db`
  - Get out: `exit`
- Create configuration file in the root folder of the project called `settings.ini`
	```
	[settings]
	DEBUG=True
	SECRET_KEY=ARANDOMKEY
	```
	There are additional settings that can be configured for production. (Search for `config(` in settings.py)
- Run migrations: `python3 manage.py migrate`
- Create superuser: `python3 manage.py createsuperuser`
- Run it: `python3 manage.py runserver`

You'll also have to set up a postgres database. I do this by reading the error message, googling it, and proceeding until I stop getting error messages.

In development, static and media files are served from local folders. In production, they will be served from Amazon S3. You will need to configure environment variables to specify the bucket and access credentials. (See `tribune/settings/production.py` for details.)

### Possibly necessary steps (if not previously set up)

- Create a postgres user: `sudo -u createuser YOUR_USERNAME`

## Features:

- Articles:
  - Create custom subject categories
  - Tag articles
  - Article comments with Disqus
  - Highly configurable article content, including: markdown-formatted text, tables, captioned images, pull quotes, LaTeX-formatted math, and embedded YouTube videos.
  - Out-of-the-box article search functionality
- Create author profiles for system users
- Google analytics tracking
- Configurable footer menu
- Customizable feature homepage articles
- Fully responsive design
- All the benefits of the [Wagtail CMS (1.13)](https://wagtail.io/)
