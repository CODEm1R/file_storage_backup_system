import mysql.connector

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
            SELECT user_id, role 
            FROM users 
            WHERE user_name = %s AND user_password = %s
        """, (user_name, user_password))
        user = cursor.fetchone()
        
        if user:
            print(f"Giriş başarılı! Kullanıcı ID: {user[0]}, Rol: {user[1]}")
            # Burada ana sayfaya yönlendirme yapılabilir
            return True  # Giriş başarılı
        else:
            print("Hatalı kullanıcı adı veya şifre!")
            return False  # Giriş başarısız
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
            print("Kullanıcı bulunamadı!")
            return None  # Kullanıcı yoksa None döndür
    except mysql.connector.Error as e:
        print(f"Veritabanı hatası: {e}")
        return None
    finally:
        #cursor.close()
        connection.close()


# CREATE: Yeni kullanıcı ekleme
def create_user(user_name, user_password, role):
    connection = connect_db()
    cursor = connection.cursor()
    try:
        # Kullanıcı adının daha önce kullanılıp kullanılmadığını kontrol et
        cursor.execute("SELECT user_id FROM users WHERE user_name = %s", (user_name))
        existing_user = cursor.fetchone()

        if existing_user:
            print("Hata: Bu kullanıcı adı zaten kullanılıyor. Lütfen başka bir kullanıcı adı seçin.")
            return

        # Kullanıcı adı mevcut değilse yeni kullanıcı ekle
        cursor.execute("""
            INSERT INTO users (user_name, user_password, role)
            VALUES (%s, %s, %s)
        """, (user_name, user_password, role))
        connection.commit()
        print("Kullanıcı başarıyla eklendi.")
    except mysql.connector.Error as e:
        print(f"Veritabanı hatası: {e}")
    finally:
        cursor.close()
        connection.close()

# Tüm Kullanıcılar 
def get_all_users():
    connection = connect_db()
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT user_id, user_name, role FROM users")
        users = cursor.fetchall()
        return users  # Kullanıcıları bir liste olarak döndür
    except mysql.connector.Error as e:
        print(f"Veritabanı hatası: {e}")
        return []
    finally:
        cursor.close()
        connection.close()

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
        print(f"Veritabanı hatası: {e}")
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

# Örnek Kullanım
if __name__ == "__main__":
    # Yeni kullanıcı ekleme
    create_user("drogba", "password123", "admin")
    
    # Kullanıcıları listeleme
    print("Tüm kullanıcılar:")
    read_users()
    
    # Kullanıcı güncelleme
    update_user(user_id=1, user_name="mehmet.kaya", role="user")
    
    # Kullanıcı silme
    delete_user(user_id=1)
