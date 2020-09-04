# Owen Tribune
*The Owen Tribune, tremendous news source*

This is a news/magazine/blog backend and template. The design is heavily inspired by *The New Yorker* and *The New York Times*. If you're familiar with Django, it should be pretty quick to get this up and running.

## Setup (Ubuntu Linux)

- Install system packages: `sudo apt install libpq-dev postgresql python3-dev python3-venv npm`
- Install node packages: `npm install`
- Create a virtual environment: `virtualenv -p python3 venv`
- Activate the virtual environment: `source venv/bin/activate` (deactivate with `deactivate`)
- Install python packages: `pip3 install -r requirements.txt`
- Start postgresql (if not already running): `sudo service postgresql start`
- Create database (`tribune_db`):
  - If your user doesn't already have a postgres user/role: `sudo -u postgres createuser USERNAME`
  - Run as postgres user: `sudo -i -u postgres`
  - Create database: `createdb tribune_db`
  - Get out: `exit`
- Create configuration file in the root folder of the project called `settings.ini`
	```
	[settings]
	DEBUG=True
	SECRET_KEY=A_RANDOM_KEY
  BASE_URL=127.0.0.1
	```
	There are additional settings that can be configured for production. (Search for `config(` in settings.py)
- Run migrations: `python3 manage.py migrate`
- Create superuser: `python3 manage.py createsuperuser`
- Run it: `python3 manage.py runserver`

You'll also have to set up a postgres database. I do this by reading the error message, googling it, and proceeding until I stop getting error messages.

In development, static and media files are served from local folders. In production, they will be served from Amazon S3. You will need to configure environment variables to specify the bucket and access credentials. (See `tribune/settings/production.py` for details.)

### Optional: Gulp setup (BrowserSync)

- Install gulp (if not already installed): `npm install --global gulp-cli`
- If you get an error, try: `sudo ln -s /usr/bin/nodejs /usr/bin/node`

## Creating your first site

- With the server running, open your browser to `localhost:8000/admin` and log in with the credentials you set above
- Create a home page
  - In the left menu, click "Pages," then click the "Pages" link at the top (with a house next to it.)
  - Click "Add child page" and choose "Homepage". Fill it out and choose "Publish" from the save menu at the bottom. The title you set here will show up in the tab title.
  - In the left menu, go to "Settings > Sites". Choose the existing one, and change the root page to the home page you just created. Also change the "Site Name" here. (That's what will show up on your home page.)
  - You should now be able to refresh the site (at `localhost:8000`) and see a correctly-styled (but empty) home page.
- Configure your settings.
  - In the left menu, go to "Settings > General Settings". Here you can configure some general/useful site settings, like Google Analytics and Disqus comments.
- Create an "About" page
  - In the left menu, click "Pages," then the home page you previously created.
  - Click "Add child page" and select "Information Page."
  - Call it "About" and fill it with whatever content you want.
  - Go to the "Promote" tab and check the "Show in menus" box. (This is necessary for it to show up in the footer menu.)
  - Then select "Publish."
- Create Authors
  - From the home page in the admin, select "Add child page" and choose "Authors list."
  - Call it "Authors" and publish it. You can only create one "Authors list" page.
  - Create a child page of "Authors". (This will automatically be an Author bio page.)
  - The Author "Title" is the author's name. You must choose a different user for each author page/bio. That means each of your authors will need their own user on the site.
  - Publish the author page. You'll need an Author to be able to an Article.
- Create subjects (categories for articles)
  - From the home page in the admin, select "Add child page" and choose "Subject Section."
  - All you need to choose is the name of the section. For example, "Technology". Then publish. (Each of these sections will show up in the main menu.)
  - You can create as many subject sections as you want. You'll file your articles under these sections.
- Configure footer menu
  - From the left menu, select "Settings > Flat menus" and click "Add flat menu".
  - Call it "Footer", select your current site, and set the handle to `footer_menu`. (If you don't set this handle, it won't show up at the bottom of the page!)
  - Leave the "Heading" blank and save.
- Create an article
  - From the admin for one of the Subjects you created above, click "Add child page." This will automatically create an "Article" page.
  - Write out your article. You can save it as a draft if you're not ready to publish it yet.
  - Note: Right now the "Audiences" part isn't used anywhere (yet).
  - Tags is a list of arbitrary string tags. They're an additional way that your audience can filter and see related articles.
  - For the Body, you can use Markdown formatting in your text. But for internal links, use the link option in the text editor. For videos (including ones that you want to emulate GIFs) use the "Media" option.
  - You can use the "Notes" section at the bottom to make notes to yourself about the article that won't show up anywhere on the published page.

## Features

- Articles:
  - Create custom subject categories
  - Tag articles
  - Article comments with Disqus
  - Highly configurable article content, including: markdown-formatted text, tables, captioned images, block quotes, LaTeX-formatted math, and embedded YouTube videos.
  - Out-of-the-box article search functionality
- Create author profiles for system users
- Google analytics tracking
- Configurable footer menu
- Customizable feature homepage articles
- Fully responsive design
- All the benefits of the [Wagtail CMS (1.13)](https://wagtail.io/)
