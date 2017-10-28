# readFile.py
    # reads a text file line by line of the form "itemID - itemName | itemCategory"
    # and splits each line with delims - and |
    # and uses these values to initialize MariaDB tables

#imports
    #MySQLdb - python interface for MariaDB
import MySQLdb

myDB = "grandexchange"      #name of database

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


for line in file:                           #operate on the file line by line
    try:    #attempt to operate on the line
        lineS = line.strip()                #get rid of any newline characters
        if lineS == "":         #empty line with no data
            continue

        lineParts = lineS.split(" - ")      #split the line into [id] and [name | category] bits
        if lineParts[0] == '\xef\xbb\xbf':              #first line was displaying UTF-8 encoded BOM info
            continue                                        #..so if we obtain BOM info, continue loop

        #print "lineS: ", lineS
        #print "lineParts: ", lineParts
        itemID = lineParts[0]
        lineParts = lineParts[1].split(" | ")   #split [name | category] bit
        itemName = lineParts[0]
        itemCategory = lineParts[1]
#        print "item ID: ", itemID, "item name: ", itemName, "item category: ", itemCategory

        try:
            curs.execute("""INSERT INTO itemNames (iid, itemName) VALUES (%s, %s)""", (itemID, itemName))
            conn.commit()
            #print "committed to database...\n"
        except:
            conn.rollback()
            print "rolling back database...\n"

        try:
            curs.execute("""INSERT INTO itemCategorys (iid, itemCategory) VALUES (%s, %s)""", (itemID, itemCategory))
            conn.commit()
            #print "committed to database...\n"
        except:
            conn.rollback()
            print "rolling back database...\n"

    except:     #unable to operate on the current line
        pass


print "got to end successfully!"
conn.close()
file.close()
