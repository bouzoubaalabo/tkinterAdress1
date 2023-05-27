

from tkinter import ttk, filedialog
from tkinter import *
from tkinter import Text
from PIL import Image, ImageTk
import sqlite3

from tkinter import Tk, Button
from tkinter import Toplevel, Button, Entry, Label, messagebox
from datetime import date

def open_payment_window():
#   payment_window.show_payment_window(selected_customer)
    payment_window = PaymentWindow(selected_customer)
    payment_window.mainloop()

Profile = {1 : ""}


selected_customer = None



def add_customer():
    name = entryName.get()
    phone = entryPhone.get()
    more = entryMore.get()

    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
#    cur.execute("INSERT INTO customers ('name', 'phone', 'more')values (?,?,?)", (name, phone, more))
    cur.execute("INSERT INTO customers (\"name\", \"phone\", \"more\") VALUES (?, ?, ?)", (name, phone, more))
    conn.commit()
    conn.close()
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    select = cur.execute("SELECT*FROM customers order by id desc")
    select = list(select)
    tree.insert('', END, values= select[0])
    conn.close()
    # vider les champs d'entrée
    entryName.delete(0, 'end')
    entryPhone.delete(0, 'end')
    entryMore.delete(0, 'end')
    entryPhoto.delete(0, 'end')
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    select = cur.execute("SELECT*FROM customers order by id desc")
    select = list(select)
    id = select[0][0]
    filename = entryPhoto.get()
    im = Image.open(filename)
    rgb_im = im.convert('RGB')
    rgb_im.save(("images/profile_" + str(id) + "." + "jpg"))
    conn.close()

def delete_customer():
    idSelect = tree.item(tree.selection())['values'][0]
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    delete = cur.execute("delete from customers where id = {}".format(idSelect))
    conn.commit()
    tree.delete(tree.selection())

def sortByName():
    #clear treeview
    for x in tree.get_children():
        tree.delete(x)
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    select = cur.execute("select*from customers order by name asc ")
    conn.commit()

    for row in select:
        tree.insert('', END, values=row)
    conn.close()

def SearchByName(event):
    for x in tree.get_children():
        tree.delete(x)
    name = entrySearchByName.get()
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    select = cur.execute("SELECT*FROM customers where name =(?)", (name,))
    conn.commit()
    for row in select:
        tree.insert('', END, values=row)
    conn.close()

def SearchByPhone(event):
    for x in tree.get_children():
        tree.delete(x)
    phone = entrySearchByPhone.get()
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    select = cur.execute("SELECT*FROM customers where phone =(?)", (phone,))
    conn.commit()
    for row in select:
        tree.insert('', END, values=row)
    conn.close()

def BrowsePhoto():
    entryPhoto.delete(0, END)
    filename = filedialog.askopenfilename(initialdir = "/", title = "Select File")
    entryPhoto.insert(END, filename)



class PaymentWindow(Toplevel):
    def __init__(self, selected_customer):
        super().__init__()
        self.title("Add Payment")
        self.geometry("600x400")

        lbl_date_encaissement = Label(self, text="Date d'encaissement:")
        lbl_date_encaissement.grid(row=0, column=0)

        self.entry_date_encaissement = Entry(self)
        self.entry_date_encaissement.grid(row=0, column=1)
        self.entry_date_encaissement.insert(0, date.today().strftime("%Y-%m-%d"))

        lbl_encaissement = Label(self, text="Montant de l'encaissement:")
        lbl_encaissement.grid(row=1, column=0)

        self.entry_encaissement = Entry(self)
        self.entry_encaissement.grid(row=1, column=1)

        btn_add_payment = Button(self, text='Ajouter l\'encaissement', command=self.add_payment)
        btn_add_payment.grid(row=2, column=0, columnspan=2)


        self.selected_customer = selected_customer

    def add_payment(self):
        if self.selected_customer is None:
            messagebox.showwarning("Attention", "Veuillez sélectionner un client.")
        else:
            date_encaissement = self.entry_date_encaissement.get()
            encaissement = self.entry_encaissement.get()
            # Connexion à la base de données
            conn = sqlite3.connect("database.db")
            cursor = conn.cursor()

            # Exemple de requête d'insertion des données dans une table "encaissements"
            query = "INSERT INTO encaissements (id_customer, date_encaissement, encaissement) VALUES (?, ?, ?)"
            values = (self.selected_customer['id'], date_encaissement, encaissement)
            cursor.execute(query, values)

            # Exemple de validation de la transaction et fermeture de la connexion
            conn.commit()
            conn.close()

        self.destroy()



def get_customer_by_id(customer_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Exécutez une requête SELECT pour récupérer les informations du client par ID
    cursor.execute("SELECT id, name, phone, more FROM customers WHERE id = ?", (customer_id,))
    customer_data = cursor.fetchone()  # Récupérez la première ligne de résultat

    conn.close()

    if customer_data:
        customer = {
            'id': customer_data[0],
            'name': customer_data[1],
            'phone': customer_data[2],
            'more': customer_data[3],
        }
        return customer

    return None  # Aucun client trouvé avec l'ID fourni


def treeActionSelect(event):
    global selected_customer
    idSelect = tree.item(tree.selection())['values'][0]
    # Autres actions à effectuer avec l'ID du client sélectionné, par exemple :
    selected_customer = get_customer_by_id(idSelect)

    # Charger l'image
    imgProfile = "images/profile_" + str(idSelect) + ".jpg"
    load = Image.open(imgProfile)
    load.thumbnail((100, 100))
    photo = ImageTk.PhotoImage(load)

    # Détruire le label d'image existant (s'il y en a un)
    if hasattr(root, "lblImage"):
        root.lblImage.destroy()

    # Créer un nouveau label d'image
    lblImage = Label(root, bg="blue", image=photo)
    lblImage.place(x=10, y=350)
    root.lblImage = lblImage  # Sauvegarder la référence du label d'image pour une utilisation future

#    load image
    lblImage.destroy()
    idSelect = tree.item(tree.selection())['values'][0]
    nameSelect = tree.item(tree.selection())['values'][1]
    phoneSelect = tree.item(tree.selection())['values'][2]
    moreInfoSelect = tree.item(tree.selection())['values'][3]

    imgProfile = "images/profile_" + str(idSelect) + "." + "jpg"
    print(imgProfile)
    load = Image.open(imgProfile)
    load.thumbnail((100, 100))
    photo = ImageTk.PhotoImage(load)
    Profile[1] = photo
    lblImage = Label(root, bg="blue", image=photo)
    lblImage.place(x=10, y=350)
    lid = Label(root, text="ID: " + str(idSelect))
    lid.place(x=110, y=350)
    lname = Label(root, text="Name: " + nameSelect)
    lname.place(x=110, y=380)
    lphone = Label(root, text="Phone: " + str(phoneSelect))
    lphone.place(x=110, y=410)
    Tmore = Text(root)
    Tmore.place(x=260, y=360, width=280, height=100)
    Tmore.insert(END, "More info: " + moreInfoSelect)

    # Mettre à jour la variable selected_customer avec les informations du client sélectionné
    selected_customer = {
        "id": idSelect,
        "name": nameSelect,
        "phone": phoneSelect,
        "more_info": moreInfoSelect
    }








root = Tk()
root.title("Address Book")
root.geometry("1200x600")
root['bg'] = 'red'
root.configure(bg="#eaeaea")
root.resizable(height=False, width=False)

# add Title
lblTitle = Label(root, text="Adress book", font=("Arial", 21), bg="darkblue", fg="white")
lblTitle.place(x=0, y=0, width=250, height=41)

# search area

def populate_combobox():
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    select = cur.execute("SELECT name FROM customers ORDER BY name ASC")
    names = [row[0] for row in select]
    entrySearchByName['values'] = names
    conn.close()


lbSearchByName = Label(root, text="Search by name :", bg="darkblue", fg="white")
lbSearchByName.place(x=250, y=0, width=120)
#entrySearchByName = Entry(root)
entrySearchByName = ttk.Combobox(root, values=[], state="readonly")
#essai GPT
# Appeler la fonction pour peupler la liste déroulante au démarrage
populate_combobox()

# Associer la fonction SearchByName à l'événement de sélection de la liste déroulante
entrySearchByName.bind("<<ComboboxSelected>>", SearchByName)
#fIN

# entrySearchByName.bind("<Return>" , SearchByName)
entrySearchByName.place(x=380, y=0, width=160)



lbSearchByPhone = Label(root, text="Search by phone :", bg="darkblue", fg="white")
lbSearchByPhone.place(x=250, y=20, width=120)
entrySearchByPhone = Entry(root)
entrySearchByPhone.bind("<Return>" , SearchByPhone)
entrySearchByPhone.place(x=380, y=20, width=160)

# LABEL name & surname
lblName = Label(root, text="name & surname :", bg="black", fg="yellow")
lblName.place(x=5, y=50, width=125)
entryName = Entry(root)
entryName.place(x=140, y=50, width=400)

# Label & Entry Phone
lblPhone = Label(root, text="Phone Number:", bg="black", fg="yellow")
lblPhone.place(x=5, y=80, width=125)
entryPhone = Entry(root)
entryPhone.place(x=140, y=80, width=400)

# Label & Entry Photo
lblPhoto = Label(root, text="Photo:", bg="black", fg="yellow")
lblPhoto.place(x=5, y=110, width=125)
bPhoto = Button(root, text="Browse", bg="darkblue", fg="yellow", command= BrowsePhoto)
bPhoto.place(x=480, y=110, height=25)
entryPhoto = Entry(root)
entryPhoto.place(x=140, y=110, width=320)

# More Info
lblMore = Label(root, text="More Info:", bg="black", fg="yellow")
lblMore.place(x=5, y=140, width=125)
entryMore = Entry(root)
entryMore.place(x=140, y=140, width=400)

# COMMand button
bAdd = Button(root, text="add Customer", bg="darkblue", fg="yellow", command = add_customer)
bAdd.place(x=5, y=170, width=255)

bDelete = Button(root, text="Delete Selected", bg="darkblue", fg="yellow", command= delete_customer)
bDelete.place(x=5, y=205, width=255)

bEdit = Button(root, text="Edit Selected", bg="darkblue", fg="yellow")
bEdit.place(x=5, y=240, width=255)

bSort = Button(root, text="Sort by name", bg="darkblue", fg="yellow", command = sortByName)
bSort.place(x=5, y=275, width=255)

bExit = Button(root, text="Exit App", bg="darkblue", fg="yellow", command=quit)
bExit.place(x=5, y=310, width=255)

#load Image
"""
load = Image.open("Images/profile.png")
load.thumbnail((130, 130))
photo = ImageTk.PhotoImage(load)
label_image = Label(root, image = photo)
label_image.place(x = 10, y =350)
"""
#add treeview
tree = ttk.Treeview(root, columns = (1, 2, 3), height= 5, show = "headings")
tree.place(x= 265, y= 170, width=280, height=175)
tree.bind("<<TreeviewSelect>>", treeActionSelect)

#add heAdings
tree.heading(1, text = "ID")
tree.heading(2, text = "Name")
tree.heading(3, text = "Phone")

#define column width
tree.column(1, width=50)
tree.column(2, width=100)
#Display data in treeview object
conn = sqlite3.connect('database.db')
cur = conn.cursor()
select = cur.execute("select*from customers")
for row in select:
    tree.insert('', END, value=row)
conn.close()

#bouton ajouter paiement
bAddPayment = Button(root, text="Ajouter Paiement", bg="darkblue", fg="yellow", command = open_payment_window)
bAddPayment.place(x=570, y=0, width=255)

#add treeviewEncaissement
treeEnc = ttk.Treeview(root, columns = (1, 2, 3), height= 5, show = "headings")
treeEnc.place(x= 570, y= 170, width=400, height=175)
#tree.bind("<<TreeviewSelect>>", treeActionSelect)

#add heAdings
treeEnc.heading(1, text = "customer")
treeEnc.heading(2, text = "date")
treeEnc.heading(3, text = "Encaissement")

#define column width
treeEnc.column(1, width=50)
treeEnc.column(2, width=50)
treeEnc.column(3, width=100)
"""
# Récupérer l'ID du client sélectionné
selected_customer_id = selected_customer['id']



#Display data in treeview object
conn = sqlite3.connect('database.db')
cur = conn.cursor()
#select = cur.execute("select*from encaissements")
select = cur.execute("SELECT * FROM encaissements WHERE id_customer = ?", (selected_customer_id,))
for row in select:
    treeEnc.insert('', END, values=(row[1], row[2], row[3]))

conn.close()
"""

root.mainloop()
