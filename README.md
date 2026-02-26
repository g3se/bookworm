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

I recommend to clone the repository through SSH to authenticate with GitHub, using a URL similar to: `ssh://git@github.com/g3se/bookworm.git`.

There are alternative ways to clone that let you avoid needing to interact with SSH
directly:
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
