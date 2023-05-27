import sqlite3
from tkinter import Toplevel, Label, Entry, Button

from index import  tree


def show_payment_window():
    payment_window = Toplevel()
    payment_window.title("Add Payment")
    payment_window.geometry("600x400")

    lbl_date_encaissement = Label(payment_window, text="date_encaissement:")
    lbl_date_encaissement.pack()

    entry_date_encaissement = Entry(payment_window)
    entry_date_encaissement.pack()

    lbl_encaissement = Label(payment_window, text="encaissement:")
    lbl_encaissement.pack()

    entry_encaissement = Entry(payment_window)
    entry_encaissement.pack()


    btn_add_payment = Button(payment_window, text="Add Payment", command=lambda: add_payment(entry_date_encaissement, entry_encaissement))
    btn_add_payment.pack()

    def add_payment(entry_date_encaissement, entry_encaissement):
        idSelect = tree.item(tree.selection())['values'][0]
        date_encaissement = entry_date_encaissement.get()
        encaissement = entry_encaissement.get()



        conn = sqlite3.connect("database.db")
        cur = conn.cursor()
        cur.execute("INSERT INTO encaissements (id_customer, date_encaissement, encaissement) VALUES (?, ?, ?)",
                    (idSelect, date_encaissement, encaissement))
        conn.commit()
        conn.close()

        # Afficher un message ou effectuer d'autres actions après l'ajout de l'encaissement

        # Effacer les champs d'entrée
        entry_date_encaissement.delete(0, 'end')
        entry_encaissement.delete(0, 'end')

        # Fermer la fenêtre de paiement
        payment_window.destroy()

        payment_window.mainloop()
