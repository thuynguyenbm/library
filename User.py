from flask_login import UserMixin
from werkzeug.security import check_password_hash


class User(UserMixin):
    def __init__(self, id, name, password):
        self.id = id
        self.name = name
        self.password = password

    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    @staticmethod
    def get(id, db):
        cursor = db.cursor()
        sql = "SELECT * FROM user WHERE id = %s"
        val = (id, )
        cursor.execute(sql, val)
        result = cursor.fetchone()
        if result:
            return User(result[0], result[1], result[2])
        return None

    @staticmethod
    def getAll(db):
        cursor = db.cursor()
        sql = "SELECT * FROM user"
        cursor.execute(sql)
        result = cursor.fetchall()
        return result   
    
    @staticmethod
    def getName(id, db):
        cursor = db.cursor()
        sql = "SELECT * FROM user WHERE id = %s"
        cursor.execute(sql, (id,))
        result = cursor.fetchone()
        return result[1]  
    
    @staticmethod
    def getFromName(name, db):
        cursor = db.cursor()
        sql = "SELECT * FROM user WHERE name = %s"
        cursor.execute(sql, (name,))
        result = cursor.fetchone()
        if result:
            return User(result[0], result[1], result[2])
        return None 
