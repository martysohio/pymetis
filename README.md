# pymetis

Python web site monitor using InfluxDB + Grafana dashboards

## How to use

Create list of URLs to hit in urls.list

## The point

Sometimes you want to monitor a lot of URLs, it can be as hard or as easy as you want it to be. A lot of similar things already exist, I just wanted to see if I could do it this way.

## Flaws

Using multiple RQ workers scales much as your available hardware on a single box. Doesn't scale horizontally well so far.