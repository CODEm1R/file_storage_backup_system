import tkinter as tk
from tkinter import messagebox
from signUpPage import *
import sys
import os

# Proje kök dizinini belirle ve arama yoluna ekle
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

# Giriş sayfası sınıfı
class LoginPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        tk.Label(self, text="Giriş Yap", font=("Arial", 20)).pack(pady=10)

        tk.Label(self, text="Kullanici Adi:").pack(pady=5)
        self.name_entry = tk.Entry(self)
        self.name_entry.pack(pady=5)

        tk.Label(self, text="Şifre:").pack(pady=5)
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack(pady=5)

        tk.Button(self, text="Login", command=self.login).pack(pady=10)
        tk.Button(self, text="Sign Up", command=lambda: parent.show_page(SignUpPage)).pack(pady=5)

    def login(self):

        user = NormalUser(user_id=1, nickname=self.name_entry.get(), password=self.password_entry.get(), role="Normal")

        if user.nickname and user.password:
            if login_user(user.nickname,user.password):
                global activeUser 
                activeUser = user
                activeUser.user_id = get_user_id_by_name(activeUser.nickname)
                print(activeUser.user_id)
                print(f"giris yapan {activeUser.nickname}")
                self.master.show_page(HomePage)
            else:
                messagebox.showerror("Hata","Kulalnici Bulunamadi")
                self.master.show_page(LoginPage)        
            
        else:
            messagebox.showerror("Hata", "Kullanici adi ve şifre boş birakilamaz!")

