import MySQLdb
import urllib, json
import time
from datetime import datetime

def selectRunedate(cursor):     #obtain the most recent runedate that we have prices for
    cursor.execute("""SELECT max(runedate) FROM runedates""")
    runedate = cursor.fetchone()

    return runedate

def fetchRecentRunedate():      #obtain the last runedate jagex updated grand exchange
    try:
        url = "http://secure.runescape.com/m=itemdb_rs/api/info.json"
        response = urllib.urlopen(url)
        responseData = json.loads(response.read())
        recentRunedate = responseData["lastConfigUpdateRuneday"]
    except:
        print "could not retrieve most recent Runedate...\n"

    return recentRunedate

def selectItemIDList(cursor):   #generate a list of iid to request new pricing data with
    try:                                                    #get the item ID of all items
        cursor.execute("""SELECT DISTINCT iid FROM itemNames""")
        data = curs.fetchall()
        idList = []                                         #store each item ID into idList[]
        for value in data:
            idList.append(value[0])
    except:
        print "could not select iid from itemNames...\n"

    return idList

def requestNewPrice(iid):       #obtain an items new price from jagex
    try:
        url = "http://services.runescape.com/m=itemdb_rs/api/graph/" + str(iid) + ".json"
        response = urllib.urlopen(url)
        data = json.loads(response.read())
        dailyData = data["daily"]
        dailyKeys = []
        for k in dailyData:
            dailyKeys.append(k)
        dailyKeys.sort()
        lastKey = len(dailyKeys) - 1
        newPrice = dailyData[dailyKeys[lastKey]]
        print "iid: ", iid, " with current price: ", newPrice, "\n"
        return newPrice     #returns the requested new price if successful..
    except:
        print "unable to connect to website...", iid, "\n"
        return 0            #..or 0 if unable to fetch price



def updateItemPrices(idList, rdate, curs, conn):
    for iid in idList:
    #    print iid
        updatedPrice = requestNewPrice(iid)
        print "updt price: ", updatedPrice, "\n"
        if updatedPrice != 0:   #valid price obtained
            try:
                curs.execute("""INSERT INTO itemPrices (iid, itemPrice, runedate) VALUES (%s, %s, %s)""", (iid, updatedPrice, rdate))
                conn.commit()
                print "insert success, time for sleep..\n"

            except:
                print "connection rolling back..."
                conn.rollback()

        time.sleep(1)


        #except:
            #print "unable to connect to website for iid: ", iid, "\n"
            #pass
            #time.sleep(5)

    return

def updateRunedate(rdate, curs, conn):
    try:
        realdate = datetime.now()
        curs.execute("""INSERT INTO runedates (runedate, realdate) VALUES (%s, %s)""", (rdate, realdate))
        conn.commit()
    except:
        print "could not update runedate, rolling back.."
        conn.rollback()

    return

if __name__ == "__main__":
    myDB = "grandexchange"

    try:
        conn = MySQLdb.connect(host="localhost",
                                user="ge",
                                passwd="password",
                                db=myDB)
        curs = conn.cursor()
        print "connected to db"

        myRunedate = selectRunedate(curs)
        jagRunedate = fetchRecentRunedate()

        if (myRunedate[0] != jagRunedate):          #our data needs an update
            print "dates do not match.."
            iidList = selectItemIDList(curs)
            for iid in iidList:
                print "itemID: ", iid
        #    print "got iidl"
            updateItemPrices(iidList, jagRunedate, curs, conn)  #try to update every item
            print "finished updating item prices..."
            updateRunedate(jagRunedate, curs, conn)         #finally, update our last completed update to the current runedate
            print "updated newest runedate, time to quit.."

        else:
            print "runedate matches...database up to date!"

    except:
        print "could not connect to database: " + myDB + "\n"

    conn.close()
