import tkinter as tk
from tkinter import messagebox

from homePage import HomePage
from myTeamPage import MyTeamPage

import sys
import os

# Proje kök dizinini belirle ve arama yoluna ekle
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from models.team import Team
from repository.team_member_repo import get_user_teams_by_user_id
from repository.team_repo import get_team_id_by_team_name
from global_variables import *

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
