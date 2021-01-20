from tkinter import *
from PIL import ImageTk,Image
import sqlite3

root = Tk()
root.title("Contacts")
root.geometry("300x250")

# connect to database
connection = sqlite3.connect ("contacts_book.db")

# create cursor
cur = connection.cursor()

# create table
'''cur.execute ("""CREATE TABLE contacts (
	first_name text,
	last_name text,
	phone_number integer)""")'''

# functions 
def submit ():
	connection = sqlite3.connect("contacts_book.db")
	cur = connection.cursor()
	cur.execute ("INSERT INTO contacts VALUES (:first_name, :last_name, :phone_number)",
		{
                "first_name": first_name.get (),
                "last_name": last_name.get (),
                "phone_number": phone_number.get ()      
		})
	# commit changes to database
	connection.commit()
	# close connection
	connection.close ()

	# clear text boxes
	first_name.delete (0, END)
	last_name.delete (0, END)
	phone_number.delete (0, END)

def see_all ():
	connection = sqlite3.connect("contacts_book.db")
	cur = connection.cursor()
	cur.execute ("SELECT *, oid FROM contacts")
	records = cur.fetchall ()
    
    # loop through results
	print_records = ""
	for record in records:
		print_records += str(record[0]) + " " + str(record[1]) + " " + "\t" +str(record[2]) + "\n"

	see_all_label = Label (root, text = print_records)
	see_all_label.grid (row = 5, column = 0, columnspan = 2)

# create text boxes
first_name = Entry (root, width = 30)
first_name.grid (row =0, column = 1, padx = 20)
last_name = Entry (root, width = 30)
last_name.grid (row =1, column = 1)
phone_number = Entry (root, width = 30)
phone_number.grid (row =2, column = 1)

# create labels
first_name_label = Label (root, text = "First Name")
first_name_label.grid (row = 0, column =  0)
last_name_label = Label (root, text = "Last Name")
last_name_label.grid (row = 1, column =  0)
phone_number_label = Label (root, text = "Phone Number")
phone_number_label.grid (row = 2, column = 0)

# create submit button
submit_btn = Button (root, text = "Add Contact", command = submit)
submit_btn.grid (row = 3, column = 0, columnspan = 2, pady = 10, padx = 10, ipadx = 30)

# create see_all button
see_all_btn = Button (root, text = "Show All Contacts", command = see_all)
see_all_btn.grid (row = 4, column = 0, columnspan = 2, pady = 10, padx = 10, ipadx = 20)




# commit changes to database
connection.commit()

# close connection
connection.close ()


root.mainloop ()