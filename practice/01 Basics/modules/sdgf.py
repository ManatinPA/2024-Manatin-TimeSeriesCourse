#! /usr/bin/env python3

from collections import Counter
from scapy.all import sniff
from collections import deque
import psycopg2
import json
import urllib.request
import subprocess
import os
import datetime
import ipaddress
## Create a Packet Counter
def x_not_in_d(x,d):
    try:
        if d.index(x):
            d.appendleft(x)
            return True
    except ValueError:
         d.append(x)
         return False
## Define our Custom Action function
def custom_action(packet):
    if ipaddress.IPv4Address(str(packet[0][1].src)).is_private: return
    # Create tuple of Src/Dst in sorted order
    if x_not_in_d(packet[0][1].src,d):
        try:
          connection = psycopg2.connect(database="logs", user="postgres", password="postgres", host="192.168.12.92", port=5432)
          cursor = connection.cursor()
          cursor.execute(f"""SELECT cidrs.cidr,
                                 cidrs.country,
	                             sel."IP"
                          FROM ( SELECT "AR6280_ips"."IP",
                                        "AR6280_ips".cidr
                                            FROM "AR6280_ips"
                                        JOIN cidrs cidrs_1 ON "AR6280_ips".cidr = cidrs_1.id) sel, cidrs
                                        WHERE sel.cidr = cidrs.id and sel."IP"='{packet[0][1].src}'""")
          result=cursor.fetchall()
          print(result)
          if len(result)==0:
              print("New address:"+str(packet[0][1].src))
              req = urllib.request.Request(url=f"https://stat.ripe.net/data/geoloc/data.json?resource={packet[0][1].src}", headers={
                'User-Agent': ' Mozilla/5.0 (Windows NT 6.1; WOW64; rv:12.0) Gecko/20100101 Firefox/12.0'})
              with urllib.request.urlopen(req) as f:d
                data = json.loads(f.read().decode('utf-8'))
                country=data["data"]["located_resources"][0]["locations"][0]["country"]
                cidr=data["data"]["located_resources"][0]["locations"][0]["resources"][0]
                print(country,cidr)
                cursor.execute("INSERT INTO cidrs (cidr,country,last_query) VALUES (%s,%s,%s)  ON CONFLICT DO NOTHING;", (cidr, country, datetime.datetime.now()))
                connection.commit()
                cursor.execute(f"""INSERT INTO "AR6280_ips" ("IP",cidr) VALUES ('{str(packet[0][1].src)}', (SELECT id from cidrs where cidrs.id={cidr}))  ON CONFLICT DO NOTHING;""")
                connection.commit()
                if (country) in white_countries:
                    subprocess.call("./add_to_white_countries.sh '%s'" % cidr, shell=True)
                if (country) in black_countries:
                    subprocess.call("./add_to_black_countries.sh '%s'" % cidr, shell=True)
          else:
            for element in result:
                print(element[1])
                if element[1] in white_countries:
                    subprocess.call("/ipsets/sniffer/add_to_white_countries.sh %s" % element[0], shell=True)
                if element[1] in black_countries:
                    subprocess.call("/ipsets/sniffer/add_to_black_countries.sh %s" % element[0], shell=True)
        except Exception as e: print(str(e)+":"+str(packet[0][1].src))
        finally:
          cursor.close()
          connection.close()

## Setup sniff, filtering for IP traffic
d = deque(maxlen=1000)
os.nice(5)
white_countries=[]
black_countries=[]
iface=""
with open('white_countries','r') as f:
    for element in f.readlines():
        for el in element.split():
            white_countries.append(el)
with open('black_countries','r') as f:
    for element in f.readlines():
        for el in element.split():
            black_countries.append(el)
print(white_countries)
print(black_countries)
with open('iface','r') as f:
    iface=f.readline().rstrip().lstrip()
sniff(iface=iface, filter="ip", prn=custom_action)
