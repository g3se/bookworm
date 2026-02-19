# bookworm
bookstore website for CS 3773-002, Spring 2026

# Setup guide

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

Clone <https://github.com/g3se/bookworm.git>.

I do this through SSH to authenticate myself with GitHub. I know how to set this
up on macOS and Linux, but not on Windows.

Alternatives:
- GitHub Desktop: <https://github.com/apps/desktop>
- VS Code: <https://code.visualstudio.com/download>

## Install the project's dependencies

`cd` into the bookworm repository so that you're in the same directory as
`pyproject.toml` and `poetry.lock`.

```sh
poetry install
```

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
