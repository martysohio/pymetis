import requests
import json
from influxdb import InfluxDBClient
import time 

influx_client = InfluxDBClient('127.0.0.1', '8086', 'admin','admin','http_monitor')

def send_to_influx(data):
    #fields can be updated with new measurements as desired
    json_body = [
                    {
                            "measurement": "http_response",
                            "tags": {
                                    "domain": data['domain'], 
                                    "status" : data['status'],
                            },
                 #           "time": data["time"] + "000000000",
                            "fields": {
                                "response_time" : data['response_time'],
                            }
                    }
            ]
    output=influx_client.write_points(json_body)
    return output

def check_url(url):
    resp = requests.get(url)
    """
    f = open("log.txt","a")
    f.write(str(len(resp.text.split())) + "\n")
    f.close()
    """
    timestamp = str(time.time()).split(".")[0]
    data = { "domain" : resp.url, "status" : resp.status_code, "response_time" : str(resp.elapsed.total_seconds()) , "time" : timestamp  }
    
    send_to_influx(data)
    return True