import os
import route53
import requests
import time

# import dotenv

# dotenv.load_dotenv()

AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
AWS_ACCESS_SECRET = os.getenv("AWS_ACCESS_SECRET")
A_RECORD_NAME = os.getenv("A_RECORD_NAME")
POLL_TIMEOUT_SECONDS = os.getenv("POLL_TIMEOUT_SECONDS")
HOSTED_ZONE_ID=os.getenv("HOSTED_ZONE_ID")


def main():
    conn = route53.connect(
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_ACCESS_SECRET,
    )

    cachedIp = ""


    print("======= STARTING UPDATE LOOP =======")
    while True:
        req = requests.get("https://api.ipify.org")
        if req.status_code != 200:
            Exception("ERR: Ip readback service reported status: ", req.status_code)

        IP = req.text
        if IP != cachedIp:
            print(time.asctime())
            zone = conn.get_hosted_zone_by_id(HOSTED_ZONE_ID)
            for record_set in zone.record_sets:
                if A_RECORD_NAME in record_set.name:
                    record_set.name = record_set.name.replace("\\052", "*")
                    print(" > Cached IP and public ip mismatch, dns lookup says: ", record_set.name, " ", record_set.records)
                    if record_set.records[0] != IP:
                        print("     |- Updating Ip for: ", record_set.name, " ", record_set.records, " -> ", IP)
                        record_set.records[0] = IP
                        record_set.save()
                    else:
                        print("     |- no need to update: ")

            cachedIp = IP
            print()
        time.sleep(int(POLL_TIMEOUT_SECONDS))

# Hangs on network reset
while True:
    try:
        main()
    except Exception as e:
        print("ERR (", time.asctime(), ") : ", repr(e))
        print()
        if "403" in str(e):
            print("CRITICAL ERR (", time.asctime(), ") : update iam policy, exiting ...")
            break 
    time.sleep(int(POLL_TIMEOUT_SECONDS))
