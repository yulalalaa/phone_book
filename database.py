from tkinter import *
from PIL import ImageTk,Image
import sqlite3

root = Tk()
root.title("Contacts")
root.geometry("300x400")

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
                "first_name": first_name.get(),
                "last_name": last_name.get(),
                "phone_number": phone_number.get()      
		})
	# commit changes to database
	connection.commit()
	# close connection
	connection.close()

	# clear text boxes
	first_name.delete (0, END)
	last_name.delete (0, END)
	phone_number.delete (0, END)

def see_all ():
	connection = sqlite3.connect("contacts_book.db")
	cur = connection.cursor()
	cur.execute ("SELECT *, oid FROM contacts")
	records = cur.fetchall()
    
    # loop through results
	print_records = ""
	for record in records:
		print_records += str(record[0]) + " " + str(record[1]) + " " + "\t" +str(record[3]) + " " + "\n"

	see_all_label = Label (root, text = print_records)
	see_all_label.grid (row = 5, column = 0, columnspan = 2)

def delete ():
	connection = sqlite3.connect("contacts_book.db")
	cur = connection.cursor()
	cur.execute ("DELETE FROM contacts WHERE oid = " + delete_box.get())
	connection.commit()
	connection.close()

def update ():
	connection = sqlite3.connect("contacts_book.db")
	cur = connection.cursor()

	record_id = delete_box.get()

	cur.execute ("""UPDATE contacts SET
		first_name = :first,
		last_name = :last,
		phone_number = :phone_number
		
		WHERE oid = :oid""",
        {
        "first": first_name_editor.get(),
        "last": last_name_editor.get(),
        "phone": phone_number_editor.get(),
        "oid": record_id
        })
	
	connection.commit()
	connection.close()

	editor.destroy()

def edit ():

	global editor

	editor = Tk ()
	editor.title ("Edit Contact")
	editor.geometry("300x400")

	connection = sqlite3.connect("contacts_book.db")
	cur = connection.cursor()

	record_id = delete_box.get()
	cur.execute ("SELECT * FROM contacts WHERE oid = " + record_id)
	records = cur.fetchall()

	# create global var
	global first_name_editor
	global last_name_editor
	global phone_number_editor

	first_name_editor = Entry (editor, width = 30)
	first_name_editor.grid (row =0, column = 1, padx = 20, pady = (10, 0))
	last_name_editor = Entry (editor, width = 30)
	last_name_editor.grid (row =1, column = 1)
	phone_number_editor = Entry (editor, width = 30)
	phone_number_editor.grid (row =2, column = 1)

	first_name_label = Label (editor, text = "First Name")
	first_name_label.grid (row = 0, column =  0, pady = (10, 0))
	last_name_label = Label (editor, text = "Last Name")
	last_name_label.grid (row = 1, column =  0)
	phone_number_label = Label (editor, text = "Phone Number")
	phone_number_label.grid (row = 2, column = 0)

	for record in records:
		first_name_editor.insert (0, record [0])
		last_name_editor.insert (0, record [1])
		phone_number_editor.insert (0, record [2])

	save_btn = Button (editor, text = "Save Changes", command = update)
	save_btn.grid (row = 3, column = 0, columnspan = 2, pady = 10, padx = 10, ipadx = 40)

# create text boxes
first_name = Entry (root, width = 30)
first_name.grid (row =0, column = 1, padx = 20, pady = (10, 0))
last_name = Entry (root, width = 30)
last_name.grid (row =1, column = 1)
phone_number = Entry (root, width = 30)
phone_number.grid (row =2, column = 1)

delete_box = Entry (root, width = 30)
delete_box.grid (row = 6, column = 1)

# create labels
first_name_label = Label (root, text = "First Name")
first_name_label.grid (row = 0, column =  0, pady = (10, 0))
last_name_label = Label (root, text = "Last Name")
last_name_label.grid (row = 1, column =  0)
phone_number_label = Label (root, text = "Phone Number")
phone_number_label.grid (row = 2, column = 0)

delete_box_label = Label (root, text = "Select ID")
delete_box_label.grid (row = 6, column = 0, pady = 10, padx = 10)

# create submit button
submit_btn = Button (root, text = "Add Contact", command = submit)
submit_btn.grid (row = 3, column = 0, columnspan = 2, pady = 10, padx = 10, ipadx = 30)

# create see_all button
see_all_btn = Button (root, text = "Show All Contacts", command = see_all)
see_all_btn.grid (row = 4, column = 0, columnspan = 2, pady = 10, padx = 10, ipadx = 20)

# create delete button 
delete_btn = Button (root, text = "Select Contact", command = delete)
delete_btn.grid (row = 7, column = 0, columnspan = 2, pady = 10, padx = 10, ipadx = 30)

# create edit button
edit_btn = Button (root, text = "Edit Contact", command = edit)
edit_btn.grid (row = 8, column = 0, columnspan = 2, pady = 10, padx = 10, ipadx = 40)

# commit changes to database
connection.commit()

# close connection
connection.close()

root.mainloop()