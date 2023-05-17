from pymongo import MongoClient
import schedule
import time
from datetime import datetime
from Logic.sshPost_BlockWebsite import sshPost_BlockWebsite

def updatePendingWebsiteJob():
    currentTime = datetime.now()
    print("Start Update at " + str(currentTime) + " ...")

    client = MongoClient('localhost', 27017)
    db = client['CapstoneProject']
    collection_registration = db['BlockWebsite']

    # get only pending website
    pendingWebsiteList = []
    for x in collection_registration.find():
        if x['status'] == 'pending':
            pendingWebsiteList.append(x['website'])

    if len(pendingWebsiteList) == 0:
        print("No pending website to update")
        return
    else:
        for website in pendingWebsiteList:
            print(website)
            collection_registration.update_one(
                {'website': website},
                {'$set': {'status': sshPost_BlockWebsite(website)}}
            )

    print("Done Update")
            
schedule.every(30).seconds.do(updatePendingWebsiteJob)
updatePendingWebsiteJob()

while True:
    schedule.run_pending()
    time.sleep(1)