
# first try
class HomePage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        tk.Label(self, text="Ana Sayfa", font=("Arial", 20)).pack(pady=20)
        tk.Label(self, text="Hoş geldiniz!", font=("Arial", 14)).pack(pady=10)

        # "Takımlar" butonu
        tk.Button(self, text="Takimlarim", command=self.open_teams).pack(pady=10)

        # Takım Oluştur Butonu 
        tk.Button(self, text="Takim yap", command=lambda: parent.show_page(CreateTeamPage)).pack(pady=10)

        # "Profilim" butonu
        tk.Button(self, text="Profilim", command=lambda: parent.show_page(ProfilePage)).pack(pady=10)

    # Takımlar butonuna tıklanınca çalışacak fonksiyon
    def open_teams(self):
        print("Takımlar sayfasına yönlendiriliyor...")
        # parent.show_page(TeamsPage) gibi başka bir sayfaya yönlendirme yapılabilir.