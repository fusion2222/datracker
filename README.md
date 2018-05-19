# DaTracker

DaTracker stands for Damn awesome Tracker. It is a small web application, which main purpose is to minimize effort
for company managers during checking progress of task-solving by employees. At the same time, DaTracker displays
simple statistics about the company and its workplaces. Users may create and solve issues and assigne them on each
other. CEO and Managers have right to manage employees, issues and workspaces.

## How to run a project

In order to install DaTracker you must finish following steps:

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
- If you have not opened Terminal, navigate into folder where you would like to have DaTracker installed.
- run `git clone git@github.com:fusion2222/datracker.git` from your Terminal.
- Navigate to newly created DaTracker folder using your Terminal.
- [Create virtualenv](https://virtualenv.pypa.io/en/stable/userguide/) for DaTracker in your system.
- [Activate virtualenv](https://virtualenv.pypa.io/en/stable/userguide/#activate-script) you recently created.
- [Create Database SQLite](https://www.sqlite.org/cli.html) file in your datracker root directory.
Name it `db.sqlite3`.
- run `python manage.py makemigrations`
- run `pip install -r requirements.txt` in your Terminal. If you have installed pip3 instead, run the
same command for pip3
- rum `npm install`
- run `npm link gulp`
- run `gulp sass`
- run `gulp js`
- run `python manage.py collectstatic`

## Contribution guide

Project uses strictly SCSS syntax as the only CSS syntactical preprocessor.

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