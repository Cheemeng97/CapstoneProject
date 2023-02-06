import nltk
import pandas as pd

result_EndPointUrl = []
result_VerbWord = []
result_HasVerb = []

def nltkFunction(input, iteration):
    VERB_CODES = {
    'VB',  # Verb, base form
    'VBD',  # Verb, past tense
    'VBG',  # Verb, gerund or present participle
    'VBN',  # Verb, past participle
    'VBP',  # Verb, non-3rd person singular present
    'VBZ',  # Verb, 3rd person singular present
    }

    hasVerb = 0
    verbWords = []

    word = nltk.word_tokenize(input)
    result = nltk.pos_tag(word) #all result
    # print(result) 
    for i in result:
        if i[1] in VERB_CODES:
            # print(i[0]) # verb word
            hasVerb = 1
            verbWords.append(i[0])
            # result_VerbWord.append(i[0])
            # result_HasVerb.append(1)

    return hasVerb, verbWords

endpointList = []

def verb_checker():
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
            currentEndPoint = currentEndPoint.replace("-", " ") # replace - with space
            
            result_EndPointUrl.append(currentEndPoint.replace(" ", "-"))  #store the endpoint in a list
            returnHasVerb, returnVerbWord = nltkFunction(currentEndPoint, line)
            result_HasVerb.append(returnHasVerb)
            result_VerbWord.append(returnVerbWord)

    return(result_EndPointUrl, result_VerbWord, result_HasVerb)
    # print(result_EndPointUrl)
    # print(result_VerbWord)
    # print(result_HasVerb)


        



