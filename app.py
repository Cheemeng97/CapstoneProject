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

UPLOAD_FOLDER = './uploads'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

############################# Background services #########################################

def start_networkScannerJob():
    subprocess.Popen(['python', 'networkScanner.py'])


def start_checkRegistrationRecordsJob():
    subprocess.Popen(['python', 'checkingRecords.py'])
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
    

@app.route("/result_codeAnalysis", methods=["POST", "GET"])
def code_analyse():
    if request.form['action'] == 'Submit_File':
        if (request.method == "POST"):

            code = request.form["code"]
            if not code:
                return "Error: Code input cannot be empty."
            else:
                return render_template("result_codeAnalysis.html", code=code)
        


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
    collection.insert_one(data)
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


if __name__ == "__main__":
    start_networkScannerJob()
    start_checkRegistrationRecordsJob()
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(debug=False,port=4949)




