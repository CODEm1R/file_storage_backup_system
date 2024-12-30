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
from repository.file_share_repo import *


activeUser = None
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

        tk.Button(self, text="Login", command=lambda: self.login(self.name_entry.get(), self.password_entry.get())).pack(pady=10)
        tk.Button(self, text="Sign Up", command=lambda: parent.show_page(SignUpPage)).pack(pady=5)

    def login(self, nickname, password):

        if nickname and password:
            print(password)
            result = login_user_hash(nickname,password)
            print(result)

            global activeUser
            if result[3] == "Admin":
               activeUser  = AdminUser(result[0],result[1],result[2],result[3])
               self.master.show_page(AdminHomePage)

            elif result[3] == "Normal":
                activeUser  = NormalUser(result[0],result[1],result[2],result[3])
                self.master.show_page(HomePage)

        else:
            messagebox.showerror("Hata", "Kullanici adi ve şifre boş birakilamaz!")
            self.master.show_page(LoginPage)


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

class AdminHomePage(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.master.title("Admin Home Page")
        self.pack()

        # Sayfa bileşenlerini buraya ekleyebilirsiniz
        self.create_widgets()

    def create_widgets(self):
        # Burada admin home page için widget'lar ekleyebilirsiniz
        welcome_label = tk.Label(self, text="Hoş geldiniz, Admin!")
        welcome_label.pack(pady=20)

        # Kullanıcı listesini göstermek için Listbox
        self.user_listbox = tk.Listbox(self, width=50, height=10)
        self.user_listbox.pack(pady=10)
        # Kullanıcı listesini yükle
        update_users_list(users_listbox=self.user_listbox)

        delete_user_button = tk.Button(self, text="Kullanici sil",command=lambda: self.remove_user(self.user_listbox))
        delete_user_button.pack(pady=10)

        # Kullanıcı boyutunu düzenleme alanı (Entry ve Buton yan yana)
        size_frame = tk.Frame(self)
        size_frame.pack(pady=10)

        self.size_entry = tk.Entry(size_frame, width=20)
        self.size_entry.pack(side=tk.LEFT, padx=5)

        size_button = tk.Button(size_frame, text="Boyut Düzenle", command=lambda: self.update_user_limit(self.get_user_id(self.user_listbox),self.size_entry.get(),self.user_listbox))
        size_button.pack(side=tk.LEFT, padx=5)

        # Kullanıcı dsoyalarını düzenleme alanı (Entry ve Buton yan yana)
        usersfile_frame = tk.Frame(self)
        usersfile_frame.pack(pady=10)

        tk.Label(usersfile_frame, text="Dosyalari goruntulenecek user id:").pack(side=tk.LEFT, padx=5)
        self.userID_entry = tk.Entry(usersfile_frame, width=20)
        self.userID_entry.pack(side=tk.LEFT, padx=5)

        file_button = tk.Button(usersfile_frame, text="Dosyalari Gor", command=lambda: update_files_list(self.files_listbox,self.userID_entry.get()))
        file_button.pack(side=tk.LEFT, padx=5)

        # Kullanıcı listesini göstermek için Listbox
        self.files_listbox = tk.Listbox(self, width=50, height=10)
        self.files_listbox.pack(pady=10)

        file_open_button = tk.Button(self, text="Dosya Ac", command=lambda: os.startfile(self.files_listbox.get(self.files_listbox.curselection())[2]))
        file_open_button.pack(side=tk.LEFT, padx=5)

        # Kullanıcı dosyası silmek için
        file_delete_frame = tk.Frame(self)
        file_delete_frame.pack(side=tk.LEFT, padx=5)

        self.delete_entry = tk.Entry(file_delete_frame,width=20)
        self.delete_entry.pack(side=tk.LEFT, padx=5)

        file_delete_button = tk.Button(file_delete_frame, text="Dosya Sil", command=lambda: delete_file_by_id(self.delete_entry.get()))
        file_delete_button.pack(side=tk.LEFT, padx=5)



        logout_button = tk.Button(self, text="Çikiş Yap", command=self.logout)
        logout_button.pack(pady=10)    

    def update_user_limit(self,userID, new_limit, users_listbox):
        update_storage_limit(userID, new_limit)
        update_users_list(users_listbox)        

    def remove_user(self, user_listbox):
        user_id = self.get_user_id(user_listbox)
        delete_user(user_id)
        update_users_list(user_listbox)

    def get_user_id (self, user_listbox):
        selected = user_listbox.curselection()
        index = selected[0]
        user = user_listbox.get(index)
        user_id = user[0]
        print(user_id)
        #user_id = user_listbox.get(selected[0])
        return user_id

    def logout(self):
        print("Admin çıkış yaptı.")
        # Burada çıkış yapmak için gerekli işlemleri gerçekleştirebilirsiniz
        self.master.quit()

class HomePage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        tk.Label(self, text="Ana Sayfa", font=("Arial", 20)).pack(pady=20)
        tk.Label(self, text="Hoş geldiniz!", font=("Arial", 14)).pack(pady=10)

        # Yatay Takım butonları
        team_buttons_frame = tk.Frame(self)
        team_buttons_frame.pack(pady=10)

        tk.Button(team_buttons_frame, text="Takimlarim", command=lambda: parent.show_page(TeamsPage)).pack(side=tk.LEFT, padx=10)

        # "Dosya Sil" butonu
        tk.Button(team_buttons_frame, text="Takim yap", command=lambda: parent.show_page(CreateTeamPage)).pack(side=tk.LEFT, padx=10)

        # "Profilim" butonu
        tk.Button(self, text="Profilim", command=lambda: parent.show_page(ProfilePage)).pack(pady=10)

        # "Dosya Yükle" butonu
        files_listbox = tk.Listbox(parent, height=10, width=100, selectmode="single")
        files_listbox.pack(pady=10)
        update_files_list(files_listbox,activeUser.user_id) 

        teams_listbox = tk.Listbox(parent, height=10, width=100, selectmode="single")
        teams_listbox.pack(pady=10)
        update_teams_list(teams_listbox,activeUser.user_id)

         # Yatay çerçeve oluştur
        file_buttons_frame = tk.Frame(self)
        file_buttons_frame.pack(pady=10)

        # "Dosya Yükle" butonu
        tk.Button(file_buttons_frame, text="Dosya Yukle", command=lambda: upload_file(files_listbox, activeUser.user_id)).pack(side=tk.LEFT, padx=10)

        # "Dosya Sil" butonu
        tk.Button(file_buttons_frame, text="Dosya Sil", command=lambda: delete_file(files_listbox, activeUser.user_id)).pack(side=tk.LEFT, padx=10)

         # Dosya paylaşma girişleri
        share_inputs_frame = tk.Frame(self)
        share_inputs_frame.pack(pady=10)

        # Dosya ID girişi
        tk.Label(share_inputs_frame, text="Dosya ID:").pack(side=tk.LEFT, padx=5)
        file_id_entry = tk.Entry(share_inputs_frame, width=15)
        file_id_entry.pack(side=tk.LEFT, padx=5)

        # Takım ID girişi
        tk.Label(share_inputs_frame, text="Takim ID:").pack(side=tk.LEFT, padx=5)
        team_id_entry = tk.Entry(share_inputs_frame, width=15)
        team_id_entry.pack(side=tk.LEFT, padx=5)

        # "Dosya Paylaş" butonu
        tk.Button(
            share_inputs_frame,
            text="Dosya Paylaş",
            command=lambda: share_file_with_team(
                file_id=file_id_entry.get(),
                team_id=team_id_entry.get()
            )
        ).pack(pady=10)


    def share_file(self, files_listbox):
        selected_file_item = files_listbox.curselection()
        if not selected_file_item:
            print("Lütfen bir dosya seçin!")
            return None

        index = selected_file_item[0]
        file = files_listbox.get(index)
        print(f"Listbox'tan alınan dosya: {file}")  # Değeri doğrulama

        if isinstance(file, tuple) and len(file) > 0:
            file_id = file[0]
            print(f"Seçilen dosya ID: {file_id}")
            return file_id
        else:
            print("Geçersiz dosya formati!")
            return None

    def share_team(self, teams_listbox):
        selected_team_item = teams_listbox.curselection()
        if not selected_team_item:
            print("Lütfen bir takim seçin!")
            return None

        index = selected_team_item[0]
        team = teams_listbox.get(index)
        print(f"Listbox'tan alinan takim: {team}")  # Değeri doğrulama

        if isinstance(team, tuple) and len(team) > 0:
            team_id = team[0]
            print(f"Seçilen takim ID: {team_id}")
            return team_id
        else:
            print("Geçersiz takım formatı!")
            return None    


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

    def create_widgets(self, parent):
        # Üst Kısım: Başlık
        header = tk.Frame(parent)
        header.pack(fill="x", pady=10)
        tk.Label(header, text=f"{activeTeam.team_name}", font=("Arial", 20)).pack(side="left", padx=20)
        # Sağ Üst: Kullanıcı Ekle Butonu
        tk.Button(header, text="Kullanıcı Ekle", command=self.add_user).pack(side="right", padx=20)

        # "Dosya Yükle" butonu ve Dosya Listbox
        self.team_files_listbox = tk.Listbox(self, height=10, width=100, selectmode="single")
        self.team_files_listbox.pack(pady=10)
        
        # Başlangıçta dosyaları listele
        self.update_file_listbox()

    def add_user(self):
        print(f"Kullanıcı ekleme işlemi başlatıldı. {activeTeam.team_id}")
        # Yeni bir pencere aç
        popup = tk.Toplevel(self)
        popup.title("Kullanıcı Seç")
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
            tk.Label(self.teams_frame, text="Herhangi bir takımınız yok.", font=("Arial", 12)).pack(pady=5)         

    def select_user(self, user_id, popup):
        add_team_member(user_id, activeTeam.team_id)
        popup.destroy()  # Pencereyi kapat
        self.update_file_listbox()  # Yeni kullanıcı eklendikten sonra dosyaları güncelle

    def update_file_listbox(self):
        # Takıma ait dosyaları veritabanından al
        file_ids = get_file_ids_for_team(activeTeam.team_id)
        if not file_ids:
            self.team_files_listbox.delete(0, tk.END)
            self.team_files_listbox.insert(tk.END, "Bu takıma ait dosya bulunmamaktadır.")
            return
        
        file_details = get_file_details(file_ids)
        
        # Listbox'u temizle
        self.team_files_listbox.delete(0, tk.END)

        # Dosya bilgilerini Listbox'a ekle
        for file in file_details:
            file_info = f"{file[0]} - {file[2]} MB - {file[3]} - Owner: {file[4]}"  # file_name, file_size, file_type, owner_id
            self.team_files_listbox.insert(tk.END, file_info)





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
