import mysql.connector

class Student:
    def __init__(self, student_id, name, email):
        self.student_id = student_id
        self.name = name
        self.email = email



    @staticmethod
    def showAll(db):
        cursor = db.cursor()
        sql = "SELECT * FROM student"
        cursor.execute(sql, )
        result = cursor.fetchall()
        return result

    @staticmethod
    def get(id, db):
        cursor = db.cursor()
        sql = "SELECT * FROM student WHERE student_id = %s"
        val = (id, )
        cursor.execute(sql, val)
        result = cursor.fetchall()
        return result
    
    @staticmethod
    def getNameById(id, db):
        cursor = db.cursor()
        sql = "SELECT name FROM student WHERE student_id = %s"
        val = (id, )
        cursor.execute(sql, val)
        result = cursor.fetchall()
        if len(result)>0:
            return result[0]
        return None

    def add(self, db):
        cursor = db.cursor()
        sql = "INSERT INTO student (student_id, name, email) VALUES (%s, %s, %s)"
        val = (self.student_id, self.name, self.email)
        cursor.execute(sql, val)
        db.commit()