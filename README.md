# grandExchange
A python and MariaDB solution to query the Jagex grand exchange webpages and store recent price data to a database.

## Included files:
**iid name.txt** - a list of item ID and name, where each item is separated by a newline

### Usage information:
**DATABASE**
MariaDB [(none)]> CREATE DATABASE grandexchange;
Query OK, 1 row affected (0.00 sec)

MariaDB [(none)]> USE grandexchange
Database changed
MariaDB [grandexchange]> CREATE USER 'ge'@'localhost' IDENTIFIED BY 'password';
Query OK, 0 rows affected (0.00 sec)

MariaDB [grandexchange]> GRANT ALL PRIVILEGES ON grandexchange.* TO 'ge'@'localhost';
Query OK, 0 rows affected (0.00 sec)

MariaDB [grandexchange]> FLUSH PRIVILEGES;
Query OK, 0 rows affected (0.00 sec)

**TABLES**
MariaDB [grandexchange]> CREATE TABLE itemNames (iid INT NOT NULL, itemName VARCHAR(100) NOT NULL, PRIMARY KEY ( iid ));
Query OK, 0 rows affected (0.01 sec)

MariaDB [grandexchange]> CREATE TABLE currentRunedate (runedate INT NOT NULL);
Query OK, 0 rows affected (0.01 sec)

MariaDB [grandexchange]> CREATE TABLE itemPrices (iid INT NOT NULL, itemPrice INT NOT NULL, runedate INT NOT NULL);
Query OK, 0 rows affected (0.00 sec)


