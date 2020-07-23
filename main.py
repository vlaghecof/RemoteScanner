import scapy.all as scapy

import time

import subprocess





NETWORK = "192.168.1.0/24"

IP_NETWORK ='192.168.1.1'
IP_DEVICE ='192.168.1.2'


INTERVAL = 3  # seconds

dictionary = {

     'b0:19:c6:b3:4c:4d': 'Vlad '

}





def scan(ip):

    macs = set()

    arp_request = scapy.ARP(pdst=ip)


    broadcast = scapy.Ether(dst='ff:ff:ff:ff:ff:ff')

    arp_request_broadcast = broadcast/arp_request

    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]



    for host in answered_list:

        if host[1].psrc != "192.168.1.1":
            macs.add(host[1].src)




    return macs





def connection_change(hosts, action):

    if action not in ("connected", "disconnected"):

        raise ValueError(f"Invalid action: {action}")

    for host in hosts:

        device = dictionary[host] if host in dictionary else 'unknown device'

        if device=='unknown device':
            continue

        if action == 'connected':

            say = f"echo {device} connected"
            print(say)
        else:

            say = f"echo {device} disconnected"
            print(say)







def main():

    old_macs = scan(NETWORK)

    connection_change(old_macs, "connected")

    while True:

        time.sleep(INTERVAL)

        macs = scan(NETWORK)



        new = macs - old_macs

        connection_change(new, "connected")



        left = old_macs - macs

        connection_change(left, "disconnected")



        old_macs = macs





if __name__ == "__main__":

    main()