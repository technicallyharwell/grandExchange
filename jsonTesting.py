import urllib, json
from datetime import datetime

rnow = datetime.now()
print rnow

try:
    url = "http://services.runescape.com/m=itemdb_rs/api/graph/97.json"
    response = urllib.urlopen(url)
    data = json.loads(response.read())

    dailyData = data["daily"]
    dailyKeys = []
    for k in dailyData:
        dailyKeys.append(k)

    dailyKeys.sort()
    lastKey = len(dailyKeys) - 1
    recentPrice = dailyData[dailyKeys[lastKey]]

    #print "data: \n", data
    #print "daily data: \n", dailyData
    #print "sorted daily keys: \n", dailyKeys
    print "price is: \n", recentPrice

except:
    print "unable to connect...\n"
