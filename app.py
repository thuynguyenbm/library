from flask import Flask, render_template, request, redirect, url_for,session
from Book import Book
from User import User
from BorrowItem import BorrowItem
from BorrowList import BorrowList
from Student import Student
import mysql.connector,os
import pandas as pd
from flask_login import LoginManager, login_user, login_required, logout_user,current_user

app = Flask(__name__)
app.secret_key = '1901040219'
app.config['PERMANENT_SESSION_LIFETIME'] = 1800

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="123456789",
    database="books"
)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

def getUserName():
    user_id=session.get('user_id')
    if(not user_id):
        return redirect(url_for('login'))
    return User.getName(user_id,db)

@login_manager.user_loader
def load_user(user_id):
    u = User.get(user_id,db)
    return User.get(user_id,db)

@app.route("/", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated and session.get('user_id') != None:
        return redirect(url_for('home', page=1))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.getFromName(username,db)
        if user and user.check_password(password):
            session['user_id'] = user.id
            login_user(user, remember=True)
            return redirect(url_for('home', page=1))
        return 'Tên đăng nhập hoặc mật khẩu không đúng'
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route("/<int:page>")
def home(page):
    per_page = 10
    start_index = (page - 1) * per_page
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM book ORDER BY title asc LIMIT {start_index}, {per_page}")
    books = cursor.fetchall()
    cursor.execute(f"SELECT COUNT(*) FROM book")
    max_page = cursor.fetchone()
    cursor.execute(f"SELECT DISTINCT genre FROM book ORDER BY genre asc")
    genres = cursor.fetchall()
    return render_template("index.html", books=books, page=page, len=len(books), genres=genres, genreSize=len(genres), max_page=max_page[0]/10, user_name = getUserName())

@app.route("/search")
@login_required
def search():
    cursor = db.cursor()
    cursor.execute(f"SELECT DISTINCT genre FROM book ORDER BY genre asc")
    genres = cursor.fetchall()
    keyword = request.args.get("keyword")

    books = Book.search(keyword, db)

    return render_template("index.html", keyword=keyword, books=books, page=1, len=len(books), genres=genres, genreSize=len(genres), max_page=1, user_name = getUserName())

@app.route("/filter")
@login_required
def filter():
    genre = request.args.get("genre")
    if(genre!="All Genres"):
        filteredBooks = Book.filter(genre, db)
        cursor = db.cursor()
        cursor.execute(f"SELECT DISTINCT genre FROM book ORDER BY genre asc")
        genres = cursor.fetchall()
    else:
        filteredBooks = Book.showAll(db)
    return render_template('index.html',books=filteredBooks, page=1, len=len(filteredBooks), genres=genres, genreSize=len(genres), max_page=1, user_name = getUserName())

@app.route('/books/add', methods=['GET', 'POST'])
@login_required
def add_book():
    cursor = db.cursor()
    cursor.execute(f"SELECT DISTINCT genre FROM book ORDER BY genre asc")
    genres = cursor.fetchall()
    if request.method == 'POST':
        id = request.form['id']
        title = request.form['title']
        author = request.form['author']
        location = request.form['location']
        genre = request.form['genre']
        published_date = request.form['published_date']
        publishing_house = request.form['publishing_house']
        amount = request.form['amount']


        Book.add(Book(id, title, author, location, genre, published_date, publishing_house, amount, 0),db)

        return redirect(url_for('home',page=1))
    else:
        return render_template('add.html',books=None, len=0, genres=genres, genreSize=len(genres), user_name = getUserName())
    
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    book = Book.get(id, db)
    cursor = db.cursor()
    cursor.execute(f"SELECT DISTINCT genre FROM book ORDER BY genre asc")
    genres = cursor.fetchall()
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        location = request.form['location']
        genre = request.form['genre']
        published_date = request.form['published_date']
        publishing_house = request.form['publishing_house']
        amount = request.form['amount']
        occupancy = request.form['occupancy']

        Book.update(Book(id, title,author, location, genre, published_date, publishing_house, amount, occupancy),id,db)

        return redirect(url_for('home', page=1))

    return render_template('edit.html', book=book, genres=genres, genreSize=len(genres), id= id, max_page=1, user_name = getUserName())

@app.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete(id):
    book = Book.query.get(id)

    db.session.delete(book)
    db.session.commit()

    return redirect(url_for('home', page=1))

@app.route('/borrow', methods=['GET','POST'])
@login_required
def borrow_book():
    cursor = db.cursor(buffered=True)
    cursor.execute(f"SELECT * FROM(SELECT  id, title, author, genre, (amount-occupancy) AS amount_left FROM book) mytable  WHERE amount_left>0 ORDER BY title")
    books = cursor.fetchall()
    cursor.execute(f"SELECT DISTINCT genre FROM book ORDER BY genre asc")
    genres = cursor.fetchall()
    if request.method == 'POST':
        selected_books = request.form.getlist('books')
        student_id = request.form.get('student_id')
        student_name=Student.getNameById(student_id,db)
        BorrowList.add(BorrowList(-1, student_id, None, None, session.get('user_id')),db)
        cursor = db.cursor(buffered=True)
        cursor.execute(f"SELECT borrow_id FROM borrow_order_list WHERE student_id = {student_id} ORDER BY borrow_id desc")
        borrow_id= cursor.fetchone()
        borrow_list=BorrowList.get(borrow_id[0],db)
        list=[]
        for book_id in selected_books:
            book=Book.get(book_id,db)
            BorrowItem.add(BorrowItem(borrow_id[0], book_id, 1, 0, None),db)
            Book.update(Book(book[0][0], book[0][1], book[0][2], book[0][3], book[0][4], book[0][5], book[0][6], book[0][7], book[0][8]+1), book[0][0], db)
            list.append(Book.get(book_id,db))
        return render_template('borrow_order.html', borrow_list=borrow_list[0], list=list, genres=genres, genreSize=len(genres), len=len(list),student_name=student_name, user_name = getUserName())
    return render_template('borrow.html', books=books, genres=genres, genreSize=len(genres), len=len(books), user_name = getUserName())

@app.route('/return/<student_id>', methods=['GET','POST'])
@login_required
def return_book(student_id):
    cursor = db.cursor(buffered=True)
    student_name = Student.getNameById(student_id,db)
    if student_name:
        cursor.execute("SELECT bi.book_id, b.title AS book_title, b.author, SUM(bi.amount) AS total_amount, s.name AS student_name, bol.borrow_date, bol.due_date \
FROM borrow_item AS bi \
JOIN book AS b ON bi.book_id = b.id \
JOIN borrow_order_list AS bol ON bi.borrow_id = bol.borrow_id \
JOIN student AS s ON bol.student_id = s.student_id \
WHERE bi.status = 0 AND bol.student_id = %s \
GROUP BY bi.book_id, bol.due_date, s.name \
ORDER BY bol.due_date ASC;", (student_id,))
        books = cursor.fetchall()
        cursor.execute(f"SELECT DISTINCT genre FROM book ORDER BY genre asc")
        genres = cursor.fetchall()
        cursor.execute("SELECT DATE_FORMAT(CURDATE(), '%Y-%m-%d');")
        return_date = cursor.fetchone()
        if request.method == 'POST':
            selected_books = request.form.getlist('books')
            return_amount = request.form.getlist('r_amount')
            # cursor = db.cursor(buffered=True)
            # cursor.execute(f"SELECT borrow_id FROM borrow_order_list WHERE student_id = {student_id} ORDER BY borrow_id desc")
            list=[]
            b_list=[]
            r_list=[]
            for index in range(len(selected_books)):
                if(return_amount[index]):
                    cursor = db.cursor(buffered=True)
                    cursor.execute("UPDATE borrow_item \
SET status = 1, return_date = curdate() \
WHERE book_id = %s \
  AND status = 0 \
  AND borrow_id IN ( \
    SELECT borrow_id \
    FROM borrow_order_list \
    WHERE student_id = %s \
) \
LIMIT %s;", (selected_books[index], student_id, int(return_amount[index])))
                    cursor.execute("UPDATE book SET occupancy = occupancy - %s WHERE id = %s;", (int(return_amount[index]), selected_books[index]))
                    cursor.execute("COMMIT;")
                    book=Book.get(selected_books[index],db)
                    list.append(book)
                    b_list.append(books[index][5])
                    r_list.append(return_amount[index])
            return render_template('return_list.html', student_name=student_name, books=books,r_list=r_list, list=list, genres=genres, genreSize=len(genres), len=len(list), return_date=return_date,student_id=student_id, user_name = getUserName(), b_list=b_list)
        return render_template('return.html', student_name=student_name, books=books, genres=genres, genreSize=len(genres), len=len(books),student_id=student_id, user_name = getUserName())
    return redirect(url_for('home', page=1))


if __name__ == "__main__":
    app.run(debug=True)