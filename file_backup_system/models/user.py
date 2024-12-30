class User:
    def __init__(self,user_id,nickname,password,role,storage_limit):
        """
        Kullanici adi ve sifre özelliklerini başlatır.
        """
        self.user_id = user_id
        self.nickname = nickname
        self.password = password
        self.role = role
        self.storage_limit = storage_limit
        

class AdminUser(User):
    def __init__(self, user_id, nickname, password, role, storage_limit):
        super().__init__(user_id, nickname, password,role="Admin",storage_limit=50) 

class NormalUser(User):
    def __init__(self, user_id, nickname, password, role, storage_limit):
        super().__init__(user_id, nickname, password, role="Normal",storage_limit=50)       