import mysql.connector
import tkinter as tk 
from tkinter import messagebox
import bcrypt

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
                print("Şifre başarıyla değiştirildi.")
            else:
                messagebox.showinfo("Hata","Istek bulunamadi")
                print("Request bulunamadı.")

            # Request sil
            # cursor.execute("DELETE FROM requests WHERE request_id = %s", (request_id,))
            # messagebox.showinfo("Onay","Sifre Silindi")
            # print("Request silindi.")

        elif state == "Not Accept":
            cursor.execute("UPDATE requests SET state = %s WHERE request_id = %s", (state, request_id))
            messagebox.showinfo("Onay","Istek reddedildi")
            print("Request kabul edilmedi.")

        elif state == "Wait":
            # İşlem yapılmasın
            messagebox.showinfo("Beklemede","Istek Beklemede")
            print("Bekleme durumu: İşlem yapilmadi.")

        else:
            messagebox.showinfo("HATA","Gecersiz state")
            print("Geçersiz state parametresi.")

        connection.commit()
    except mysql.connector.Error as e:
        messagebox.showinfo("HATA","Veritabani Hatasi")
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
