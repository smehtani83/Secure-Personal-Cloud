import sqlite3
if __name__ == "__main__":
    con = sqlite3.connect("db.sqlite3")
    cur = con.cursor()

    cur.execute("SELECT file_file from login_file where file_name = '1'")
    for row in cur:
        blob = bytearray(row[0])
        newFile = open("filename.txt", "wb")
# write to file
        newFile.write(blob)
    
    con.close()
