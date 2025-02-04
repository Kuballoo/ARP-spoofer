
# ARP Spoofer

Program which let you perform ARP spoof attack, and after all restore right ARP tables on target and spoofed device.

**You use script on your own risk. In many countries this process is illegal!**

## Usage
To use the script, follow the steps bellow.

Firstly:
```bash
pip install -r requirements.txt
```
Secondly:
```bash
python arp_spoofer.py -t [target_ip] -s [spoofed_ip]
```
or
```bash
python arp_spoofer.py --target [target_ip] --spoof [spoofed_ip]
```

