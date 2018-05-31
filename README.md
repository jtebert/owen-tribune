# Owen Tribune
*The Owen Tribune, tremendous news source*

This is a news/magazine/blog backend and template. The design is heavily inspired by *The New Yorker* and *The New York Times*. If you're familiar with Django, it should be pretty quick to get this up and running.

## Setup:

- Install requirements: `pip install -r requirements.txt`
- Run migrations: `python manage.py migrate`
- Create superuser: `python manage.py createsuperuser`
- Run it: `python manage.py runserver`

You'll also have to set up a postgres database. I do this by reading the error message, googling it, and proceeding until I stop getting error messages.

In development, static and media files are served from local folders. In production, they will be served from Amazon S3. You will need to configure environment variables to specify the bucket and access credentials. (See `owen/settings/production.py` for details.)

### Possibly necessary steps (if not previously set up)

- Install postgresql (on Ubuntu: `sudo apt install libpq-dev postgresql`)

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
