"""
import sqlite3
from tkinter import Toplevel, Button, Entry, Label, messagebox
from datetime import date

def show_payment_window(selected_customer):
    def add_payment():
        if selected_customer is None:
            messagebox.showwarning("Attention", "Veuillez sélectionner un client.")

        else:
            # Connexion à la base de données
            conn = sqlite3.connect('database.db')
            cur = conn.cursor()

            date_encaissement = entry_date_encaissement.get()
            encaissement = entry_encaissement.get()

            # Logique pour ajouter l'encaissement au client sélectionné
            # Insérez les valeurs d'encaissement dans la base de données
            insert_query = "INSERT INTO encaissements (id_customer, date_encaissement, encaissement) VALUES (?, ?, ?)"
            cur.execute(insert_query, (selected_customer["id"], date_encaissement, encaissement))

            # Validez les modifications et fermez la connexion
            conn.commit()
            conn.close()

        payment_window.destroy()

    payment_window = Toplevel()
    payment_window.title("Add Payment")
    payment_window.geometry("600x400")

    lbl_date_encaissement = Label(payment_window, text="date_encaissement:")
    lbl_date_encaissement.pack()

    entry_date_encaissement = Entry(payment_window)
    entry_date_encaissement.pack()
    entry_date_encaissement.insert(0, date.today().strftime("%Y-%m-%d"))

    lbl_encaissement = Label(payment_window, text="encaissement:")
    lbl_encaissement.pack()

    entry_encaissement = Entry(payment_window)
    entry_encaissement.pack()

    btn_add_payment = Button(payment_window, text="Add Payment", command=add_payment)
    btn_add_payment.pack()

    # Affichage de la fenêtre de paiement
    payment_window.mainloop()


# Appel à la fenêtre de paiement
#show_payment_window(selected_customer)
"""