import tkinter as tk
from tkinter import messagebox

# Uygulama penceresi
app = tk.Tk()
app.title("Giriş ve Kayıt")
app.geometry("400x400")

# Ana sayfayı oluşturma
def create_main_page():
    for widget in app.winfo_children():
        widget.destroy()

    tk.Label(app, text="Ana Sayfa", font=("Arial", 20)).pack(pady=20)
    tk.Label(app, text="Hoş geldiniz!", font=("Arial", 14)).pack(pady=10)

# Giriş sayfasını oluşturma
def create_login_page():
    for widget in app.winfo_children():
        widget.destroy()

    tk.Label(app, text="Giriş Yap", font=("Arial", 20)).pack(pady=10)

    tk.Label(app, text="Kullanıcı Adı:").pack(pady=5)
    name_entry = tk.Entry(app)
    name_entry.pack(pady=5)

    tk.Label(app, text="Şifre:").pack(pady=5)
    password_entry = tk.Entry(app, show="*")
    password_entry.pack(pady=5)

    def login():
        name = name_entry.get()
        password = password_entry.get()
        if name and password:
            create_main_page()
        else:
            messagebox.showerror("Hata", "Kullanıcı adı ve şifre boş bırakılamaz!")

    tk.Button(app, text="Login", command=login).pack(pady=10)
    tk.Button(app, text="Sign Up", command=create_signup_page).pack(pady=5)

# Kayıt sayfasını oluşturma
def create_signup_page():
    for widget in app.winfo_children():
        widget.destroy()

    tk.Label(app, text="Kayıt Ol", font=("Arial", 20)).pack(pady=10)

    tk.Label(app, text="Kullanıcı Adı (Nickname):").pack(pady=5)
    nickname_entry = tk.Entry(app)
    nickname_entry.pack(pady=5)

    tk.Label(app, text="Şifre:").pack(pady=5)
    password_entry = tk.Entry(app, show="*")
    password_entry.pack(pady=5)

    tk.Label(app, text="Şifre Tekrar:").pack(pady=5)
    confirm_password_entry = tk.Entry(app, show="*")
    confirm_password_entry.pack(pady=5)

    def signup():
        nickname = nickname_entry.get()
        password = password_entry.get()
        confirm_password = confirm_password_entry.get()

        if not nickname or not password or not confirm_password:
            messagebox.showerror("Hata", "Tüm alanları doldurun!")
        elif password == confirm_password:
            messagebox.showinfo("Bilgi", f"Kayıt başarılı.\nKullanıcı Adı: {nickname}")
            create_main_page()
        else:
            messagebox.showerror("Hata", "Şifreler uyuşmuyor!")

    tk.Button(app, text="Sign Up", command=signup).pack(pady=10)

# İlk olarak giriş sayfasını oluştur
create_login_page()

# Uygulamayı çalıştır
app.mainloop()
