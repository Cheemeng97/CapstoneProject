from flask import *
from werkzeug.utils import secure_filename
import os
import datetime
from Logic.CheckStatusCode.HttpStatusErrorCodeChecker import httpStatusErrorCodeChecker
from Logic.CheckSSL.ssl_checker import SSL_Checker
from Logic.getMainUrl import getMainUrl
from Logic.BestPractice.docType_checker import docTypeChecker
from Logic.BestPractice.xss_checker import xssChecker
from pymongo import MongoClient
import subprocess
import time
from threading import Thread

UPLOAD_FOLDER = './uploads'

app = Flask(__name__) 
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

########################### Network Scanner #########################################

def run_networkScanner():
    while True:
        print('Performing network Scanning...')
        subprocess.run(['python', 'networkScanner.py'])
        time.sleep(300) # wait for 5 minutes

script_thread = Thread(target=run_networkScanner)
# script_thread.start()

########################################################################################




############################# Check Registration Records against Netwrk Scanner Results #########################################
def run_checkRegistrationRecords():
    while True:
        print('Checking Registration Records...')
        client = MongoClient('localhost', 27017)
        db = client['CapstoneProject']
        collection_registration = db['Registration']
        collection_networkScanRecord = db['NetworkScanRecord']


        #get all macc address from registration
        macAddressList_registration = []
        for x in collection_registration.find():
            macAddressList_registration.append(x['macAddress'])

        #get all macc address from network scan record
        macAddressList_networkScanRecord = []
        for x in collection_networkScanRecord.find():
            macAddressList_networkScanRecord.append(x['MAC'])

        # 1 - registered by student and appear in network scan record # green
        # 2 - registered by student but not appear in network scan record # red
        # 3 - not registered by student but appear in network scan record # orange

        for macAddress in macAddressList_networkScanRecord:
            #appeared in both registration and network scan record
            if macAddress in macAddressList_registration:
                collection_checkRegistrationRecords = db['CheckRegistrationRecords']
                collection_checkRegistrationRecords.insert_one({
                    'macAddress': macAddress,
                    'status': '1'
                    })
            #appeared in network scan record but not in registration
            elif macAddress not in macAddressList_registration:
                collection_checkRegistrationRecords = db['CheckRegistrationRecords']
                collection_checkRegistrationRecords.insert_one({
                    'macAddress': macAddress,
                    'status': '3'
                    })

        for macAddress in macAddressList_registration:
            #appeared in registration but not in network scan record
            if macAddress not in macAddressList_networkScanRecord:
                collection_checkRegistrationRecords = db['CheckRegistrationRecords']
                collection_checkRegistrationRecords.insert_one({
                    'macAddress': macAddress,
                    'status': '2'
                    })
                
        print('Done Checking Registration Records...')
        subprocess.run(['python', 'networkScanner.py'])
        time.sleep(120) # 2 minutes


checkRegistrationRecords_thread = Thread(target=run_checkRegistrationRecords)
checkRegistrationRecords_thread.start()
#################################################################################################################################



def db_registration():
    client = MongoClient('localhost', 27017)
    db = client['CapstoneProject']
    collection = db['Registration']
    return collection

@app.route("/") 
@app.route("/home")
def home():
    return render_template("home.html") 

@app.route("/result", methods=["POST", "GET"]) 
@app.route("/result_codeAnalysis", methods=["POST", "GET"])
def analyse():
    if request.form['action'] == 'Submit_Url':
        url = "<API Endpoint Not Defined>" 

        if (request.method == "POST"): #Checking if the method of request was post
            url = request.form["url"] #getting the url from the form on home page

            if not url: #if name is not defined it is set to default string
                url = "<API Endpoint Not Defined>"

            original_url, main_url = getMainUrl(url)
            #response = requests.get(url)
            # print(response.status_code)

            #HttpStatusErrorCodeChecker_range_result, HttpStatusErrorCodeChecker_code_result = httpStatusErrorCodeChecker(response.status_code)
            #print(HttpStatusErrorCodeChecker_range_result)
            #print(HttpStatusErrorCodeChecker_code_result)

            sslChecker_results = SSL_Checker(main_url)
            docTypeChecker_contentType, docTypeChecker_result = docTypeChecker(original_url)
            xssChecker_xssProtection, xssChecker_result = xssChecker(original_url)

        return render_template("result.html",url=url,sslChecker_results=sslChecker_results, 
        docTypeChecker_contentType = docTypeChecker_contentType, docTypeChecker_result=docTypeChecker_result,
        xssChecker_xssProtection=xssChecker_xssProtection, xssChecker_result=xssChecker_result) #rendering our account.html contained within /templates



    elif request.form['action'] == 'Submit_File':
        if (request.method == "POST"):
        
            if 'file' not in request.files:
                flash('No file part')
                return redirect(request.url)

            file = request.files['file']
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            
            if file:
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                # return redirect(url_for('uploaded_file', filename=filename))
                return render_template("result_codeAnalysis.html")


@app.route("/register", methods=['GET', 'POST'])
def register():  
    return render_template("register.html")


@app.route('/save-registration-data', methods=['POST'])
def save_registration_data():
    client = MongoClient('localhost', 27017)
    db = client['CapstoneProject']
    collection = db['Registration']
    currentDateTime = datetime.datetime.now()
    currentDateTime = currentDateTime.strftime("%d/%m/%Y %H:%M:%S")   
    data = request.get_json()
    data['registeredOn'] = currentDateTime
    result = collection.insert_one(data)
    return jsonify({'message': 'Data saved to MongoDB'})


@app.route("/register-list", methods=['GET', 'POST'])
def register_list():
    client = MongoClient('localhost', 27017)
    db = client['CapstoneProject']
    collection = db['Registration']
    data = list(collection.find())

    collection = db['CheckRegistrationRecords']
    checkingData = list(collection.find())

    return render_template("register-list.html", data=data, checkingData=checkingData)

@app.route('/refreshRegistrationData')
def refresh_registration_data():
    app.logger.info('Refreshing registration data...')
    client = MongoClient('localhost', 27017)
    db = client['CapstoneProject']
    # collection = db['Registration']
    # data = list(collection.find({}, {'_id': 0}))

    collection = db['CheckRegistrationRecords']
    checkingData = list(collection.find({}, {'_id': 0}))

    # return jsonify(data, checkingData)
    return jsonify(checkingData)

# @app.route("/result_codeAnalysis", methods=["POST", "GET"])
# def code_analyse():
#     if request.form['action'] == 'Submit_File':
#         if (request.method == "POST"):
        
#             if 'file' not in request.files:
#                 flash('No file part')
#                 return redirect(request.url)

#             file = request.files['file']
#             if file.filename == '':
#                 flash('No selected file')
#                 return redirect(request.url)
            
#             if file:
#                 filename = secure_filename(file.filename)
#                 file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#                 # return redirect(url_for('uploaded_file', filename=filename))
#                 return render_template("result_codeAnalysis.html")
        
        
            # return render_template("result_codeAnalysis.html")



if __name__ == "__main__": 
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(debug=True,port=4949) 


