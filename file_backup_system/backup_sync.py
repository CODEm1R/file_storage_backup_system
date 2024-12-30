import os
import shutil
import time
import threading
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Kaynak ve hedef dizinler
SOURCE_DIR = '../file_storage_backup_system/file_backup_system/general_file'
TARGET_DIR = '../file_storage_backup_system/file_backup_system/general_file_backup'

def sync_directories(source_dir=SOURCE_DIR, target_dir=TARGET_DIR):
    """
    Kaynak ve hedef dizinleri senkronize eder.
    Yeni dosyaları ekler, değişenleri günceller ve fazlalıkları temizler.
    """
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)  # Hedef dizin yoksa oluştur
    
    # Kaynak dizinindeki dosyaları hedefe kopyala veya güncelle
    for root, dirs, files in os.walk(source_dir):
        relative_path = os.path.relpath(root, source_dir)
        target_root = os.path.join(target_dir, relative_path)
        
        if not os.path.exists(target_root):
            os.makedirs(target_root)
        
        for file in files:
            source_file = os.path.join(root, file)
            target_file = os.path.join(target_root, file)
            
            if not os.path.exists(target_file) or os.path.getmtime(source_file) > os.path.getmtime(target_file):
                shutil.copy2(source_file, target_file)
                print(f"Kopyalandı: {source_file} -> {target_file}")

    # Hedefteki fazlalıkları kontrol et ve sil
    for root, dirs, files in os.walk(target_dir):
        relative_path = os.path.relpath(root, target_dir)
        source_root = os.path.join(source_dir, relative_path)
        
        for file in files:
            target_file = os.path.join(root, file)
            source_file = os.path.join(source_root, file)
            
            if not os.path.exists(source_file):
                os.remove(target_file)
                print(f"Silindi: {target_file}")

        for dir in dirs:
            target_dir_path = os.path.join(root, dir)
            source_dir_path = os.path.join(source_root, dir)
            
            if not os.path.exists(source_dir_path):
                shutil.rmtree(target_dir_path)
                print(f"Silindi: {target_dir_path}")

class SyncHandler(FileSystemEventHandler):
    """
    Watchdog olaylarını işleyen sınıf. 
    Gerçek zamanlı değişiklikler algılandığında senkronizasyonu başlatır.
    """
    def __init__(self, source_dir, target_dir):
        """
        SyncHandler sınıfı, değişiklikleri algılayıp senkronize etmek için source_dir ve target_dir alır.
        """
        self.source_dir = source_dir
        self.target_dir = target_dir

    def on_any_event(self, event):
        """
        Dosya sistemi olayları algılandığında senkronizasyon başlatılır.
        """
        print(f'Detected change: {event}')
        sync_directories(self.source_dir, self.target_dir)

def manual_sync():
    """ Manuel yedekleme işlemini başlatır. """
    print("Manuel yedekleme başlatılıyor...")
    sync_directories(SOURCE_DIR, TARGET_DIR)
    print("Manuel yedekleme tamamlandı.")

def real_time_sync(source_dir, target_dir):
    """ Gerçek zamanlı senkronizasyonu başlatır. """
    print("Gerçek zamanlı senkronizasyon başlatılıyor...")
    event_handler = SyncHandler(source_dir, target_dir)
    observer = Observer()
    observer.schedule(event_handler, path=source_dir, recursive=True)
    observer.start()
    return observer

def periodic_sync():
    """ Periyodik olarak senkronizasyon yapar. """
    while True:
        sync_directories(SOURCE_DIR, TARGET_DIR)
        time.sleep(10)

def start_automatic_sync():
    """ Arka planda otomatik senkronizasyon başlatır. """
    sync_thread = threading.Thread(target=periodic_sync)
    sync_thread.daemon = True
    sync_thread.start()
    print("Arka planda otomatik senkronizasyon başlatıldı.")

def start_sync_on_startup():
    """ Uygulama açıldığında senkronizasyonu başlatır. """
    observer = real_time_sync(SOURCE_DIR, TARGET_DIR)
    return observer

def stop_sync_on_shutdown(observer):
    """ Uygulama kapanmadan önce senkronizasyonu durdurur. """
    observer.stop()
    observer.join()
    print("Senkranizasyon durduruldu.")

# GUI kısmı için fonksiyonlar
def on_closing(observer):
    """ Uygulama kapanırken senkronizasyonu durdurma. """
    stop_sync_on_shutdown(observer)