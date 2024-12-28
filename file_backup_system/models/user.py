class User:
    def __init__(self,user_id,nickname,password,role):
        """
        Kullanici adi ve sifre özelliklerini başlatır.
        """
        self.user_id = user_id
        self.nickname = nickname
        self.password = password
        self.role = role

class AdminUser(User):
    def __init__(self, user_id, nickname, password):
        super().__init__(user_id, nickname, password,role="Admin") 

class NormalUser(User):
    def __init__(self, user_id, nickname, password, role):
        super().__init__(user_id, nickname, password, role="Normal")       