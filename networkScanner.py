from scapy.all import ARP, Ether, srp
import socket
import schedule
import time
from datetime import datetime
import pandas as pd
import subprocess
import netifaces as nf
import warnings
warnings.filterwarnings('ignore')

def masterDevice():
    masterDeviceName = socket.gethostname()
    masterDeviceIP = socket.gethostbyname(masterDeviceName)
    return masterDeviceName, masterDeviceIP

def getWifiIP():
    wifi_iface = nf.gateways()['default'][nf.AF_INET][1]
    wifi_ip = None
    for iface in nf.interfaces():
        addrs = nf.ifaddresses(iface)
        if iface == wifi_iface and nf.AF_INET in addrs:
            wifi_ip = addrs[nf.AF_INET][0]['addr']
            break

    #change the last digit of the IP address to 0
    wifi_ip = wifi_ip.rsplit('.', 1)[0] + '.0'
    return wifi_ip

def job():
    print("Getting WiFi IP.....")
    wifiIP = getWifiIP()
    if wifiIP:
        print("WiFi IP address: " + wifiIP)
        print("Start Scanning.....")

        df = pd.DataFrame(columns=['Master Device', 'Name', 'IP', 'MAC'])
        packet = Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=f"{wifiIP}/24") # Create ARP request packet

        print("Scanning device.....")

        results = srp(packet, timeout=3, verbose=0)[0]

        print("Generating results.....")

        devices = []
        for result in results: # 0 = sent packet, 1 = received packet
            devices.append({'ip': result[1].psrc, 'mac': result[1].hwsrc})

        currentDateTime = datetime.now()

        print("Devices connected to WiFi at "+ currentDateTime.strftime("%d/%m/%Y %H:%M:%S") + ":")

        for device in devices:
            try:
                name = socket.gethostbyaddr(device['ip'])[0]
            except socket.herror:
                name = 'Unknown'

            df = df.append({'Master Device':"", 'Name': name, 'IP': device['ip'], 'MAC': device['mac']}, ignore_index=True)

        #Check master device
        masterDeviceName, masterDeviceIP = masterDevice()
        df['Master Device'] = df['Name'].apply(lambda x: '*' if x == masterDeviceName else '')
        df['Master Device'] = df['IP'].apply(lambda x: '*' if x == masterDeviceIP else '')

        print(df)

        #Analyse the Total number of devices connected to WiFi
        totalDevices = len(df.index)
        print("Total Devices Connected to WiFi: " + str(totalDevices))
        knownDevices = len(df[df['Name'] != 'Unknown'].index)
        print("Known Devices Connected to WiFi: " + str(knownDevices))
        unknownDevices = len(df[df['Name'] == 'Unknown'].index)
        print("Unknown Devices Connected to WiFi: " + str(unknownDevices))

    else:
        print("Could not find WiFi IP address")


schedule.every(1).minutes.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)