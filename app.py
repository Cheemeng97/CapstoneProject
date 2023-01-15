from flask import * #importing flask (Install it using python -m pip install flask)
import requests
from Logic.CheckStatusCode.HttpStatusErrorCodeChecker import httpStatusErrorCodeChecker

app = Flask(__name__) #initialising flask


@app.route("/") #defining the routes for the home() funtion (Multiple routes can be used as seen here)
@app.route("/home")
def home():
    return render_template("home.html") #rendering our home.html contained within /templates

@app.route("/result", methods=["POST", "GET"]) #defining the routes for the account() funtion
def analyse():
    url = "<API Endpoint Not Defined>" #Creating a variable url

    if (request.method == "POST"): #Checking if the method of request was post
        url = request.form["url"] #getting the name of the user from the form on home page

        if not url: #if name is not defined it is set to default string
            url = "<API Endpoint Not Defined>"

        #response = requests.get(url)
        # print(response.status_code)

        #HttpStatusErrorCodeChecker_range_result, HttpStatusErrorCodeChecker_code_result = httpStatusErrorCodeChecker(response.status_code)
        #print(HttpStatusErrorCodeChecker_range_result)
        #print(HttpStatusErrorCodeChecker_code_result)

    return render_template("result.html",url=url) #rendering our account.html contained within /templates



if __name__ == "__main__": #checking if __name__'s value is '__main__'. __name__ is an python environment variable who's value will always be '__main__' till this is the first instatnce of app.py running
    app.run(debug=True,port=4949) #running flask (Initalised on line 4)
