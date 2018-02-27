# owen-tribune
The Owen Tribune, tremendous news source

## Setup:

- Run migrations: `python manage.py migrate`
- Create superuser: `python manage.py createsuperuser`
- Run it: `python manage.py runserver`

You'll also have to set up a postgres database. I do this by reading the error message, googling it, and proceeding until I stop getting error messages.

## Features:

- CMS backend built on Wagtail
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
