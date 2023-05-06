from openwrt_luci_rpc import OpenWrtRpc

router = OpenWrtRpc('192.168.168.1', 'root', 'cheemeng')
result = router.get_all_connected_devices(only_reachable=True)

print("Connected")
for device in result:
   mac = device.mac
   name = device.hostname
   ip = device.ip
   connectedTime = device.
   
   print(ip)
   # convert class to a dict
   device_dict = device._asdict()



#when they connect
#when they disconnect
#how long they connect
#hostname
#ip address