from scapy.all import *

iPkt = 0

def process_packet(pkt):
    global iPkt
    iPkt += 1
    print(f"Ho letto un pacchetto sulla tua macchina {str(iPkt)}")

sniff(iface="enp4s0", filter="", prn=process_packet)