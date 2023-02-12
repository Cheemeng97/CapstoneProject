def getMainUrl(original_url):
# original_url = "https://www.healthcare.gov/api/articles.json"
    main_url = ""
    main_url = original_url

    if "https://" in original_url:
        main_url = main_url.split("https://")[1]

    if ".gov" in main_url:
        main_url = main_url.split(".gov")[0]
        main_url = main_url + ".gov"

    if ".com" in main_url:
        main_url = main_url.split(".com")[0]
        main_url = main_url + ".com"

    return original_url, main_url