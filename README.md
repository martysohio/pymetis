# pymetis

Python web site monitor using InfluxDB + Grafana dashboards.  This project is a base to work from to develop your own monitoring dependent on your needs.  

## Requirements

Docker, and you can test locally with the proper Python environment, check the requirement.txt. Requires Python 3.7+

## How to use

- Run docker-compose build to create the Python image
- Edit list in scripts/url.list for what sites you want to monitor
- docker-compose up -d
- A cron should start in the Python container to run hits against the sites.

Status codes are logged with a timeout of 30 seconds.  Unreachable/immediate errors have a status code of 0

Open Grafana to see a simple premade dashboard at localhost:3000 , user/pass is admin/foobar

## Recommendations

Alter to suit. Most of the TICK stack is included, but no alerts are pre-provisioned as everyone will have their own notification channels. I.E. if you like Kapacitor then you can use it , or integrate checks and notifications into the check_urls.py script.  
