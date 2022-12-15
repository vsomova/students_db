from flask import Flask, render_template, request, url_for, flash, redirect
import datetime
import mysql.connector
conn = mysql.connector.connect(host="localhost", user="root", password="12345", database="cmpsc363_final")
cursor = conn.cursor()

def get_names():
    result = set()
    cursor.execute("select name from Authors")
    records = cursor.fetchall()
    for row in records:
        result.add(row[0])
    return result

def get_titles():
    result = set()
    cursor.execute("select title from Books")
    records = cursor.fetchall()
    for row in records:
        result.add(row[0])
    return result


try:
    with open('schema.sql', 'r') as f:
        cursor.execute(f.read(), multi=True)
        conn.commit()
except Exception:
    pass #tables exist

try:
    for line in open('sample.sql', 'r'):
        cursor.execute(line)
    conn.commit()
except Exception as e:
    pass


app = Flask(__name__)
app.config['SECRET_KEY'] = '3f0c4747101d85a1fb314f9b4bbdc94795848112a6850082'

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/authors_table")
def authors_table():
    cursor.execute("select * from Authors")
    value = cursor.fetchall()
    return render_template("authors_table.html", data=value, name="Authors")

@app.route("/a_insert", methods=('GET', 'POST'))
def a_insert():
    if request.method == 'POST':
        add_author = ("INSERT INTO Authors "
                      "(name, addr) "
                      "VALUES (%(name)s, %(addr)s)")

        name = request.form['name']
        addr = request.form['addr']

        result = get_names()

        if not name:
            flash('Name is required!')
        elif name in result:
            flash('Name should be unique!')

        else:
            new_author = {'name': name, 'addr': addr}
            cursor.execute(add_author, new_author)
            conn.commit()

            return redirect(url_for('index'))

    return render_template('a_insert.html')


@app.route("/a_delete", methods=('GET', 'POST'))
def a_delete():
    if request.method == 'POST':
        dr = "DELETE FROM Authors WHERE name = %s"

        name = request.form['name']


        if name not in get_names():
            flash('This student does not exist')
        else:
            sid = (name, )
            cursor.execute(dr, sid)
            conn.commit()

            return redirect(url_for('index'))

    return render_template("a_delete.html")


@app.route("/a_update", methods=('GET', 'POST'))
def a_update():

    if request.method == 'POST':

        if "name" in request.form:
            dr = "SELECT * FROM Authors WHERE name = %s"

            name = request.form['name']


            if name not in get_names():
                flash('This author does not exist')
            else:
                sid = (name, )
                cursor.execute(dr, sid)
                value = cursor.fetchall()
                return render_template("a_update.html", upd=True, data=value, aid=name)

        if "addr" in request.form:
            addr = request.form['addr']

            name = request.form['aid']

            if not name:
                flash('Name is required!')
            else:
                upd_author = ("UPDATE Authors SET "
                               "addr = %(addr)s "
                               "WHERE name = %(name)s")

                author_info = {'name': name, 'addr': addr}

                cursor.execute(upd_author, author_info)
                conn.commit()
                return redirect(url_for('index'))

    return render_template('a_update.html')


@app.route("/a_query", methods=('GET', 'POST'))
def a_query():
    if request.method == 'POST':
        if "name" in request.form:
            dr = "SELECT * FROM Authors WHERE name = %s"

            name = request.form['name']

            if name not in get_names():
                flash('This author does not exist')
            else:
                sid = (name, )
                cursor.execute(dr, sid)
                value = cursor.fetchall()
                return render_template("a_query.html", q=True, data=value)

        else: #search is not by name
            addr = request.form.get('addr')

            dr = "SELECT * FROM Authors WHERE "

            query_info = {}

            if addr:
                dr += "addr = %(addr)s "
                query_info.update({'addr': addr})

            if query_info:
                cursor.execute(dr, query_info)
                value = cursor.fetchall()
                return render_template("a_query.html", q=True, data=value)

    return render_template('a_query.html')

# _________________________________________

@app.route("/books_table")
def books_table():
    cursor.execute("select * from Books")
    value = cursor.fetchall()
    return render_template("books_table.html", data=value, name="Books")


@app.route("/b_insert", methods=('GET', 'POST'))
def b_insert():
    if request.method == 'POST':
        add_book = ("INSERT INTO Books "
                      "(title, authorName, year, genre, format, coverType) "
                      "VALUES (%(title)s, %(authorName)s, %(year)s, %(genre)s, %(format)s, %(coverType)s)")

        title = request.form['title']
        authorName = request.form['authorName']
        year = request.form['year']
        genre = request.form['genre']
        format = request.form['format']
        coverType = request.form['coverType']

        if not title:
            flash('Title is required!')
        elif not authorName:
            flash('Author is required!')
        elif title in get_titles() and authorName in get_names():
            flash('The record of this book already exists')
        elif authorName not in get_names():
            flash('The author must exist in Authors table!')
        else:
            new_book = {'title': title, 'authorName': authorName, 'year': year, 'genre': genre,
                             'format': format, 'coverType': coverType}
            cursor.execute(add_book, new_book)
            conn.commit()

            return redirect(url_for('index'))

    return render_template('b_insert.html')


@app.route("/b_delete", methods=('GET', 'POST'))
def b_delete():
    if request.method == 'POST':
        dr = "DELETE FROM Books WHERE title=%(title)s AND authorName=%(authorName)s"

        title = request.form['title']
        authorName = request.form['authorName']

        if not title:
            flash('Title is required!')
        elif not authorName:
            flash('Author is required!')
        elif title not in get_titles() or authorName not in get_names():
            flash('This book does not exist')
        else:
            key = {'title': title, 'authorName': authorName}
            cursor.execute(dr, key)
            conn.commit()

            return redirect(url_for('index'))

    return render_template("b_delete.html")


@app.route("/b_update", methods=('GET', 'POST'))
def b_update():

    if request.method == 'POST':

        if "title" in request.form or "authorName" in request.form:
            dr = "SELECT * FROM Books WHERE title=%(title)s AND authorName=%(authorName)s"

            title = request.form['title']
            authorName = request.form['authorName']

            if title not in get_titles() or authorName not in get_names():
                flash('This book does not exist')
            else:
                key = {'title': title, 'authorName': authorName}
                cursor.execute(dr, key)
                value = cursor.fetchall()
                return render_template("b_update.html", upd=True, data=value, btitle=title, bauthor=authorName)

        if "year" in request.form:
            year = request.form['year']
            genre = request.form['genre']
            format = request.form['format']
            coverType = request.form['coverType']

            title = request.form['btitle']
            authorName = request.form['bauthor']

            if not title or not authorName:
                flash('Title and author name are required!')
            else:
                upd_book = ("UPDATE Books SET "
                               "year = %(year)s, genre = %(genre)s, format = %(format)s, coverType = %(coverType)s "
                               "WHERE title = %(title)s AND authorName = %(authorName)s")

                book_info = {'year': year, 'genre': genre, 'format': format, 'coverType': coverType,
                                    'title': title, 'authorName': authorName}

                cursor.execute(upd_book, book_info)
                conn.commit()
                return redirect(url_for('index'))

    return render_template('b_update.html')


@app.route("/b_query", methods=('GET', 'POST'))
def b_query():
    if request.method == 'POST':
        title = request.form.get('title')
        authorName = request.form.get('authorName')
        year = request.form.get('year')
        genre = request.form.get('genre')
        format = request.form.get('format')
        coverType = request.form.get('coverType')

        dr = "SELECT * FROM Books WHERE "

        query_info = {}

        if title:
            dr += "title = %(title)s AND "
            query_info.update({'title': title})
        if authorName:
            dr += "authorName = %(authorName)s AND "
            query_info.update({'authorName': authorName})
        if year:
            dr += "year = %(year)s AND "
            query_info.update({'year': year})
        if genre:
            dr += "genre = %(genre)s AND "
            query_info.update({'genre': genre})
        if format:
            dr += "format = %(format)s AND "
            query_info.update({'format': format})
        if coverType:
            dr += "coverType = %(coverType)s AND "
            query_info.update({'coverType': coverType})

        if query_info:
            dr = dr[:-5] #get rid of "AND" at the end
            cursor.execute(dr, query_info)
            value = cursor.fetchall()
            return render_template("b_query.html", q=True, data=value)

    return render_template('b_query.html')

if __name__=="__main__":
    app.run(debug=True)