import tkinter as tk
from tkinter import messagebox
from logInPage import LoginPage
import sys
import os

# Proje kök dizinini belirle ve arama yoluna ekle
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)


# Ana uygulama sınıfı
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Giriş ve Kayıt")
        self.geometry("400x400")
        self.show_page(LoginPage)

    # Sayfaları değiştirme fonksiyonu
    def show_page(self, page_class):
        for widget in self.winfo_children():
            widget.destroy()
        page = page_class(self)
        page.pack(expand=True, fill="both")






# Uygulamayı çalıştırma
if __name__ == "__main__":
    app = App()
    app.mainloop()
