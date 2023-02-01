import nltk
nltk.download('averaged_perceptron_tagger')
nltk.download('punkt')

endpointList = []

with open('./TestData/BookController.cs', 'r') as file:
    for line in file:
        # find HttpGet and HttpPost and HttpPut and HttpDelete, print the line
        if "HttpGet" in line or "HttpPost" in line or "HttpPut" in line or "HttpDelete" in line:
            #remove space and store the line in a list
            line = line.replace(" ", "")
            endpointList.append(line)
            
    #loop through the list and print the endpoint
    for line in endpointList:
        currentEndPoint = line.split('"')[1]
        
        if ("get" in currentEndPoint) or ("update" in currentEndPoint):
            print("GET: " + currentEndPoint)
        
