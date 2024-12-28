import tkinter as tk
from tkinter import messagebox

# arayuz/sayfa.py
import sys
import os

# Proje kök dizinini belirle ve arama yoluna ekle
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from models.user import *
from models.team import *

from repository.user_repo import *
from repository.team_repo import *
from repository.team_member_repo import *
from repository.file_repo import *


activeUser = NormalUser(user_id=1,nickname="default Name",password="default Password",role="Normal")
activeTeam = Team(team_id=1,team_name="defaultName")

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


class HomePage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        tk.Label(self, text="Ana Sayfa", font=("Arial", 20)).pack(pady=20)
        tk.Label(self, text="Hoş geldiniz!", font=("Arial", 14)).pack(pady=10)

        # "Takımlar" butonu
        tk.Button(self, text="Takimlarim", command=lambda: parent.show_page(TeamsPage)).pack(pady=10)

        # Takım Oluştur Butonu 
        tk.Button(self, text="Takim yap", command=lambda: parent.show_page(CreateTeamPage)).pack(pady=10)

        # "Profilim" butonu
        tk.Button(self, text="Profilim", command=lambda: parent.show_page(ProfilePage)).pack(pady=10)

        # "Dosya Yükle" butonu
        files_listbox = tk.Listbox(parent, height=10, width=100)
        files_listbox.pack(pady=10)
        update_files_list(files_listbox,activeUser.user_id) 
        tk.Button(self, text="Dosya Yukle", command=lambda: upload_file(files_listbox , activeUser.user_id)).pack(pady=10)


# Takımlar Sayfası
class TeamsPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Takimlar", font=("Arial", 20)).pack(pady=20)
        
        # Takımlar alanı (Boş alan)
        self.teams_frame = tk.Frame(self)
        self.teams_frame.pack(pady=20)

        # Veritabanından kullanıcıya ait takımları al
        teams = get_user_teams_by_user_id(activeUser.user_id)

        if teams:
            for team in teams:
                # Takım isimlerini buton olarak göstermek
                tk.Button(
                    self.teams_frame, 
                    text=team[1], 
                    command=lambda t=team: self.open_team_page(t),  # 't=team' ile her bir takım değerini lambda'ya geçiriyoruz
                    font=("Arial", 12)
                ).pack(pady=5)
                print(team)
        else:
            tk.Label(self.teams_frame, text="Herhangi bir takiminiz yok.", font=("Arial", 12)).pack(pady=5)

        # Geri Dön Butonu
        tk.Button(self, text="Geri Dön", command=lambda: self.master.show_page(HomePage)).pack(pady=20)

    def open_team_page(self,team):
        # Seçilen takım 'activeTeam' değişkenine atanır
        team_object = Team(team_id=1,team_name=team[1])
        global activeTeam
        activeTeam = team_object
        print(f"Aktif takım adı : {team_object.team_name}")
        activeTeam.team_id = get_team_id_by_team_name(activeTeam.team_name)
        print(f"Aktif takım: {activeTeam.team_id}")
        # Burada takım detay sayfasına yönlendirme ya da başka işlemler yapılabilir.
        self.master.show_page(MyTeamPage)


class MyTeamPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.create_widgets(self.parent)

    def create_widgets(self,parent):
        # Üst Kısım: Başlık
        header = tk.Frame(parent)
        header.pack(fill="x", pady=10)
        tk.Label(header, text=f"{activeTeam.team_name}", font=("Arial", 20)).pack(side="left", padx=20)
        # Sağ Üst: Kullanıcı Ekle Butonu
        tk.Button(header, text="Kullanici Ekle", command=self.add_user).pack(side="right", padx=20)

        # Orta Kısım: Yüklenecek Dosyaların Gösterileceği Alan
        middle_frame = tk.Frame(self, width=300, height=300, bg="lightgray")
        middle_frame.pack(pady=20, fill="both", expand=True)
        middle_frame.pack_propagate(False)  # Alanın sabit boyutta kalmasını sağla
        # "Dosya Yükle" butonu
        files_listbox = tk.Listbox(self.parent, height=10, width=100)
        files_listbox.pack(pady=10)
        update_files_list(files_listbox,activeUser.user_id)

        # Alt Kısım: Dosya Ekle Butonu
        tk.Button(self, text="Dosya Ekle", command=lambda: upload_file(files_listbox , activeUser.user_id), font=("Arial", 12)).pack(pady=20)

    def add_user(self):
        print(f"Kullanıcı ekleme işlemi başlatıldı. {activeTeam.team_id}")
        # Yeni bir pencere aç
        popup = tk.Toplevel(self)
        popup.title("Kullanici Seç")
        popup.geometry("300x400")

        all_users = get_all_users()
        # Kullanıcıları listele (activeUser dışındaki kullanıcılar)
        if all_users:
            for user in all_users:
                if user[0] != activeUser.user_id:
                    tk.Button(
                        popup,
                        text=user[1],
                        command=lambda user_id=user[0]: self.select_user(user_id, popup)
                    ).pack(pady=5)
        else:
            tk.Label(self.teams_frame, text="Herhangi bir takiminiz yok.", font=("Arial", 12)).pack(pady=5)         

    def select_user(self, user_id, popup):
        add_team_member(user_id, activeTeam.team_id)
        
        popup.destroy()  # Pencereyi kapat




class CreateTeamPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        tk.Label(self, text="Takim Yarat", font=("Arial", 20)).pack(pady=20)  

        tk.Label(self, text="Takim Adi").pack(pady=5)
        self.teamname_entry = tk.Entry(self)
        self.teamname_entry.pack(pady=5)      

        # Takım Yarat 
        tk.Button(self, text="Olustur", command=self.create_new_team).pack(pady=10)
    
    def create_new_team(self):    
        team = Team(team_id=1,team_name=self.teamname_entry.get())

        if not team.team_name :
            messagebox.showerror("Hata", "Tüm alanlari doldurun!")
        else:            
            create_team(team_name=team.team_name)
            messagebox.showinfo("Bilgi", f"Kayit başarili.\Takim Adi: {team.team_name}")
            team.team_id = get_team_id_by_team_name(team_name=team.team_name)
            print(f"olusturulan takim idsi: {team.team_id}")
            add_team_member(user_id=activeUser.user_id, team_id=team.team_id)
            print(f"Takim olustu {team.team_name}")
            self.master.show_page(HomePage)

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

        


        



# Uygulamayı çalıştırma
if __name__ == "__main__":
    app = App()
    app.mainloop()
