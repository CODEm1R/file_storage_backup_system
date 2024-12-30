import logging
from logging.handlers import RotatingFileHandler
import os

# Log dosyalarının kayıt dizini
LOG_DIR = r'C:\Users\90541\Documents\GitHub\file_storage_backup_system\file_backup_system\log_files'

# Eğer log dizini yoksa oluştur
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

# Loglama yapılandırma fonksiyonu
def setup_logger(name, log_file, level=logging.INFO):
    """
    Belirtilen dosyaya log yazacak bir logger oluşturur.
    """
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    handler = RotatingFileHandler(log_file, maxBytes=5 * 1024 * 1024, backupCount=5)
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger

# Farklı işlemler için loggerlar
abnormal_logger = setup_logger("abnormal_logger", os.path.join(LOG_DIR, "abnormal_log.txt"))
backup_logger = setup_logger("backup_logger", os.path.join(LOG_DIR, "backup_log.txt"))
file_logger = setup_logger("file_logger", os.path.join(LOG_DIR, "file_sharing_log.txt"))
login_logger = setup_logger("login_logger", os.path.join(LOG_DIR, "login_log.txt"))
password_logger = setup_logger("password_logger", os.path.join(LOG_DIR, "password_change_log.txt"))
request_logger = setup_logger("request_logger", os.path.join(LOG_DIR, "request_log.txt"))
team_logger = setup_logger("team_logger", os.path.join(LOG_DIR, "team_member_log.txt"))
