# pymetis

Python web site monitor using InfluxDB + Grafana dashboards

## How to use

- Run docker-compose build to create the Python image
- Edit list in scripts/url.list for what sites you want to monitor
- docker-compose up -d
- A cron should start in the Python container to run hits against the sites.

Status codes are logged with a timeout of 30 seconds.  Unreachable/immediate errors have a status code of 0

Open Grafana to see a simple premade dashboard.
