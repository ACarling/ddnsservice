import os
import route53
import requests
import time

AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
AWS_ACCESS_SECRET = os.getenv("AWS_ACCESS_SECRET")
A_RECORD_NAME = os.getenv("A_RECORD_NAME")
POLL_TIMEOUT_SECONDS = os.getenv("POLL_TIMEOUT_SECONDS")

conn = route53.connect(
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_ACCESS_SECRET,
)

cachedIp = ""

for zone in conn.list_hosted_zones():
    for record_set in zone.record_sets:
        if A_RECORD_NAME in record_set.name:
            print("Retrieved Ip: ", record_set.name, " ", record_set.records)
            cachedIp = record_set.records[0]

            if record_set.records[0] != cachedIp:
                print("Updating Ip for: ", record_set.name, " ", record_set.records, " -> ", cachedIp)
                record_set.records[0] = cachedIp
                record_set.save()

print("======= STARTING UPDATE LOOP =======")
while True:
    IP = requests.get("https://api.ipify.org").text
    print("Reported IP: ", IP)
    if IP != cachedIp:
        for zone in conn.list_hosted_zones():
            for record_set in zone.record_sets:
                if A_RECORD_NAME in record_set.name:
                    print("# ", record_set.name, " ", record_set.records)
                    if record_set.records[0] != IP:
                        print(" |- Updating Ip for: ", record_set.name, " ", record_set.records, " -> ", cachedIp)
                        record_set.records[0] = IP
                        record_set.save()
        cachedIp = IP
    time.sleep(int(POLL_TIMEOUT_SECONDS))