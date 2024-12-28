import mysql.connector

connection = mysql.connector.connect(host='localhost',user='root',passwd='MySQL_316497',database='file_backup_system') 

if connection.is_connected ():
    print("basarili")

cursor = connection.cursor()   
