# bookworm
bookstore website for CS 3773-002, Spring 2026


# Setup guide

## Install Python

Neither pipx nor Poetry provides Python for you.
You should install it independently if you do not already have a version of
Python 3.14.0 or later installed: <https://realpython.com/installing-python/>.

Make sure that you get Python 3.14.0 or later.

Verify that it's installed by running
```sh
python3.14 --version
```
which should print something like `Python 3.14.x`.

## Install Poetry

Get pipx: <https://pipx.pypa.io/stable/installation/>

Install Poetry using pipx
```sh
pipx install poetry
```
(<https://python-poetry.org/docs/#installing-with-pipx>)

Install the poetry shell plugin
```sh
pipx inject poetry poetry-plugin-shell
```

## Clone the project

Clone <https://github.com/g3se/bookworm>.

I recommend to clone the repository through SSH to authenticate with GitHub,
using a URL similar to: `ssh://git@github.com/g3se/bookworm.git`.

There are alternative ways to clone that let you avoid needing to interact with
SSH directly:
- VS Code (built-in GitHub integration):
  <https://code.visualstudio.com/download>
- GitHub Desktop: <https://github.com/apps/desktop>

## Install the project's dependencies

`cd` into the bookworm repository so that you're in the same directory as
`pyproject.toml` and `poetry.lock`.

```sh
poetry install
```

**NOTE:** If the `poetry.lock` file changes, you will probably need to run this
command again in order to synchronize your dependencies with the project's
requirements.
Just running it occasionally should be fine.

## Do this each time you want to test the website / use manage.py / run Python

Activate the environment in a subshell
```sh
poetry shell
```

`cd` into `bookworm` from the root of the repository. You should be in the same
directory where `manage.py` is.

Start the built-in webserver
```sh
python manage.py runserver
```

Connect to <http://localhost:8000/> in your web browser to view the website.


# Run with Gunicorn

Gunicorn website: <https://gunicorn.org/>.

Gunicorn is a web server that lets us run the Django website through WSGI.

## Set up Gunicorn

Activate the virtual environment (if you haven't)
```sh
poetry shell
```

`cd` into the `bookworm` directory that contains `manage.py`.

Collect the static files into directory `staticfiles`
```sh
python manage.py collectstatic
```
**NOTE:** You may need to re-run this command if the static files update.

## Run Gunicorn

Activate the virtual environment (if you haven't)
```sh
poetry shell
```

`cd` into the `bookworm` directory that contains `manage.py`.

Reload Gunicorn and run through WSGI.
```sh
gunicorn bookworm.wsgi:application --reload
```


# Copyright Disclaimer

The bookworm contributors license bookworm under the `CC0-1.0` license as
designated by SPDX and place it into the public domain in all applicable
jurisdictions (see `LICENSE` file or <https://spdx.org/licenses/CC0-1.0.html>).
The copyrights of other works contained within this repository, i.e. those of
the cover art and details of books located within the `bookworm/media` directory
and `bookworm/db.sqlite3` database, respectively, are held by their respective
copyright holders.
These other works are not all released under similar terms into the public
domain.
The bookworm contributors do not necessarily claim copyright to these other
works and use them for educational purposes only.

Under section 107 of the Copyright Act of 1976, allowance is made for "fair use"
for purposes such as criticism, comment, news reporting, teaching, scholarship,
education, and research.
Fair use is a use permitted by U.S. copyright statute that might otherwise be
infringing.
Non-profit, educational, or personal use tips the balance in favor of fair use.
