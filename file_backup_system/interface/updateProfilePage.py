import tkinter as tk
from tkinter import messagebox

from profilePage import ProfilePage
from logInPage import LoginPage

import sys
import os

# Proje kök dizinini belirle ve arama yoluna ekle
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from repository.user_repo import update_user
from global_variables import *

class UpdateProfilePage(tk.Frame):
    def __init__(self, parent):      
        super().__init__(parent)  
        tk.Label(self, text=f"Guncelle  {activeUser.nickname}", font=("Arial", 20)).pack(pady=20)

        tk.Label(self, text="Yeni Kullanici Adi:").pack(pady=5)
        self.name_entry = tk.Entry(self)
        self.name_entry.pack(pady=5)

        tk.Label(self, text="Yeni Şifre:").pack(pady=5)
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack(pady=5)

        # Update
        tk.Button(self,text="Profil Guncelle", command=self.update_profile).pack(pady=10)
        # Back
        tk.Button(self,text="Geri Don", command=lambda: parent.show_page(ProfilePage)).pack(pady=10)

    def update_profile(self):
        update_user(user_id=activeUser.user_id, user_name=self.name_entry.get(), user_password=self.password_entry.get(), role="Normal")
        
        print("Guncelleniyor ")
        self.master.show_page(LoginPage)

