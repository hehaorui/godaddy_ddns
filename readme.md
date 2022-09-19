# ipv6 DDNS Script for GoDaddy 

# How to Use

* fill the `config.json` file with your key and secret obtained from godaddy, you can get then at <a href="https://developer.godaddy.com/keys">here</a>
* also fill the domain name, record type and name of the target DNS record in the `url` field
* the `getAddrUrl` is used to get your current IPV6 address from a public accessible API, you can update it if you find it no longer accessible
* you can add the execution of the script in you crontab to perform DNS record update once in a while
* the `recordAddr.py` script is used to record the change of you IPV6 address, which can help you to decide the time interval of DNS record update
