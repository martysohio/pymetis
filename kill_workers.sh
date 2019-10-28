#!/bin/sh
ps aux | grep "rq worker" | awk '{print $2}'  | xargs -I % kill % 