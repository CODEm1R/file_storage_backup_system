import tkinter as tk
from tkinter import filedialog, messagebox
import os, shutil
import mysql.connector

UPLOAD_DIR = '../file_backup_system/general_file'

def create_database_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="MySQL_316497",
            database="file_backup_system"
        )
        if connection.is_connected():
            return connection
    except mysql.connector.Error as e:
        messagebox.showerror("Database Error", f"Error connecting to database: {e}")
        return None

def fetch_files_list(owner_id):
    connection = create_database_connection()
    query = 'SELECT file_id, file_name, file_path, file_size, file_type FROM files WHERE owner_id = %s;'
    params = (owner_id,)

    try:
        cursor = connection.cursor()
        cursor.execute(query, params)
        result = cursor.fetchall()
        files_list = [(row[0], row[1], row[2], row[3], row[4]) for row in result]
        return files_list
    except Exception as e:
        messagebox.showerror("Error", f"Error fetching files: {e}")
        return []

def update_files_list(files_listbox, owner_id):
    files = fetch_files_list(owner_id)

    files_listbox.delete(0, tk.END)

    for file in files:
        files_listbox.insert(tk.END, file)

def upload_file(files_listbox, owner_id):
    connection = create_database_connection()
    file_path = filedialog.askopenfilename()
    if not file_path:
        return

    file_name = os.path.basename(file_path)
    file_type = os.path.splitext(file_name)[1]
    file_size = os.path.getsize(file_path)

    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)

    destination_path = os.path.join(UPLOAD_DIR, file_name)

    try:
        shutil.copy(file_path, destination_path)

        query = 'INSERT INTO files (owner_id, file_name, file_path, file_size, file_type) VALUES (%s, %s, %s, %s, %s)'
        params = (owner_id, file_name, destination_path, file_size, file_type)

        cursor = connection.cursor()
        cursor.execute(query, params)
        connection.commit()

        messagebox.showinfo('Info', 'File uploaded.')
        update_files_list(files_listbox, owner_id)
    except Exception as e:
        messagebox.showerror("Error", f"Error uploading file: {e}")

def delete_file(files_listbox, owner_id):
    connection = create_database_connection()
    selected = files_listbox.curselection()
    if not selected:
        messagebox.showwarning("Warning", "No file selected.")
        return

    target_file_id = files_listbox.get(selected[0])[0]

    query = 'SELECT file_path FROM files WHERE file_id = %s AND owner_id = %s;'
    params = (target_file_id, owner_id)

    try:
        cursor = connection.cursor()
        cursor.execute(query, params)
        result = cursor.fetchone()

        if not result:
            messagebox.showerror("Error", "File not found or access denied.")
            return

        file_path = result[0]
        if os.path.exists(file_path):
            os.remove(file_path)

        query = 'DELETE FROM files WHERE file_id = %s;'
        params = (target_file_id,)
        cursor.execute(query, params)
        connection.commit()

        messagebox.showinfo('Info', 'File deleted.')
        update_files_list(files_listbox, owner_id)
    except Exception as e:
        messagebox.showerror("Error", f"Error deleting file: {e}")


# Girilen team_id'ye göre file_id'leri bulma
def get_file_ids_for_team(team_id):
    conn = create_database_connection()
    if conn is None:
        return []
    
    cursor = conn.cursor()
    cursor.execute("SELECT file_id FROM file_sharing WHERE team_id = %s", (team_id,))
    file_ids = cursor.fetchall()
    conn.close()
    return [file_id[0] for file_id in file_ids]


# file_id'ye göre dosya bilgilerini alma
def get_file_details(file_ids):
    conn = create_database_connection()
    if conn is None:
        return []
    
    cursor = conn.cursor()
    # file_id'leri veritabanına güvenli bir şekilde geçirmek için '%s' kullanıyoruz
    cursor.execute(f"SELECT file_name, file_path, file_size, file_type, owner_id FROM files WHERE file_id IN ({','.join(['%s'] * len(file_ids))})", tuple(file_ids))
    file_details = cursor.fetchall()
    conn.close()
    return file_details
