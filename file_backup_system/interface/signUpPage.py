import tkinter as tk
from tkinter import messagebox
# arayuz/sayfa.py
import sys
import os

# Proje kök dizinini belirle ve arama yoluna ekle
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)
from logInPage import LoginPage
from homePage import *

from models.user import *
from repository.user_repo import *


# Kayıt sayfası sınıfı
class SignUpPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        tk.Label(self, text="Kayıt Ol", font=("Arial", 20)).pack(pady=10)

        tk.Label(self, text="Kullanıcı Adı (Nickname):").pack(pady=5)
        self.nickname_entry = tk.Entry(self)
        self.nickname_entry.pack(pady=5)

        tk.Label(self, text="Şifre:").pack(pady=5)
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack(pady=5)

        tk.Label(self, text="Şifre Tekrar:").pack(pady=5)
        self.confirm_password_entry = tk.Entry(self, show="*")
        self.confirm_password_entry.pack(pady=5)

        tk.Button(self, text="Sign Up", command=self.signup).pack(pady=10)
        tk.Button(self, text="Back to Login", command=lambda: parent.show_page(LoginPage)).pack(pady=5)

    def signup(self):
        user = NormalUser(user_id=1,nickname=self.nickname_entry.get(), password=self.password_entry.get(),role="Normal")
        print(user.nickname)
        confirm_password = self.confirm_password_entry.get()

        if not user.nickname or not user.password or not confirm_password:
            messagebox.showerror("Hata", "Tüm alanları doldurun!")

        elif user.password == confirm_password:

            create_user(user.nickname,user.password,"Normal")
            messagebox.showinfo("Bilgi", f"Kayit başarili.\nKullanici Adi: {user.nickname}")
            self.master.show_page(LoginPage)

        else:
            messagebox.showerror("Hata", "Şifreler uyuşmuyor!")

