from scapy.all import ARP, Ether, srp
import socket
import schedule
import time
from datetime import datetime
import pandas as pd
import subprocess

def masterDevice():
    masterDeviceName = socket.gethostname()
    masterDeviceIP = socket.gethostbyname(masterDeviceName)
    return masterDeviceName, masterDeviceIP

# def job():

print("Start Scanning.....")

#Create datafrome to store the data
df = pd.DataFrame(columns=['Master Device', 'Name', 'IP', 'MAC'])

# Create ARP request packet
packet = Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst="192.168.50.0/24")

# Send packet and capture response
results = srp(packet, timeout=3, verbose=0)[0]

# Extract devices from response
devices = []
for result in results: # 0 = sent packet, 1 = received packet
    devices.append({'ip': result[1].psrc, 'mac': result[1].hwsrc})

currentDateTime = datetime.now()
print("Devices connected to WiFi at"+ currentDateTime.strftime("%d/%m/%Y %H:%M:%S") + ":")
# print("Name" + " "*18 + "IP" + " "*18 + "MAC")

for device in devices:
    try:
        name = socket.gethostbyaddr(device['ip'])[0]
    except socket.herror:
        name = 'Unknown'

    #store the data in dataframe
    df = df.append({'Master Device':"", 'Name': name, 'IP': device['ip'], 'MAC': device['mac']}, ignore_index=True)
    # print(f"{name}    {device['ip']:16}    {device['mac']}")

masterDeviceName, masterDeviceIP = masterDevice()

df['Master Device'] = df['Name'].apply(lambda x: '*' if x == masterDeviceName else '')
df['Master Device'] = df['IP'].apply(lambda x: '*' if x == masterDeviceIP else '')


print(df)





# schedule.every(40).seconds.do(job)

# while True:
#     schedule.run_pending()
#     time.sleep(1)