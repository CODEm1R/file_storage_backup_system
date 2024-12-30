import mysql.connector
import tkinter as tk 
from tkinter import messagebox
import bcrypt
from logging_operations import *

def connect_db():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        passwd='MySQL_316497',
        database='file_backup_system'
    )

def create_request(new_password, requester_id, state):
    connection = connect_db()
    cursor = connection.cursor()
    try:
        cursor.execute("""
            INSERT INTO requests (new_password, requester_id, state)
            VALUES (%s, %s, %s)
        """, (new_password, requester_id, state))
        connection.commit()
        messagebox.showinfo("Basarili","Parola degistirme istegi olustu")
        password_logger.info(f"{requester_id} id'li kullanici sifre degistirme talebinde bulundu. Talep edilen sifre: {new_password}")        
        print("Yeni request başarıyla eklendi.")
    except mysql.connector.Error as e:
        print(f"Veritabanı hatası: {e}")
    finally:
        cursor.close()
        connection.close()

def get_all_requests():
    connection = connect_db()
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT * FROM requests")
        return cursor.fetchall()
    except mysql.connector.Error as e:
        print(f"Veritabanı hatası: {e}")
        return []
    finally:
        cursor.close()
        connection.close()

def update_requests_list(requests_listbox):
    users = get_all_requests()

    requests_listbox.delete(0, tk.END)

    for user in users:
        requests_listbox.insert(tk.END, user)    

def change_request_state(request_id, state):
    print(f"request id : {request_id}")
    connection = connect_db()
    cursor = connection.cursor()
    try:
        if state == "Confirm":
            # Şifre değiştir
            cursor.execute("SELECT new_password, requester_id FROM requests WHERE request_id = %s", (request_id,))
            result = cursor.fetchone()
            if result:
                new_password, requester_id = result
                print(f"result: {result}")
                hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
                cursor.execute("UPDATE requests SET state = %s WHERE request_id = %s", (state, request_id))
                cursor.execute("UPDATE users SET user_password = %s WHERE user_id = %s", (hashed_password, requester_id))
                messagebox.showinfo("Onay","Sifre Onaylandi")
                request_logger.info(f"Admin {requester_id} id'li kullanicinin {request_id} numarali sifre degistirme talebini onayladi. Yeni sifre: {hashed_password}")
                print("Şifre başarıyla değiştirildi.")
            else:
                messagebox.showinfo("Hata","Istek bulunamadi")
                print("Request bulunamadı.")

        elif state == "Not Accept":
            cursor.execute("UPDATE requests SET state = %s WHERE request_id = %s", (state, request_id))
            messagebox.showinfo("Onay","Istek reddedildi")
            request_logger.info(f"Admin {requester_id} idli kullanicinin {request_id} numarali sifre degistirme talebini reddetti.")
            print("Request kabul edilmedi.")

        elif state == "Wait":
            # İşlem yapılmasın
            messagebox.showinfo("Beklemede","Istek Beklemede")
            request_logger.info(f"Admin {requester_id} idli kullanicinin {request_id} numarali sifre degistirme talebini bekletiliyor.")
            print("Bekleme durumu: İşlem yapilmadi.")

        else:
            messagebox.showinfo("HATA","Gecersiz state")
            request_logger.warning(f"{request_id} numarali istek için beklenmeyen state degeri olustu. State: {state}")
            print("Geçersiz state parametresi.")

        connection.commit()
    except mysql.connector.Error as e:
        messagebox.showinfo("HATA","Veritabani Hatasi")
        request_logger.error(f"{request_id} numarali sifre degistirme talebi işlemi sirasinda hata olustu. Hata: {e}")
        print(f"Veritabani hatasi: {e}")
    finally:
        cursor.close()
        connection.close()


def get_request_by_id(request_id):
    connection = connect_db()
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT * FROM requests WHERE request_id = %s", (request_id,))
        return cursor.fetchone()
    except mysql.connector.Error as e:
        print(f"Veritabanı hatası: {e}")
        return None
    finally:
        cursor.close()
        connection.close()

def update_request(request_id, new_password=None, state=None):
    connection = connect_db()
    cursor = connection.cursor()
    try:
        if new_password:
            cursor.execute("UPDATE requests SET new_password = %s WHERE request_id = %s", (new_password, request_id))
        if state:
            cursor.execute("UPDATE requests SET state = %s WHERE request_id = %s", (state, request_id))
        connection.commit()
        print("Request başarıyla güncellendi.")
    except mysql.connector.Error as e:
        print(f"Veritabanı hatası: {e}")
    finally:
        cursor.close()
        connection.close()

def delete_request(request_id):
    connection = connect_db()
    cursor = connection.cursor()
    try:
        cursor.execute("DELETE FROM requests WHERE request_id = %s", (request_id,))
        connection.commit()
        print("Request başarıyla silindi.")
    except mysql.connector.Error as e:
        print(f"Veritabani hatasi: {e}")
    finally:
        cursor.close()
        connection.close()
