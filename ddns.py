#!/usr/bin/python3
# -*- coding: utf-8 -*- #
# ddns.py
import json
import requests
import subprocess
import re
import sys
import time

def log(s):
     print(time.asctime(time.localtime(time.time())), " ", s)

def getLocalIP6():
    #interface='eth0'
    interface=''
    output=subprocess.getoutput('/sbin/ip addr show '+interface+'|grep -v deprecated')
    ipv6=re.findall(r' inet6 ([^f:][\da-f:]+)/(\d+) scope global .+?\n.+? valid_lft (\d+)sec ',output,re.M|re.I)
    # eui64的ipv6地址按超时时间排序,其他的排前面
    # def my_key(a):
    #     if a[0].find('ff:fe')>4:
    #         return int(a[2])
    #     else:
    #         return -1
    
    ipv6.sort(key=lambda a: int(a[2]) if a[0].find("ff:fe")>4 else -1, reverse=True) #反向排序
    ipv6 = [a[0].strip() for a in ipv6]

    
    #print('ipv4=',ipv4)
    #print('ipv6=',ipv6)

    return ipv6

def getRecord(url, key, secret):
    authKey = 'sso-key ' + key + ':' + secret
    head = {
            'accept':'application/json',
            'Content-Type': 'application/json',
            'Authorization': authKey}
    resp = requests.get(url, headers=head)
    if resp.status_code != 200:
        raise Exception("get original record failed")
    return json.loads(resp.text)

def setRecord(url, key, secret, addr):
    authKey = 'sso-key '+ key + ':' + secret
    head = {
            'accept':'application/json',
            'Content-Type': 'application/json',
            'Authorization': authKey}
    data = [{
            'data': addr,
            'ttl': 600
            }]
    return requests.put(url, headers=head, data=json.dumps(data)) 

def main():
    iUpdateCount = 10
    filename= 'config.json'
    config = None
    try:
        with open(filename, 'r', encoding='utf-8') as fp:
            config = json.load(fp)
    except FileNotFoundError as e:
        sys.stderr.write("json.conf not found, aborted")
        raise e
    
    success = False
    resp = requests.get(config["getAddrUrl"])
    # get public addr6 via public api
    if resp.status_code == 200:
        success = True
        curAddr6 = [json.loads(resp.text)["ip"].strip()]
    
    # get addr6 via local instruction
    if not success:
        curAddr6 = getLocalIP6()
        if len(curAddr6)>0:
            success = True
    
    # failed to get ipv6 address
    if not success:
        raise Exception("failed to get ipv6 address")
    
    recAddr6 = getRecord(config["url"], config["key"], config["secret"])[0]["data"]

    iUpdate = 10
    resp_code = -1
    if recAddr6 in curAddr6:
        log("no need to update DNS record")
        return

    while iUpdate > 0 and resp_code != 200:
        iUpdate -= 1
        resp_code  = setRecord(config["url"], config["key"], config["secret"], curAddr6[0]).status_code
    
    if resp_code != 200:
        raise Exception("failed to update record")
    else:
        log("DNS record updated, new address:" + curAddr6[0])

    
    


if __name__=='__main__':
    main()
