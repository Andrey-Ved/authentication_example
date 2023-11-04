from app.core.db_base import BaseDAO
from app.users.models import Users


class UserDAO(BaseDAO):
    model = Users


print('init users dao')
