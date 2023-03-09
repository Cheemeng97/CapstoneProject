from flask import *
from werkzeug.utils import secure_filename
import os
import requests
from Logic.CheckStatusCode.HttpStatusErrorCodeChecker import httpStatusErrorCodeChecker
from Logic.CheckSSL.ssl_checker import SSL_Checker
from Logic.getMainUrl import getMainUrl
from Logic.BestPractice.docType_checker import docTypeChecker
from Logic.BestPractice.xss_checker import xssChecker

UPLOAD_FOLDER = './uploads'

app = Flask(__name__) 
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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
    if request.method == 'POST':
        if 'Register' in request.form:
            studentID = request.form['studentID']
            moduleCode = request.form['moduleCode']
            macAddress = request.form['macAddress']

            print(studentID, moduleCode, macAddress)
    else:   
        return render_template("register.html")


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
