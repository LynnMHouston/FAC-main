# Development

We use either [Docker with `docker-compose`](#docker) or [local development](#local-development) when working on issues and shipping pull requests.

## Contents

* [Tools](#tools)
* [Setting up your dev environment](#setting-up-your-dev-environment)
  * [Environment Variables](#environment-variables)
  * [Docker](#docker)
  * [Local Development](#local-development)
* [Django setup](#django-setup)

## Tools

* [Docker](https://docker.com)
* Local dev
  * [Pyenv](https://github.com/pyenv) for managing Python versions
  * [pyenv-virtualenv](https://github.com/pyenv/pyenv-virtualenv) for managing virtual environments
  * [Postgres](https://www.postgresql.org/)
  * [SAM.gov](https://sam.gov/content/home) to validate UEI's

## Setting up your dev environment

---
**NOTE**

Target python version is defined in [../backend/runtime.txt](../backend/runtime.txt)

---

## Environment Variables

Currently, the only environment variable is `SAM_API_KEY` to validate UEI's.  

To test UEI validation locally, apply for a SAM.gov [System Account](https://www.fsd.gov/sys_attachment.do?sys_id=5462e13d1b594d9006b09796bc4bcbd2) and then copy the API key into your local environment (should end up somewhere in `~/.bash_profile`, `~/.bashrc`, `~/.zshrc`, or whatever flavor of shell you're using.)

## Docker

An application and database are configured in [../backend/docker-compose.yml](../backend/docker-compose.yml), we create a volume to persist the development database, and we mount our `./backend` working directory to the `web` container so that changes made in development are reflected in the container without needing to re-build.

1. Install Docker
2. Build and start using [../backend/docker-compose.yml](../backend/docker-compose.yml)

    ```shell
    # with a working directory of ./backend
    docker-compose build
    docker-compose up
    ```

3. The application will start and be accessible @ http://localhost:8000/


## Local Development
### Install the tools

`brew install pyenv pyenv-virtualenv`

If your tools are previously installed, you may need to

`brew update && brew upgrade pyenv`

to have all of the most recent versions of Python available. This could be slow if you haven't updated in a while. Get a cup of ☕.

(Your setup process on Windows/Linux will vary. Currently, we assume local development in a Linux-like environment.)

### Update your environment

You will likely need to [update your shell](https://stackoverflow.com/questions/33321312/cannot-switch-python-with-pyenv).

```
eval "$(pyenv init --path)"
```

should end up somewhere in `~/.bash_profile`, `~/.bashrc`, or whatever flavor of shell you're using.

### Set link flags

You *might* need to set link flags. Otherwise, when you `make install`, there could be failures in the building of `psycog2`. YMMV.

```
export LDFLAGS="-L/usr/local/opt/openssl/lib -L/usr/local/lib -L/usr/local/opt/expat/lib" && export CFLAGS="-I/usr/local/opt/openssl/include/ -I/usr/local/include -I/usr/local/opt/expat/include" && export CPPFLAGS="-I/usr/local/opt/openssl/include/ -I/usr/local/include -I/usr/local/opt/expat/include"
```

### Create a virtual environment

You may need to install the Python version being used by the team. The following take place in the `backend` directory of the checked out repository.

```
FAC_PYTHON_VERSION=`cat .python-version`
pyenv install $FAC_PYTHON_VERSION
```

Then, set up the virtualenv.

`pyenv virtualenv $FAC_PYTHON_VERSION FAC`

### Activate your new virtual environment

`pyenv activate FAC`

Depending on how you feel about seeing the virtualenv in your prompt:

```
pyenv-virtualenv: prompt changing will be removed from future release. configure `export PYENV_VIRTUALENV_DISABLE_PROMPT=1' to simulate the behavior.
```

### Install python dependencies

```
python -m pip install --upgrade pip
pip install pip-tools
```

### Set environment variables

We use environment variables to configure much of how Django operates, at a minimum you'll need to configure the uri of your local database.

Set a `DATABASE_URL` environment variable with the uri of your local database
    *  `postgresql://[userspec@][hostspec][/dbname]`


### Django setup

In development, you'll need to run Django's `manage.py` and specific commands like `makemigrations`, `createsuperuser`, and more.

If developing with Docker, execute these commands from within the `web` container


```shell
docker-compose run web python manage.py $COMMAND $ARGS
```

As a convenience, you can create an alias in your shell following this or a similar pattern
```shell
fac ()
{
  docker-compose run web python manage.py ${@}
}
```

**Example workflows**

Let's use this workflow to create a `superuser` in our development environment so we can access the Admin interface!


```shell
# Start our docker containers w/ docker-compose
docker-compose up

# Django management command to create a new superuser
docker-compose run web python manage.py createsuperuser

# Follow the prompts to enter username, password, etc.

# Enter the user/pass @ the Admin login page
open http://localhost:8000/admin
```