import mysql.connector
import tkinter as tk
from tkinter import messagebox
from logging_operations import *

# Veritabanı bağlantısı
def connect_db():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        passwd='MySQL_316497',
        database='file_backup_system'
    )

# CREATE: Yeni takım üyesi ekleme
def add_team_member(user_id, team_id):
    connection = connect_db()
    cursor = connection.cursor()
    try:
        cursor.execute("""
            INSERT INTO team_member (user_id, team_id)
            VALUES (%s, %s)
        """, (user_id, team_id))
        connection.commit()
        print("Takım üyesi başarıyla eklendi.")
        messagebox.showinfo("Basarili",f"{user_id} kullanicisi {team_id} takimina eklendi")
        team_logger.info(f"{user_id} id'li kullanici {team_id} id'li takima uye olarak eklendi.")
    except mysql.connector.Error as e:
        team_logger.error(f"{user_id} id'li kullanici {team_id} id'li takima uye olarak eklenirken hata olustu. Hata: {e}")
        print(f"Veritabanı hatası: {e}")
    finally:
        #cursor.close()
        connection.close()

# Kullanıcının takımlarını getirme
def get_user_teams_by_user_id(user_id):
    connection = connect_db()
    cursor = connection.cursor()
    try:
        cursor.execute("""
            SELECT t.team_id , t.team_name 
            FROM teams t
            JOIN team_member tm ON t.team_id = tm.team_id
            WHERE tm.user_id = %s
        """, (user_id,))
        teams = cursor.fetchall()
        print(f"Repodaki teams: {teams}")
        return teams
    except mysql.connector.Error as e:
        print(f"Veritabanı hatası: {e}")
        return []
    finally:
        cursor.close()
        connection.close()

def update_teams_list(teams_listbox, user_id):
    teams = get_user_teams_by_user_id(user_id=user_id)

    teams_listbox.delete(0, tk.END)

    for team in teams:
        teams_listbox.insert(tk.END, team)


# UPDATE: Takım üyesi bilgisini güncelleme
def update_team_member(user_id, team_id, new_role=None):
    connection = connect_db()
    cursor = connection.cursor()
    try:
        if new_role:
            cursor.execute("""
                UPDATE team_member 
                SET role = %s 
                WHERE user_id = %s AND team_id = %s
            """, (new_role, user_id, team_id))
        connection.commit()
        print("Takım üyesi başarıyla güncellendi.")
    except mysql.connector.Error as e:
        print(f"Veritabanı hatası: {e}")
    finally:
        cursor.close()
        connection.close()

# DELETE: Takım üyesini silme
def remove_team_member(user_id, team_id):
    connection = connect_db()
    cursor = connection.cursor()
    try:
        cursor.execute("""
            DELETE FROM team_member 
            WHERE user_id = %s AND team_id = %s
        """, (user_id, team_id))
        connection.commit()
        team_logger.info(f"{user_id} id'li kullanici {team_id} id'li takim uyeliginden silindi.")
        print("Takım üyesi başarıyla silindi.")
    except mysql.connector.Error as e:
        team_logger.error(f"{user_id} id'li kullanici {team_id} id'li takim üyeliginden silinirken hata olustu. Hata: {e}")
        print(f"Veritabanı hatası: {e}")
    finally:
        cursor.close()
        connection.close()

# CREATE: Yeni takım ekleme
def create_team(team_name):
    connection = connect_db()
    cursor = connection.cursor()
    try:
        cursor.execute("""
            INSERT INTO teams (team_name)
            VALUES (%s)
        """, (team_name,))
        connection.commit()
        print("Takım başarıyla eklendi.")
    except mysql.connector.Error as e:
        print(f"Veritabanı hatası: {e}")
    finally:
        cursor.close()
        connection.close()

# READ: Tüm takımları listeleme
def read_teams():
    connection = connect_db()
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT team_id, team_name FROM teams")
        teams = cursor.fetchall()
        print("Takımlar:")
        for team in teams:
            print(f"ID: {team[0]}, Takım Adı: {team[1]}")
    except mysql.connector.Error as e:
        print(f"Veritabanı hatası: {e}")
    finally:
        cursor.close()
        connection.close()

# UPDATE: Takım bilgilerini güncelleme
def update_team(team_id, team_name=None):
    connection = connect_db()
    cursor = connection.cursor()
    try:
        if team_name:
            cursor.execute("UPDATE teams SET team_name = %s WHERE team_id = %s", (team_name, team_id))
        connection.commit()
        print("Takım bilgileri başariyla güncellendi.")
    except mysql.connector.Error as e:
        print(f"Veritabani hatasi: {e}")
    finally:
        cursor.close()
        connection.close()

