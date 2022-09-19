# recordAddr.py
import time, requests, json
def main():
    with open("/path/to/config.json", "r") as fp:
        config = json.load(fp)
    
    with open("/path/to/addrRecord.json", "r") as r:
        recoAddr = json.load(r)["ip"]
    
    curAddr = json.loads(requests.get(config["getAddrUrl"]).text)["ip"]
    print(time.asctime(time.localtime(time.time())), " ", end="")
    print("Addr6: ", curAddr, end="")
    if recoAddr != curAddr:
        print(" address changed!")
    else:
        print()
    
    newRecord = "{\"ip\": \"" + curAddr + "\"}"
    with open("/path/to/addrRecord.json", "w") as r:
        r.write(newRecord)

if __name__ == "__main__":
    main()