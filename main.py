from tkinter import messagebox
from database import MosqueDB
from mosque import Mosque
from tkinter import *
import folium
import webbrowser
import os


def displayAll(mdb,resultList):
  resultList.delete(0,END)
  records = mdb.display()
  clearFields()
  for i in records:
    resultList.insert(END, i.getDetails())
  
def searchName(mdb, resultList,name):
  resultList.delete(0,END)
  name = name.strip()
  i = mdb.search(name)
  if i == 0 :
     messagebox.showwarning("Not found", f"There is no mosque named {name}.")
     return
     
  recordText = i.getDetails()
  resultList.insert(END,recordText)
  clearFields()

def addEntry(mdb, mosque):
    try:
        resultsList.delete(0,END)
        mdb.insert(mosque)
        messagebox.showinfo("Success", f"Mosque '{mosque.name}' added successfully.")
        clearFields()
    except Exception as e:
        messagebox.showerror("Insert Failed", f"Error: {e}")

def deleteEntry(mdb, mid):
   try:
      resultsList.delete(0,END)
      rows = mdb.delete(mid)
      if rows == 0:
         messagebox.showwarning("Failed", f"No mosque with ID {mid} exists!")
         return
      messagebox.showinfo("Success", f"Mosque ID '{mid}' removed successfully.")
      clearFields()
   except Exception as e:
      messagebox.showerror("Delete Failed", f"Error: {e}")

def updateEntry(mdb):
   try:
      mosque = Mosque(
            id=idEntry.get(),
            name=nameEntry.get(),
            mtype=value_inside.get(),
            address=addrEntry.get(),
            coor=coorEntry.get(),
            imamName=imamEntry.get()
        )
      rows = mdb.update(mosque)
      if rows == 0:
        messagebox.showwarning("Not Found", f" no Mosque with ID {mosque.id} was found.")
      else:
        messagebox.showinfo("Success", f"Mosque ID {mosque.id} updated.")
        clearFields()
   except Exception as e:
      messagebox.showerror("Update Failed", f"Error: {e}")

def displayMap():
    coords = coorEntry.get().strip()

    if not coords:
        messagebox.showwarning("No Coordinates", "Please select or enter a mosque with coordinates.")
        return

    try:
        lat, lon = map(float, coords.split(','))

        map_obj = folium.Map(location=[lat, lon], zoom_start=17)
        folium.Marker([lat, lon], tooltip="Mosque Location").add_to(map_obj)

        map_path = os.path.abspath("mosque_map.html")
        map_obj.save(map_path)
        webbrowser.open(f"file://{map_path}")
    except Exception as e:
        messagebox.showerror("Map Error", f"Could not display map: {e}")


def on_select(event):
    clearFields()
    try:
        selection = event.widget.curselection()
        if not selection:
            return
        index = selection[0]
        selected_text = event.widget.get(index)

        id_str = selected_text.split('|')[0].strip().split(':')[1].strip()
        record = mdb.searchById(id_str)

        if record:
            idEntry.insert(0, record.id)
            nameEntry.insert(0, record.name)
            value_inside.set(record.mtype)
            addrEntry.insert(0, record.address)
            coorEntry.insert(0, record.coor)
            imamEntry.insert(0, record.imamName)

    except Exception as e:
        messagebox.showerror("Error", f"Could not load entry: {e}")

def clearFields():
  idEntry.delete(0, END)
  nameEntry.delete(0, END)
  addrEntry.delete(0, END)
  coorEntry.delete(0, END)
  imamEntry.delete(0, END)
  value_inside.set("Select")

mdb = MosqueDB()
root = Tk()

root.title('Mosques Management System')
window_width = 1000
window_height = 200

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

x = int((screen_width / 2) - (window_width / 2))
y = int((screen_height / 2) - (window_height / 2))


root.geometry(f"{window_width}x{window_height}+{x}+{y}")


root.grid_columnconfigure(1, weight=1)  


entriesFrame = Frame(root)
listFrame = Frame(root)
buttonsFrame = Frame(root)

entriesFrame.grid(column=0,row=0, sticky='nse')
listFrame.grid(column=1,row=0,rowspan=2, sticky='nsew')
buttonsFrame.grid(column=0,row=1,sticky='nse')

# Entries Frame components
idLabel = Label(entriesFrame, text='ID')
nameLabel = Label(entriesFrame, text='Name')
typeLabel = Label(entriesFrame, text='Type')
addrLabel = Label(entriesFrame, text='Address')
coorLabel = Label(entriesFrame, text='Coordinates')
imamNameLabel = Label(entriesFrame, text='Imam Name')
idEntry = Entry(entriesFrame)
nameEntry = Entry(entriesFrame)
options_list = ['Jamea', 'Masjid']
value_inside = StringVar(entriesFrame) 
value_inside.set("Select") 
typeEntry = OptionMenu(entriesFrame,value_inside, *options_list)
addrEntry = Entry(entriesFrame)
coorEntry = Entry(entriesFrame)
imamEntry = Entry(entriesFrame)
idLabel.grid(column=0,row=0,pady=4,padx=3)
idEntry.grid(column=1,row=0,pady=4,padx=3)
nameLabel.grid(column=2,row=0,pady=4,padx=3)
nameEntry.grid(column=3,row=0,pady=4,padx=3)
typeLabel.grid(column=0,row=1,pady=4,padx=3)
typeEntry.grid(column=1,row=1,pady=4,padx=3)
addrLabel.grid(column=2,row=1,pady=4,padx=3)
addrEntry.grid(column=3,row=1,pady=4,padx=3)
coorLabel.grid(column=0,row=2,pady=4,padx=3)
coorEntry.grid(column=1,row=2,pady=4,padx=3)
imamNameLabel.grid(column=2,row=2,pady=4,padx=3)
imamEntry.grid(column=3,row=2,pady=4,padx=3)

# Button Frame components
displayButton = Button(buttonsFrame,text='Display All',command=lambda: displayAll(mdb, resultsList))

searchButton =  Button(buttonsFrame,text='Search By Name', command=lambda: searchName(mdb,resultsList,nameEntry.get()))

addButton = Button(buttonsFrame,text='Add Entry', command=lambda:
                    addEntry(
  mdb,
  Mosque(
      id=idEntry.get(),
      name=nameEntry.get(),
      mtype=value_inside.get(),
      address=addrEntry.get(),
      coor=coorEntry.get(),
      imamName=imamEntry.get()
  )
)
)

deleteButton = Button(buttonsFrame,text='Delete Entry', command=lambda:
                      deleteEntry(mdb,idEntry.get()))

displayMapButton = Button(buttonsFrame,text='Display on Map', command=displayMap)
updateButton = Button(buttonsFrame,text='Update Entry', command=lambda: updateEntry(mdb))
displayButton.grid( column=0,row=0,padx=3,pady=3,sticky='nsew')
searchButton.grid( column=1,row=0,padx=3,pady=3,sticky='nsew')
updateButton.grid( column=2,row=0,padx=3,pady=3,sticky='nsew')
addButton.grid( column=0,row=1,padx=3,pady=3,sticky='nsew')
deleteButton.grid( column=1,row=1,padx=3,pady=3,sticky='nsew')
displayMapButton.grid( column=2,row=1,padx=3,pady=3,sticky='nsew')

# List Framw components
scrollbar = Scrollbar(listFrame)

resultsList = Listbox(listFrame, yscrollcommand=scrollbar.set)

resultsList.bind('<<ListboxSelect>>', on_select)

resultsList.pack(side=LEFT, fill=BOTH, expand=True)
scrollbar.pack(side=RIGHT, fill=Y)
scrollbar.config(command=resultsList.yview)


root.mainloop()
