import tkinter as tk
from tkinter import messagebox

import sys
import os

# Proje kök dizinini belirle ve arama yoluna ekle
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from homePage import HomePage
from models.team import Team
from repository.team_member_repo import add_team_member
from repository.team_repo import create_team, get_team_id_by_team_name
from global_variables import *

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
