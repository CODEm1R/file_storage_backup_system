import mysql.connector
import tkinter as tk
from tkinter import messagebox

def share_file_with_team(file_id, team_id):
    """
    MySQL'deki file_sharing tablosuna bir dosya ile takım ilişkisi ekler.

    :param files_listbox: Dosya ID'lerini içeren liste
    :param teams_listbox: Takım ID'lerini içeren liste
    """
    try:
        # MySQL bağlantısı
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="MySQL_316497",
            database="file_backup_system"
        )
        cursor = connection.cursor()

        # Dosya ve takım ID'lerini al
       
        # İlgili ilişkiyi tabloya ekle
        insert_query = """
        INSERT INTO file_sharing (file_id, team_id) 
        VALUES (%s, %s)
        """
        cursor.execute(insert_query, (file_id, team_id))

        # Değişiklikleri kaydet
        connection.commit()
        messagebox.showinfo("Basarili","Dosya paylasildi")
        print("Dosya ve takım ilişkileri başarıyla eklendi.")

    except mysql.connector.Error as error:
        print(f"MySQL hatası: {error}")
    
def delete_file_sharing(file_id, team_id):
    """
    MySQL'deki file_sharing tablosundan belirtilen dosya ve takım ilişkisini siler.

    :param file_id: Silinecek dosyanın ID'si
    :param team_id: Silinecek takımın ID'si
    """
    try:
        # MySQL bağlantısı
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="MySQL_316497",
            database="file_backup_system"
        )
        cursor = connection.cursor()

        # Dosya ve takım ID'sine göre ilişkileri sil
        delete_query = """
        DELETE FROM file_sharing 
        WHERE file_id = %s AND team_id = %s
        """
        cursor.execute(delete_query, (file_id, team_id))

        # Değişiklikleri kaydet
        connection.commit()

        # Kullanıcıya bilgi ver
        if cursor.rowcount > 0:
            messagebox.showinfo("Başarili", "Dosya paylaşımı silindi.")
            print("Dosya ve takim ilişkisi başarıyla silindi.")
        else:
            messagebox.showwarning("Uyari", "Belirtilen dosya ve takim ilişkisi bulunamadi.")
            print("Silinecek kayit bulunamadi.")

    except mysql.connector.Error as error:
        print(f"MySQL hatası: {error}")
        messagebox.showerror("Hata", f"MySQL hatası: {error}")

    finally:
        # Bağlantıyı kapat
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL bağlantısı kapatıldı.")
    
