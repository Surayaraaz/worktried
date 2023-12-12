import sys
import json
import moni
import mysql.connector
from datetime import date


connectiondb = mysql.connector.connect(host="localhost", user="root",
                                       password="", database="developtreeshrms", port=3306)
cursordb = connectiondb.cursor()
print(connectiondb)



json_object = json.loads(sys.argv[1])
employee_id = json_object.get("employee_id")  # Assuming the employee ID is included in the JSON data


for w, t in moni.show_activity():
    today = date.today()
    sql = "INSERT INTO MonitoringDetails (md_title, md_total_time_seconds, md_date , employee_id) VALUES (%s,%s, %s, %s)" 
    val = (w,t, today, employee_id)
    cursordb.execute(sql, val)
    connectiondb.commit()
    print(cursordb.rowcount, "record inserted.")
 
