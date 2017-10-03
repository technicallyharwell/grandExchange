import MySQLdb
import urllib, json
import time

def selectRunedate(cursor):
    cursor.execute("""SELECT runedate FROM currentRunedate""")
    runedate = cursor.fetchone()

    return runedate

def fetchRecentRunedate():
    try:
        url = "http://secure.runescape.com/m=itemdb_rs/api/info.json"
        response = urllib.urlopen(url)
        responseData = json.loads(response.read())
        recentRunedate = responseData["lastConfigUpdateRuneday"]
    except:
        print "could not retrieve most recent Runedate...\n"

    return recentRunedate

def selectItemIDList(cursor):
    try:                                                    #get the item ID of all items
        cursor.execute("""SELECT iid FROM itemNames""")
        data = curs.fetchall()
        idList = []                                         #store each item ID into idList[]
        for value in data:
            idList.append(value[0])
    except:
        print "could not select iid from itemNames...\n"

    return idList

def updateItemPrices(idList, cursor):
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
            print "iid: ", iid, " with current price: ", recentPrice, "\n"
            time.sleep(1)
        except:
            print "unable to connect to website...\n"

    return


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

savedRunedate = selectRunedate(curs)
#print "runedate is: ", savedRunedate[0], "\n"
recentRunedate = fetchRecentRunedate()
#print "recent Runedate is: ", recentRunedate, "\n"
if (savedRunedate[0] != recentRunedate):
    itemIDs = selectItemIDList(curs)
    updateItemPrices(itemIDs, curs)

conn.close()
