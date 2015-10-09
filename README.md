# Tournament Tracker

Second project for Full-Stack Web Devloper Nanodegree course; Tournament tracker is an API that maintains Swiss-Style tournament results and player matches.
Feature list:

* Multiple tournaments
* Player registration
* Player pairing
* Match win, loss, and tie reporting
* Supports byes; odd player count
* Tracks Opponent Match Wins

## Table of Contents

* [Installation and Run](#installation-and-run)
* [Helpful Commands](#helpful-commands)
* [Creators](#creators)
* [Copyright and license](#copyright-and-license)

## Installation and Run

In order to install Tournament Tracker follow these instructions:
- Download [Python 2.7](https://www.python.org/downloads/) and install it, if you do not already have it.
- Install [Vagrant](https://www.vagrantup.com) and [Virtual Box](https://www.virtualbox.org).
- Clone repository: `git clone https://github.com/brianquach/udacity-nano-fullstack-tournament.git` or download the zip [here](https://github.com/brianquach/udacity-nano-fullstack-tournament).
- Navigate to the directory where you cloned the repo or unzipped the file to.
- Launch Vagrant VM and SSH into it.
- Navigate to the tournament file with `cd` into `/vagrant/tournament`.
- Launch psql and execute `\i tournament.sql` to initialize table schema, then quit psql.
- To run the default test functions execute `python tournament_test.py`.

### Helpful Commands

* Launch Vagrant `vagrant up`
* Terminate Vagrant `vagrant halt`
* SSH into Vagrant `vagrant ssh`
* Exit out of Vagrant SSH `exit`
* Launching psql in after SSHing into Vagrant `psql`
* Quit psql `\q`

## Creators

Brian Quach
* <https://github.com/brianquach>

## Copyright and license

Code copyright 2015 Brian Quach. Code released under [the MIT license](https://github.com/brianquach/udacity-nano-fullstack-tournament/blob/master/LICENSE).