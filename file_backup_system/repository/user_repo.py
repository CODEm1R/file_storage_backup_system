import tkinter as tk
from tkinter import messagebox

import mysql.connector
import bcrypt

# Veritabanı bağlantısı
def connect_db():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        passwd='MySQL_316497',
        database='file_backup_system'
    )


# LOGIN: Kullanıcı adı ve şifre doğrulama
def login_user(user_name, user_password):
    connection = connect_db()
    cursor = connection.cursor()
    try:
        cursor.execute("""
            SELECT user_id, user_name, user_password ,role 
            FROM users 
            WHERE user_name = %s AND user_password = %s
        """, (user_name, user_password))
        result = cursor.fetchone()
        
        if result:
            # Burada ana sayfaya yönlendirme yapılabilir
            return result  # Giriş başarılı
        else:
            print("Hatalı kullanıcı adı veya şifre!")
            return False  # Giriş başarısız
    except mysql.connector.Error as e:
        print(f"Veritabanı hatası: {e}")
        return False  # Giriş başarısız
    finally:
        cursor.close()
        connection.close()

def login_user_hash(user_name, user_password):
    connection = connect_db()
    cursor = connection.cursor()
    try:
        # Veritabanından kullanıcı bilgilerini al
        cursor.execute("""
            SELECT user_id, user_name, user_password, role, storage_limit 
            FROM users 
            WHERE user_name = %s
        """, (user_name,))
        result = cursor.fetchone()
        print(f"result : {result}")

        if result:
            user_id, db_user_name, hashed_password, role, storage_limit = result

            # Şifreyi doğrula
            if bcrypt.checkpw(user_password.encode('utf-8'), hashed_password.encode('utf-8')):
                print(f"{user_password.encode('utf-8')} , {hashed_password}")
                # Giriş başarılı, bilgileri döndür
                return result
            else:
                messagebox.showwarning("Hata","Şifre Hatalı")
                print("Hatalı şifre!")
                return False  # Şifre hatalı
        else:
            print("Kullanıcı bulunamadı!")
            return False  # Kullanıcı adı bulunamadı
    except mysql.connector.Error as e:
        print(f"Veritabanı hatası: {e}")
        return False  # Giriş başarısız
    finally:
        cursor.close()
        connection.close()

def get_user_id_by_name(user_name):
    connection = connect_db()
    cursor = connection.cursor()
    try:
        cursor.execute("""
            SELECT user_id 
            FROM users 
            WHERE user_name = %s
        """, (user_name,))
        user = cursor.fetchone()
        
        if user:
            return user[0]  # user_id'yi döndür
        else:
            print("Kullanici bulunamadı!")
            return None  # Kullanıcı yoksa None döndür
    except mysql.connector.Error as e:
        print(f"Veritabanı hatası: {e}")
        return None
    finally:
        #cursor.close()
        connection.close()


# CREATE: Yeni kullanıcı ekleme
def create_user(user_name, user_password, role, storage_limit):
    connection = connect_db()
    cursor = connection.cursor()
    try:
        # Kullanıcı adının daha önce kullanılıp kullanılmadığını kontrol et
        cursor.execute("SELECT user_id FROM users WHERE user_name = %s", (user_name,))
        existing_user = cursor.fetchone()

        if existing_user:
            messagebox.showwarning("Hata","Bu isim kullanılıyor")
            print("Hata: Bu kullanıcı adı zaten kullanılıyor. Lütfen başka bir kullanıcı adı seçin.")
            return

        # Şifreyi hashle
        hashed_password = bcrypt.hashpw(user_password.encode('utf-8'), bcrypt.gensalt())

        # Kullanıcı adı mevcut değilse yeni kullanıcı ekle
        cursor.execute("""
            INSERT INTO users (user_name, user_password, role, storage_limit)
            VALUES (%s, %s, %s, %s)
        """, (user_name, hashed_password, role, storage_limit))
        connection.commit()
        messagebox.showinfo("Eklendi","Kullanici ekleme basarili")
        print("Kullanici başariyla eklendi.")
    except mysql.connector.Error as e:
        messagebox.showwarning("Hata","Veritabaninda hata olustu !")
        print(f"Veritabani hatasi: {e}")
    finally:
        cursor.close()
        connection.close()

# Tüm Kullanıcılar 
def get_all_users():
    connection = connect_db()
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT user_id, user_name, role, storage_limit FROM users")
        users = cursor.fetchall()
        return users  # Kullanıcıları bir liste olarak döndür
    except mysql.connector.Error as e:
        print(f"Veritabani hatasi: {e}")
        return []
    finally:
        cursor.close()
        connection.close()

def update_users_list(users_listbox):
    users = get_all_users()

    users_listbox.delete(0, tk.END)

    for user in users:
        users_listbox.insert(tk.END, user)

# READ: Tüm kullanıcıları listeleme
def read_users():
    connection = connect_db()
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT user_id, user_name, role FROM users")
        users = cursor.fetchall()
        print("Kullanıcılar:")
        for user in users:
            print(f"ID: {user[0]}, Ad: {user[1]}, Rol: {user[2]}")
    except mysql.connector.Error as e:
        print(f"Veritabanı hatası: {e}")
    finally:
        cursor.close()
        connection.close()

# UPDATE: Kullanıcı bilgilerini güncelleme
def update_user(user_id, user_name=None, user_password=None, role=None):
    connection = connect_db()
    cursor = connection.cursor()
    try:
        if user_name:
            cursor.execute("UPDATE users SET user_name = %s WHERE user_id = %s", (user_name, user_id))
        if user_password:
            cursor.execute("UPDATE users SET user_password = %s WHERE user_id = %s", (user_password, user_id))
        if role:
            cursor.execute("UPDATE users SET role = %s WHERE user_id = %s", (role, user_id))
        connection.commit()
        print("Kullanıcı bilgileri başarıyla güncellendi.")
    except mysql.connector.Error as e:
        print(f"Veritabani hatasi: {e}")
    finally:
        cursor.close()
        connection.close()

def update_user_name(user_id, user_name):
    connection = connect_db()
    cursor = connection.cursor()
    try:
        if user_name:
            cursor.execute("UPDATE users SET user_name = %s WHERE user_id = %s", (user_name, user_id))     
        connection.commit()    
    except mysql.connector.Error as e:  
        print(f"Veritabani hatasi: {e}")
        messagebox.showwarning("Hata","Veritabanina baglanamadi")
    finally:
        cursor.close
        connection.close                     

def update_storage_limit(user_id, new_storage_limit):
    connection = connect_db()
    cursor = connection.cursor()
    try:
        cursor.execute(
            "UPDATE users SET storage_limit = %s WHERE user_id = %s",
            (new_storage_limit, user_id)
        )
        connection.commit()
        print(f"Kullanıcının storage_limit başarıyla {new_storage_limit} olarak güncellendi.")
        messagebox.showinfo("Basarili",f"{user_id} kulalnicisi storage_limit başariyla {new_storage_limit} olarak güncellendi.")
    except mysql.connector.Error as e:
        print(f"Veritabanı hatası: {e}")
        messagebox.showwarning("Hata","Limit guncelleme basarisiz oldu")
    finally:
        cursor.close()
        connection.close()        

# DELETE: Kullanıcıyı silme
def delete_user(user_id):
    connection = connect_db()
    cursor = connection.cursor()
    try:
        cursor.execute("DELETE FROM users WHERE user_id = %s", (user_id,))
        connection.commit()
        print("Kullanıcı başarıyla silindi.")
    except mysql.connector.Error as e:
        print(f"Veritabanı hatası: {e}")
    finally:
        cursor.close()
        connection.close()


