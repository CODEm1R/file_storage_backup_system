import tkinter as tk
from tkinter import messagebox
import sys
import os

# Proje kök dizinini belirle ve arama yoluna ekle
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)
from teamsPage import TeamsPage
from createTeamPage import CreateTeamPage
from profilePage import ProfilePage

# Ana sayfa sınıfı

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

