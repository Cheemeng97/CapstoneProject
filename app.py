from flask import *
from werkzeug.utils import secure_filename
import os
import requests
from Logic.CheckStatusCode.HttpStatusErrorCodeChecker import httpStatusErrorCodeChecker
from Logic.CheckSSL.ssl_checker import SSL_Checker


app = Flask(__name__) 
app.config['UPLOAD_PATH'] = 'uploads'

@app.route("/") 
@app.route("/home")
def home():
    return render_template("home.html") 

@app.route("/result", methods=["POST", "GET"]) 
def analyse():
    url = "<API Endpoint Not Defined>" 

    if (request.method == "POST"): #Checking if the method of request was post
        url = request.form["url"] #getting the url from the form on home page

        if not url: #if name is not defined it is set to default string
            url = "<API Endpoint Not Defined>"


        #response = requests.get(url)
        # print(response.status_code)

        #HttpStatusErrorCodeChecker_range_result, HttpStatusErrorCodeChecker_code_result = httpStatusErrorCodeChecker(response.status_code)
        #print(HttpStatusErrorCodeChecker_range_result)
        #print(HttpStatusErrorCodeChecker_code_result)

        sslChecker_results = SSL_Checker(url)
        # print(sslChecker_results)
        

    return render_template("result.html",url=url,sslChecker_results=sslChecker_results) #rendering our account.html contained within /templates

@app.route("/result_codeAnalysis", methods=["POST", "GET"])
def code_analyse():
    if (request.method == "POST"):
        uploaded_file = request.files['file']
        filename = secure_filename(uploaded_file.filename)
        if filename != '':
            file_ext = os.path.splitext(filename)[1]
            if file_ext not in app.config['UPLOAD_EXTENSIONS']:
                abort(400)
            uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'], filename))
        return redirect(url_for('index'))
      
      
    return render_template("result_codeAnalysis.html")

if __name__ == "__main__": #checking if __name__'s value is '__main__'. __name__ is an python environment variable who's value will always be '__main__' till this is the first instatnce of app.py running
    app.run(debug=True,port=4949) #running flask (Initalised on line 4)
