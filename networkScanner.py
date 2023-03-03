from scapy.all import ARP, Ether, srp
import socket
import schedule
import time
from datetime import datetime
import pandas as pd
import subprocess
import warnings
warnings.filterwarnings('ignore')

def masterDevice():
    masterDeviceName = socket.gethostname()
    masterDeviceIP = socket.gethostbyname(masterDeviceName)
    return masterDeviceName, masterDeviceIP

# def job():
print("Start Scanning.....")

df = pd.DataFrame(columns=['Master Device', 'Name', 'IP', 'MAC'])
packet = Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst="192.168.1.0/24") # Create ARP request packet

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






# schedule.every(40).seconds.do(job)

# while True:
#     schedule.run_pending()
#     time.sleep(1)