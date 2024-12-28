import sys
import os

# Proje kök dizinini belirle ve arama yoluna ekle
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from models.user import *
from models.team import *

activeUser = NormalUser(user_id=1,nickname="default Name",password="default Password",role="Normal")
activeTeam = Team(team_id=1,team_name="defaultName")