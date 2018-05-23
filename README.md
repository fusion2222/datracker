# DaTracker

<img src="http://exile.sk/logo.svg" width="110px">

DaTracker stands for **D**amn **a**wesome **Tracker**. It is a small web application, which main purpose is to
minimize effort for company managers during checking task-solving progress by employees. At the same time,
DaTracker aggregates simple statistics about the company and its workplaces. So far managers can create issues
for employees, assign them, track them, etc.

## Before you continue
The project is still under development, and will be actively developed. There is still a lot work to do, so any
contributors will be welcome.

## Prerequisites

There are prerequisites in order to run this project locally:

- [Install Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git) on your machine.
- [Install SASS](https://sass-lang.com/install) on your machine.
- [Install Python 3.6.0 or higher](https://www.python.org/downloads/) on your machine.
- `pip` (A package manager for Python) should be installed along with your Python installation. You can check if
python was installed by running command `pip --version`. The same way check for pip3 : `pip3 --version`. If both
these commands were not recognized by system, it means, the pip is not installed or was removed. In this
case [install pip](https://pip.pypa.io/en/stable/installing/) manually.
- Install [virtualenv](https://virtualenv.pypa.io/en/stable/installation/). This is because we want to avoid
system-wide package installation.
- [Install NodeJS](https://nodejs.org/en/download/) 10.1.0 or higher.
- NPM package manager for NodeJS should be installed along NodeJS installation. Check if you have installed npm
by typing `npm --version` in terminal. If command is not recognized,
[install NPM package manager](https://www.npmjs.com/get-npm)

## How to run a project

In order to install DaTracker you must finish following steps:

- If you have not opened Terminal, open it and navigate into folder where you would like to have DaTracker installed.
- run `git clone git@github.com:fusion2222/datracker.git` from your Terminal. This command clones clone on your computer.
- Navigate to newly created DaTracker folder using your Terminal.
- [Create virtualenv](https://virtualenv.pypa.io/en/stable/userguide/) for DaTracker in your system.
- [Activate virtualenv](https://virtualenv.pypa.io/en/stable/userguide/#activate-script) you recently created.
- [Create Database SQLite](https://www.sqlite.org/cli.html) file in your datracker root directory.
Name it `db.sqlite3`.
- run `pip install -r requirements.txt` in your Terminal. If you have installed pip3 instead, run the
same command for pip3
- Run `python manage.py makemigrations`
- Run `python manage.py create_initial_data` - This will also create your test data
- Rum `npm install`
- Run `npm link gulp`
- Run `gulp sass`
- Run `gulp js`
- Run `python manage.py collectstatic`
- Copy `env.json.example` into project root directory and name it `env.json`. Then set your project
variables in this file.
## How to run

Okay you have project succesfuly installed. Now follow these steps:

- Activate your `virtualenv` related to datracker project and navigate into project root folder.
- Run `python manage.py runserver localhost:8000` (If you have installed your python
under `python3`, run the same command).
- Type localhost:8000 as web address in your browser. Datracker should load.
- If you ran `python manage.py create_initial_data`, administrator Employee has been already
created. Default username is `admin` and password is `password`.

## Important notice

Currently this biggest flaws of DaTracker is secure handling of vendor-packages, frontnend as well as
Messages module not working. This will be fixed soon.

## Contribution guide

Jesus once said wise thing - Those who will try to push any code into this repository, without reading
following rules will be damned. So better check the rules:
- Project uses strictly SCSS syntax as the only CSS syntactical preprocessor. We do not mix Sass,
Less and SCSS no matter what. (only exceptions are vendor packages)
- Consistency - If there is some naming convention widely used in project, use it no matter how obscure
it looks. This applies also for graphical and frontend stuff.
- Keep as low dependencies as possible - Dependencies are good.. but only if they save you a lot of
tedious, difficult or repetitive work.
- Any ideas are welcome and feel free to discuss.

### Compiling Javascript and SCSS to CSS

For one-time compilation of your Javascript files use following command:

`gulp js`

For one-time compilation of your SCSS files use following command:

`gulp sass`

In case of active development related to SCSS and JS files you may need to have watchdog-compilation, so you
can develop more quickly and elegantly:

`gulp watch`

### Important notes

More details Will be added..

## Contact

In case of any questions feel free to contact me on GitHub.
