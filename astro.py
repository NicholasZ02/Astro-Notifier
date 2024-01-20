import requests

#Fixed latitude and longitude for Newark
URL = "https://www.7timer.info/bin/api.pl?"
params = dict(
    lon = -74.1741,
    lat = 40.7355,
    product = 'astro',
    unit = 'british',
    output = 'json'
)
r = requests.get(URL, params).json()

#Accessing the first 5 entries which relate to the current day.
for i in range(5):
    hour = r['dataseries'][i]['timepoint'] + 1 % 12
    if(hour < 12):
        print(f"{hour} PM, ", end='')
    else:
        print(f"{hour-12} AM, ", end='')
    
    cloudCover = r['dataseries'][i]['cloudcover']
    if(cloudCover < 5):
        print(f"up to {cloudCover}0% cloud coverage. ", end='')
    else:
        print(f"up to {cloudCover+1}0% cloud coverage. ", end='')

    seeing = r['dataseries'][i]['seeing']
    if(seeing <= 2):
        print("Good seeing, ", end='')
    elif(seeing <= 4):
        print("Average seeing, ", end='')
    elif(seeing <= 6):
        print("Poor seeing, ", end='')
    else:
        print("Bad seeing, ", end='')

    transparency = r['dataseries'][i]['transparency']
    if(transparency <= 2):
        print("Good transparency.")
    elif(seeing <= 4):
        print("Average transparency.")
    elif(seeing <= 6):
        print("Poor transparency.")
    else:
        print("Bad transparency.")