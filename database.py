import sqlite3
from mosque import Mosque

class MosqueDB:
  def __init__(self):
    self.conn = sqlite3.connect('mosquesDB.db')
    self.cur = self.conn.cursor()
    self.cur.execute("""CREATE TABLE IF NOT EXISTS mosque
                      (ID INTEGER PRIMARY KEY NOT NULL,
                      name TEXT NOT NULL,
                      type TEXT NOT NULL,
                      address TEXT,
                      coordinates TEXT,
                      imam_name TEXT
                     )
                     """)
    self.conn.commit()
  
  def display(self):
    self.cur.execute("SELECT * FROM mosque")
    records = self.cur.fetchall()
    mosques = []
    for i in records:
      mosque = Mosque(id= i[0], name=i[1], mtype=i[2],address=i[3], coor=i[4],imamName=i[5])
      mosques.append(mosque)
    return mosques
  
  def search(self, name):
    self.cur.execute("SELECT * FROM mosque WHERE name LIKE ?", ('%' + name + '%',))
    i = self.cur.fetchone()
    mosque = Mosque(id= i[0], name=i[1], mtype=i[2],address=i[3], coor=i[4],imamName=i[5])
    return mosque
  
  def searchById(self,id):
    self.cur.execute("SELECT * FROM mosque WHERE ID = ?", (id,))
    i = self.cur.fetchone()
    mosque = Mosque(id= i[0], name=i[1], mtype=i[2],address=i[3], coor=i[4],imamName=i[5])
    return mosque
 
  def insert(self,mosque ):
    self.cur.execute("""INSERT INTO mosque VALUES (?,?,?,?,?,?)""", (mosque.id,mosque.name,mosque.mtype,mosque.address,mosque.coor,mosque.imamName,))
    self.conn.commit()

  def delete(self, mID):
    self.cur.execute("DELETE FROM mosque WHERE ID=?", (mID,))
    self.conn.commit()

  def update(self, mosque):
    self.cur.execute("""
                     UPDATE mosque SET
                     name = ?,
                     type = ?,
                     address = ?,
                     coordinates = ?,
                     imam_name = ?
                     WHERE ID = ?
                      """, (mosque.name,mosque.mtype,mosque.address,mosque.coor,mosque.imamName,mosque.id))
    self.conn.commit()
    return self.cur.rowcount
  def __del__(self):
    self.conn.close()