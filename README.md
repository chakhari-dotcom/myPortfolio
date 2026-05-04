# My Portfolio

A Django portfolio website built with a simple project manager and contact form. This project includes a homepage with project listings, project CRUD operations, and an email contact form.

## Features

- Homepage listing all portfolio projects
- Contact page with email form integration
- Create, update, and delete portfolio projects
- Category-based project classification
- Image upload support for projects
- Static assets configured via `staticfiles`
- SQLite database for local development

## Project Structure

- `base/` — main Django app with models, views, templates, and URLs
- `myPortfolio/` — Django project settings and global URL configuration
- `db.sqlite3` — local SQLite database
- `staticfiles/` — CSS and static assets
- `templates/base/` — HTML templates for home, contact, and project forms

## Requirements

- Python 3.10+ (or compatible version)
- Django 6.0.x

> If you have a `requirements.txt` file, use it. Otherwise install Django manually.

## Setup

1. Clone the repository:

```bash
git clone <repository-url>
cd myPortfolio
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install django==6.0.4
```

4. Apply database migrations:

```bash
git checkout -- .
python manage.py makemigrations
python manage.py migrate
```

5. Create a superuser (optional):

```bash
python manage.py createsuperuser
```

## Running the Application

```bash
python manage.py runserver
```

Then open `http://127.0.0.1:8000/` in your browser.

## Email Configuration

The project already includes SMTP email settings in `myPortfolio/settings.py` for Gmail. To use your own email account, update the following settings:

- `EMAIL_HOST_USER`
- `EMAIL_HOST_PASSWORD`
- `DEFAULT_FROM_EMAIL`

> For security, do not commit real credentials to GitHub. Instead, use environment variables in production.

## Notes

- The app uses the `base` Django app and includes routes for home, contact, and project CRUD actions.
- Media uploads are stored in the `media/` directory, and static files are served from `staticfiles/`.
- For production deployment, set `DEBUG = False`, configure `ALLOWED_HOSTS`, and secure the `SECRET_KEY`.

## Useful Commands

- `python manage.py runserver` — start the development server
- `python manage.py migrate` — apply migrations
- `python manage.py createsuperuser` — create an admin user
- `python manage.py collectstatic` — collect static files for production

## License

Add your preferred license here.
