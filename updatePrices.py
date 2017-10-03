import MySQLdb
import urllib, json
import time

myDB = "grandexchange"

try:
    conn = MySQLdb.connect(host="localhost",
                            user="ge",
                            passwd="password",
                            db=myDB)
    curs = conn.cursor()
    print "connected to db"
except:
    print "could not connect to database " + myDB + "\n"

try:                                                    #get the item ID of all items
    curs.execute("""SELECT iid FROM itemNames""")
    data = curs.fetchall()
    idList = []                                         #store each item ID into idList[]
    for value in data:
        idList.append(value[0])
except:
    print "could not execute select statement...\n"



for iid in idList:
#    print iid
    try:
        url = "http://services.runescape.com/m=itemdb_rs/api/graph/" + str(iid) + ".json"
#        print url
        response = urllib.urlopen(url)
        data = json.loads(response.read())    
        dailyData = data["daily"]
        dailyKeys = []
        for k in dailyData:
            dailyKeys.append(k)        
        dailyKeys.sort()
        lastKey = len(dailyKeys) - 1
        recentPrice = dailyData[dailyKeys[lastKey]]
#        print "iid: ", iid, " with current price: ", recentPrice, "\n"
        time.sleep(1)
    except:
        print "unable to connect to website...\n"







conn.close()
