import mysql.connector

# Veritabanı bağlantısı
def connect_db():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        passwd='MySQL_316497',
        database='file_backup_system'
    )


def get_team_id_by_team_name(team_name):
    connection = connect_db()
    cursor = connection.cursor()
    try:
        cursor.execute("""
            SELECT team_id 
            FROM teams 
            WHERE team_name = %s
        """, (team_name,))
        team = cursor.fetchone()
        
        if team:
            return team[0]  # team_id'yi döndür
        else:
            print("Takım bulunamadı!")
            return None  # Takım yoksa None döndür
    except mysql.connector.Error as e:
        print(f"Veritabanı hatası: {e}")
        return None
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
        print("Takimlar:")
        for team in teams:
            print(f"ID: {team[0]}, Takim Adi: {team[1]}")
    except mysql.connector.Error as e:
        print(f"Veritabani hatasi: {e}")
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
        print("Takım bilgileri başarıyla güncellendi.")
    except mysql.connector.Error as e:
        print(f"Veritabanı hatası: {e}")
    finally:
        cursor.close()
        connection.close()

# DELETE: Takımı silme
def delete_team(team_id):
    connection = connect_db()
    cursor = connection.cursor()
    try:
        cursor.execute("DELETE FROM teams WHERE team_id = %s", (team_id,))
        connection.commit()
        print("Takım başarıyla silindi.")
    except mysql.connector.Error as e:
        print(f"Veritabanı hatası: {e}")
    finally:
        cursor.close()
        connection.close()
