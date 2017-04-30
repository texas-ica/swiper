# Swiper

ICA Slack Bot that responds to various commands, such as making announcements, creating polls, roasting/complimenting team members, etc.

## Development

Python 3.5 is a requirement to build this project. Fork the repository and `cd` into it. You will need to create a virtual environment to keep track of the various dependencies.

```sh
$ virtualenv -p python3 venv
```

Activate the virtual environment, install the project dependencies (`requirements.txt`), and make the project a `pip` package.

```sh
$ source venv/bin/activate
$ pip install -r requirements.txt
$ pip install -e .
```

To run the server, you need to specify whether the bot will be run on the production or test channel. This can be specified with the `-p` or `-t` flags

If you want to further develop the bot, contact `shreydesai@me.com` for 1)  `data/` files, 2) the `config.py` configuration file, and 3) credentials for the test server, which are not under version control.

## Directory Structure

- `data/`: Contains a members list, compliment/roast list, memes database, and usage logs.
- `swiper/`: Core Swiper files
    - `command.py`: Defines commands the bot responds to
    - `error.py`: Error definitions (not used)
    - `parse.py`: Parses messages from the Slack channel
    - `server.py`: Request handling using the Slack API

## Miscellaneous

Currently, the bot is run on UTCS lab machines (primarily `skipper`), but the goal is to deploy the bot as a worker process on Heroku. Some work has been done in the `Procfile`, but some tweaking is still required to deploy it.
