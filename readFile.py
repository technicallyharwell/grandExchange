
import MySQLdb

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

try:
    textFileName = "iid name.txt"
    file = open(textFileName, "r")
    print "opened file " + textFileName + "\n"
except:
    print "could not open file " + textFileName + "\n"


for line in file:
    lineS = line.strip()
    lineParts = lineS.split(" - ")
    if lineParts[0] == '\xef\xbb\xbf':              #first line was displaying UTF-8 encoded BOM info
        continue                                        #..so if we obtain BOM info, continue loop
    print "lineS: ", lineS
    print "lineParts: ", lineParts

    itemID = lineParts[0]
    itemName = lineParts[1:]
    itemName = itemName[0]
    print "item ID: ", itemID, "item name: ", itemName

    try:
        curs.execute("""INSERT INTO itemNames (iid, itemName) VALUES (%s, %s)""", (itemID, itemName))
        conn.commit()
        print "committed to database...\n"

    except:
        conn.rollback()
        print "rolling back database...\n"



conn.close()
file.close()
