import requests
import argparse
import json

parser = argparse.ArgumentParser()
parser.add_argument("--node", required=True)
parser.add_argument("command", choices=["put", "get", "status"])
parser.add_argument("key", nargs="?")
parser.add_argument("value", nargs="?")
args = parser.parse_args()

url = args.node

if args.command == "put":
    requests.post(url + "/put", json={"key": args.key, "value": args.value})
    print("PUT sent")
elif args.command == "get":
    r = requests.get(url + "/status")
    store = r.json()["store"]
    print(store.get(args.key, "Not found"))
elif args.command == "status":
    r = requests.get(url + "/status")
    print(json.dumps(r.json(), indent=2))
