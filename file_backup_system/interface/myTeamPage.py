
import tkinter as tk
from tkinter import messagebox

import sys
import os

# Proje kök dizinini belirle ve arama yoluna ekle
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from repository.team_member_repo import add_team_member
from global_variables import *

class MyTeamPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.create_widgets()

    def create_widgets(self):
        # Üst Kısım: Başlık
        header = tk.Frame(self)
        header.pack(fill="x", pady=10)
        tk.Label(header, text=f"{activeTeam.team_name}", font=("Arial", 20)).pack(side="left", padx=20)
        print(f"")
        # Sağ Üst: Kullanıcı Ekle Butonu
        tk.Button(header, text="Kullanici Ekle", command=self.add_user).pack(side="right", padx=20)

        # Orta Kısım: Yüklenecek Dosyaların Gösterileceği Alan
        middle_frame = tk.Frame(self, width=300, height=300, bg="lightgray")
        middle_frame.pack(pady=20, fill="both", expand=True)
        middle_frame.pack_propagate(False)  # Alanın sabit boyutta kalmasını sağla
        tk.Label(middle_frame, text="Dosyalar burada görünecek", font=("Arial", 12), bg="lightgray").pack()

        # Alt Kısım: Dosya Ekle Butonu
        tk.Button(self, text="Dosya Ekle", state="disabled", font=("Arial", 12)).pack(pady=20)

    def add_user(self):
        print(f"Kullanici ekleme işlemi baslatildi. {activeTeam.team_id}")     
        add_team_member(user_id=7, team_id=activeTeam.team_id)   

