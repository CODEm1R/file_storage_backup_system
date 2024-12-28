import tkinter as tk
from tkinter import messagebox
import sys
import os

# Proje kök dizinini belirle ve arama yoluna ekle
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from repository.user_repo import delete_user
from updateProfilePage import UpdateProfilePage
from logInPage import LoginPage
from global_variables import *

class ProfilePage(tk.Frame):
    def __init__(self, parent):      
        super().__init__(parent)  
        tk.Label(self, text=f"Profilim {activeUser.nickname}", font=("Arial", 20)).pack(pady=20)

        # Update
        tk.Button(self,text="Profil Guncelle", command=lambda: parent.show_page(UpdateProfilePage)).pack(pady=10)
        # Delete
        tk.Button(self,text="Profil Sil", command=self.ask_delete_confirmation).pack(pady=10)
    
    def show_teams(self):
        print("Takimlariniz : ")      

    def delete_profile(self):
        delete_user(activeUser.user_id)
        print(f"Silindi {activeUser.nickname}")   
        self.master.show_page(LoginPage)    

     # Silme onayı için pencereyi açma
    def ask_delete_confirmation(self):
        result = messagebox.askquestion("Profil Silme", "Profilinizi silmek istiyor musunuz?")
        
        if result == 'yes':  # Eğer 'Evet' butonuna basarsa
            self.delete_profile()
        else:  # Eğer 'Hayır' butonuna basarsa
            print("Silme işlemi iptal edildi.")
            # Silme penceresini kapatma veya başka bir işlem yapabilirsiniz (otomatik kapanır).   

