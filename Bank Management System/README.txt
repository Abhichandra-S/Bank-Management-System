Prerequisites:

1. Python: Ensure Python is installed on your system. The code is compatible with Python 3.x.

Installation:
Download Python from python.org.

2. MySQL Server: The code uses MySQL for database management. You need to have MySQL Server installed and running.

Installation:
Download MySQL Community Server from dev.mysql.com.

3. MySQL Connector for Python: This is a Python library that allows Python to interact with MySQL databases.

pip install mysql-connector-python

4.Tkinter: Tkinter is used for the graphical user interface (GUI). It is included with Python, but if it’s not installed on your system, you might need to install it separately.

sudo apt-get install python3-tk


ADDITIONAL STEP

1. Create the Database and Tables: Ensure you create the Bank database in MySQL before running the code:
CREATE DATABASE Bank;

2. Modify Database Connection Settings: Make sure to adjust the connect_db function if your MySQL configuration differs (e.g., if you are using a different username, password, or host).


CHECK LIST:

Python (>= 3.x)
MySQL Server
MySQL Connector for Python: pip install mysql-connector-python
Tkinter (usually included with Python, otherwise install separately)