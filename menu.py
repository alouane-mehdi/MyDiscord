import tkinter as tk
from tkinter import messagebox
from main_menu import MainMenu
import mysql.connector

class LoginInterface:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Login")

        self.username_label = tk.Label(self.root, text="Username:")
        self.username_label.pack()
        self.username_entry = tk.Entry(self.root)
        self.username_entry.pack()

        self.password_label = tk.Label(self.root, text="Password:")
        self.password_label.pack()
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.pack()

        self.login_button = tk.Button(self.root, text="Login", command=self.login)
        self.login_button.pack()

        # Connexion à la base de données
        self.db_connection = mysql.connector.connect(
            host="ahmed-aouad.students-laplateforme.io",
            user="ahmed-aouad",
            password="ouarda2017",
            database="ahmed-aouad_mydiscord"
        )
        self.db_cursor = self.db_connection.cursor()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Requête pour vérifier les informations de connexion
        query = "SELECT id_utilisateur FROM Utilisateurs WHERE email = %s AND mot_de_passe = %s"
        self.db_cursor.execute(query, (username, password))
        user = self.db_cursor.fetchone()

        if user:
            messagebox.showinfo("Login Successful", "Welcome to the main menu!")
            self.root.destroy()
            MainMenu().show_main_menu()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    login_interface = LoginInterface()
    login_interface.run()
