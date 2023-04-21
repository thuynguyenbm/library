from flask import Flask, render_template, request, Response,redirect,url_for
from flask_cors import CORS, cross_origin
import mysql.connector
import datetime
app = Flask(__name__)
CORS(app, supports_credentials=True) 

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="123456789",
    database="db"
)

cursor = mydb.cursor( buffered=True)

class Note():

    def __init__(self, id, description, status):
        self.id = id
        self.description = description
        self.status = status

@app.route("/")
def list():
    cursor = mydb.cursor()
    cursor.execute('select * from todolist;')
    notes = []
    for(id, description, status) in cursor:
        notes.append(Note(id, description, status))
    return render_template('home.html',notes=notes)

@app.route("/api/add", methods = ['POST'])
def addNote():
    description=request.form.get('description')
    cursor = mydb.cursor()
    query='insert into todolist( description, status) values(%s,0);'
    cursor.execute(query,(description,))
    cursor.execute("commit;")
    return redirect(url_for('list'))

@app.route("/api/edit", methods = ['POST'])
def editNote():
    description=request.form.get('description')
    id=request.args.get('id')
    cursor = mydb.cursor()
    query='update todolist set description = %s where id = %s;'
    cursor.execute(query,(description,  id))
    cursor.execute("commit;")
    return redirect(url_for('list'))


@app.route("/api/done:<id>", methods = ['GET'])
def updateStatusNote(id):
    cursor = mydb.cursor()
    query='update todolist set status = 1 where id = %s;'
    cursor.execute(query,(id,))
    cursor.execute("commit;")
    return redirect(url_for('list'))

@app.route("/api/delete:<id>", methods = ['GET'])
def deleteNote(id):
    cursor = mydb.cursor()
    query='delete from todolist where id = %s;'
    cursor.execute(query,(id,))
    cursor.execute("commit;")
    return redirect(url_for('list'))

if __name__ == '__main__':
    app.run(debug=True)