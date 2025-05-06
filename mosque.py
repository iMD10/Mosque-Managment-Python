class Mosque():
  def __init__(self,id,name,mtype,address,coor,imamName):
    self.id = id
    self.name = name
    self.mtype = mtype
    self.address = address
    self.coor = coor
    self.imamName = imamName
  
  def getDetails(self):
    return f"ID: {self.id} | Name: {self.name} | Type: {self.mtype} | Address: {self.address} | Coordinates: {self.coor} | Imam Name: {self.imamName} "

