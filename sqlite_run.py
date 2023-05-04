import sqlite3
import datetime
import random
import time

connection = sqlite3.connect("livetest.db")

connection.execute("DROP TABLE XDATA")                       #resets the table by dropping it
connection.execute("DROP TABLE YDATA")
connection.execute("DROP TABLE ZDATA")
connection.execute('''CREATE TABLE IF NOT EXISTS XDATA
                   (sensor_name         TEXT        NOT NULL,
                    value           INT         NOT NULL,
                    time            timestamp);''' )
connection.execute('''CREATE TABLE IF NOT EXISTS YDATA
                   (sensor_name         TEXT        NOT NULL,
                    value           INT         NOT NULL,
                    time            timestamp);''' )
connection.execute('''CREATE TABLE IF NOT EXISTS ZDATA
                   (sensor_name         TEXT        NOT NULL,
                    value           INT         NOT NULL,
                    time            timestamp);''' )

timer = 0
while(1):
    timer += 1 
    getTime = datetime.datetime.now().strftime("%H:%M:%S.%f")
    currentTime = getTime[:-4]
    randomNum = random.randint(0,100)
    randomNum2 = random.randint(0, 150)
    randomNum3 = random.randint(0, 150)
    print(currentTime)
    connection.execute("INSERT INTO XDATA (sensor_name,value,time) VALUES ('Xdata', ?, ?)", (randomNum, currentTime))
    connection.execute("INSERT INTO YDATA (sensor_name,value,time) VALUES ('Ydata', ?, ?)", (randomNum2, currentTime))
    connection.execute("INSERT INTO ZDATA (sensor_name,value,time) VALUES ('Zdata', ?, ?)", (randomNum3, currentTime))
    connection.commit()
    time.sleep(0.5)

connection.close()