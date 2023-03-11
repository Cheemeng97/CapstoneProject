from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client['CapstoneProject']
collection_registration = db['Registration']
collection_networkScanRecord = db['NetworkScanRecord']

macAddressList_registration = []
for x in collection_registration.find():
    macAddressList_registration.append(x['macAddress'])

macAddressList_networkScanRecord = []
for x in collection_networkScanRecord.find():
    macAddressList_networkScanRecord.append(x['MAC'])

nameList_networkScanRecord = []
for x in collection_networkScanRecord.find():
    nameList_networkScanRecord.append(x['Name'])

# 1 - registered by student and appear in network scan record # green
# 2 - registered by student but not appear in network scan record # red
# 3 - not registered by student but appear in network scan record # orange

for macAddress in macAddressList_registration:
    print(macAddress)
    if macAddress in macAddressList_networkScanRecord:
        collection_checkRegistrationRecords = db['CheckRegistrationRecords']
        collection_checkRegistrationRecords.insert_one({
            'macAddress': macAddress,
            'status': '1'
            })
    else:
        collection_checkRegistrationRecords = db['CheckRegistrationRecords']
        collection_checkRegistrationRecords.insert_one({
            'macAddress': macAddress,
            'status': '2'
            })
        
for macAddress in macAddressList_networkScanRecord:
    if macAddress not in macAddressList_registration:
        collection_checkRegistrationRecords = db['CheckRegistrationRecords']
        collection_checkRegistrationRecords.insert_one({
            'macAddress': macAddress,
            'status': '3'
            })