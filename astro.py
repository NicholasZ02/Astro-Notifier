import requests
import config
import os
from datetime import date

#Latitude and Longitude come from configuation file.
URL = "https://www.7timer.info/bin/api.pl?"
params = {
    "lat": config.LAT,
    "lon": config.LON,
    "product": 'astro',
    "unit": 'british',
    "output": 'json',
}

try:
    weatherResponse = requests.get(url=URL, params=params).json()
except:
    quit()

#Uses the API scale from 1(Good)-8(Bad) to give weather descriptions.
def quality(x):
    if(x <= 2):
        return "Excellent"
    elif(x <= 4):
        return "Good"
    elif(x <= 6):
        return "Fair"
    else:
        return "Poor"

#Accessing the first few entries which relate to the current and next day over a period of 12 hours.
#The range and added values change depending on the hour the program runs because of the API.
#Add a value of 7 when done around 3:00, add a value of 1 when done around 6:00, add a value of 19 at 11:00.
#Switch AM/PM when done in AM or PM.
message = ""
goodClouds = False
for data in weatherResponse['dataseries'][:5]:
    time = data['timepoint'] + 1 % 12
    if(time < 12):
        message += f"{time} PM: "
    elif(time > 24):
        message += f"{time-24} PM: "
    else:
        message += f"{time-12} AM: "
    
    cloudCover = data['cloudcover']
    if(cloudCover <= 5):
        message += f"Up to {cloudCover}0% cloud coverage, "
        goodClouds = True
    else:
        message += f"Up to {cloudCover+1}0% cloud coverage, "

    message += f"{quality(data['transparency'])} transparency, {quality(data['seeing'])} seeing.\n\n"

#Pushover API Notifier. Only send a message under ideal conditions.
if(goodClouds):
    pushoverURL = "https://api.pushover.net/1/messages.json"
    imageURL = f"https://www.7timer.info/bin/astro.php?lon={config.LON}&lat={config.LAT}&lang=en&ac=0&unit=metric&output=internal&tzshift=0"
    try:
        imageResponse = requests.get(imageURL)
        with open("Forecast.jpg", "wb") as f:
            f.write(imageResponse.content)
    except:
        pass
    title = f"Forecast for {date.today().strftime('%m/%d/%y')}"
    pushoverData = {"token": config.APPLICATION_TOKEN,
                    "user": config.USER_TOKEN,
                    "title": title,
                    "message": message}
    try:
        pushoverImage={"attachment": open("Forecast.jpg","rb")}
        requests.post(url=pushoverURL, data=pushoverData, files=pushoverImage)
        os.remove("Forecast.jpg")
    except:
        try:
            requests.post(url=pushoverURL, data=pushoverData)
        except:
            quit()
