# Vaccionation Tweeter Bot ![post update](https://github.com/PedroRestrepo/VacTracking/actions/workflows/post_update.yml/badge.svg)
![Logo](static/logo_128x128.png)

## Motive
This is a personal project created to play around with Tweeter API and Github action

## How is works
*Workflow* - [post_update.yml](.github/workflows/post_update.yml) currently runs everyday at 23:00 PM (UTC). The workflow will build all the project dependerncies 

*Script* - [post_update.py](post_update.py) is the file that actually reads the status, generates the formatted tweets that are ready for publishing and publishes them

## Credit
All the data for the tweets currently comes from [Covid19Tracker](https://covid19tracker.ca/).

