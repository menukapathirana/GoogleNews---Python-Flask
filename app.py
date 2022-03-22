import atexit
import csv
from datetime import datetime
import os
import signal
import time
from functools import wraps
from threading import Thread

import MySQLdb
from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, render_template, flash, redirect, url_for, session,logging,request


from data import Articles
from latest import ltr, findltr
from flask_mysqldb import MySQL
from wtforms import Form,StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
import json,jsonify

import WebScrapper.Scraper as sc

app = Flask(__name__)


def print_date_time():
    # print(time.strftime("%A, %d. %B %Y %I:%M:%S %p"))
    print("CSV Starting Now")
    scraper = sc.scrape()

scheduler = BackgroundScheduler()
# scheduler.add_job(func=print_date_time, trigger="interval", minutes=1)
mydate = datetime.today().strftime('%Y-%m-%d')
scheduler.add_job(func=print_date_time, run_date= mydate+' 15:54:00')
scheduler.start()

# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())



# Config MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'myflaskapp'
app.config['MYSQL_CURSORCLASS'] ='DictCursor'

#initialize MYSQL
mysql = MySQL(app)


Articles=Articles()

getvaljson=""

ltrNews = ltr()

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/articles')
def articles():
    articles=Articles
    print(articles)
    return render_template('articles.html',articles=Articles)

@app.route('/article/<string:id>/')
def article(id):
    return render_template('article.html',id=id)


class JSShape(object):
    jsonNewsOut = ''
    jval=''
    alljson=''


#Register form class
class RegisterForm(Form):
    name = StringField('Name',[validators.Length(min=1,max=50)])
    username = StringField('Username',[validators.Length(min=1,max=25)])
    email = StringField('Email',[validators.Length(min=6,max=50)])
    password = PasswordField('Password',[
        validators.DataRequired(),
        validators.EqualTo('confirm',message='Password do not match')
    ])
    confirm = PasswordField('Confirm Password')


#User Register
@app.route('/register', methods=['GET' , 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))

        #Create cursor
        cur = mysql.connection.cursor()
        # Execute query
        cur.execute("INSERT INTO users(name, email, username, password) VALUES(%s, %s, %s, %s)",(name, email, username, password))
        #Commit to DB
        mysql.connection.commit()
        #Close Connection
        cur.close()

        flash('You are now registered','succuss')
        return redirect(url_for('preferences',username=username))
    return render_template('register.html',form=form)




#User Login
@app.route('/login', methods= ['GET','POST'])
def login():
    if request.method == 'POST':
        #Get Form Fields
        username = request.form['username']
        password_candidate = request.form['password']

        #Create cursor
        cur = mysql.connection.cursor()

        #Get user by username
        result = cur.execute("SELECT * FROM users WHERE username = %s",[username])

        if result > 0:
            #Get stored data
            data = cur.fetchone()
            password = data['password']

            #Compare passwords
            if sha256_crypt.verify(password_candidate,password):
                #Passed
                session['logged_in'] = True
                session['username'] = username
                flash('You are now logged in','success')
                return redirect(url_for('index'))
            else:
                error = 'Invalid login'
                return render_template('login.html', error=error)
            #Close connection
            cur.close()
        else:
            error = 'Username not found'
            return render_template('login.html',error=error)
    return render_template('login.html')

# Check if user logged in
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login', 'danger')
            return redirect(url_for('login'))
    return wrap

#Logout
@app.route('/logout')
def logout():
    session.clear()
    flash('You are not log out','success')
    return redirect(url_for('login'))

#UserProfile
@app.route('/user')
@is_logged_in
def user():
    # Create cursor
    cur = mysql.connection.cursor()


    cur.execute("select DISTINCT r.commentLike, u.news_ID, u.news_title from user_history u LEFT JOIN rating r on r.username=u.username WHERE u.username= %s", [session['username']])
    urhistory = cur.fetchall()




    # Get articles
    # result = cur.execute("SELECT * FROM articles")
    # Show articles only from the user logged in
    result = cur.execute("SELECT * FROM users WHERE username = %s", [session['username']])
    userdetails = cur.fetchall()

    if result > 0:
        return render_template('user.html', userdetails=userdetails, urhistory=urhistory)
    else:
        msg = 'Not Found'
        return render_template('user.html', msg=msg)
    # Close connection
    cur.close()


#Latest News
@app.route('/latest')
@is_logged_in
def latest():
    return render_template('latestnews.html',latest=ltrNews)

#LatestNewsItem
@app.route('/latestnewsitem/<string:id>/', methods=['GET' , 'POST'])
@is_logged_in
def latestnewitem(id):
    val=findltr(id)

    cur = mysql.connection.cursor()
    result = cur.execute("SELECT username,newsid,comment,COUNT(commentLike) as commentLike,COUNT(commentLove) as commentLove ,COUNT(comment) as commentc FROM rating  WHERE newsid=%s",'1')
    ratingdetails = cur.fetchall();
    if result > 0:
        for row in ratingdetails:
            print(row)
            return render_template('latestnewsitem.html', newsitem=val, ratingdetails=row)
    else:
        msg = 'Not Found'
        return render_template('latestnewsitem.html', msg=msg)
    # Close connection
    cur.close()
    # return render_template('newsitem.html', newsitem=val)


@app.route('/dashboard')
@is_logged_in
def dashboard():
    import numpy as np
    import pandas as pd
    from pandas import DataFrame
    import MySQLdb
    import os
    import json
    from datetime import datetime
    import csv
    from sklearn import neighbors
    from sklearn.neighbors import NearestNeighbors
    from scipy.sparse import csr_matrix
    from fuzzywuzzy import fuzz

    ##define functions
    def fuzzy_matching(mapper, fav_movie, verbose=True):
        match_tuple = []
        for title, idx in mapper.items():
            ratio = fuzz.ratio(title.lower(), fav_movie.lower())
            if ratio >= 60:
                match_tuple.append((title, idx, ratio))
        # sort
        match_tuple = sorted(match_tuple, key=lambda x: x[2])[::-1]
        if not match_tuple:
            print('Oops! No match is found')
            return
        if verbose:
            print('Found possible matches in our database: {0}\n'.format([x[0] for x in match_tuple]))
        return match_tuple[0][1]

    def make_recommendation(model_knn, data, mapper, fav_movie, n_recommendations):
        # fit
        # print(data)
        model_knn.fit(data)
        print('You have input news:', fav_movie)
        idx = fuzzy_matching(mapper, fav_movie, verbose=True)
        print(idx)
        if (idx == None):
            print("No Recommendations")  ##Replace by content based model
        else:
            print('Recommendation system start to make inference')
            print('......\n')
            distances, indices = model_knn.kneighbors(data[idx], n_neighbors=n_recommendations + 1)
            raw_recommends = \
                sorted(list(zip(indices.squeeze().tolist(), distances.squeeze().tolist())), key=lambda x: x[1])[:0:-1]
            reverse_mapper = {v: k for k, v in mapper.items()}
            print('Recommendations for {}:'.format(fav_movie))
            with open('my_csv.csv', 'a') as f:
                for i, (idx, dist) in enumerate(raw_recommends):
                    try:
                        recResults = df.loc[df['Title'] == reverse_mapper[idx]]
                    except KeyError:
                        print('Can not find "Title"')
                    recResults.to_csv(f, index=False, header=False)
            with open('my_csv.csv') as file:
                # reads = csv.reader(file)
                reader = csv.DictReader(file, fieldnames=(
                "SNO", "ID", "Title", "Topic", "Section", "Timestamp", "RSS", "Link", "Image",	"Description", "JsonDict",	"Source",
 "Rating"))
                out = json.dumps([row for row in reader])
                # print(out)

                ##FinalResult for Colloborative filtering
            os.remove('my_csv.csv')
            return out

    ##Read user info from the db for the user
    userId =  [session['username']];  ##get logged in user id
    conn = MySQLdb.connect(host='localhost', user='root', passwd='')
    cursor = conn.cursor()
    cursor.execute('use myflaskapp')
    cursor.execute("select first_login from users where username= %s", userId)
    result = cursor.fetchone()[0]
    my_path = os.path.abspath(os.path.dirname(__file__))
    path = os.path.join(my_path, "Scrape_Data.csv")

    df = pd.read_csv(path)  ##Change the path

    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_colwidth', -1)

    ##FirstUserLogin then Content Based Model
    if (result == 'Y'):
        print(result)
        cursor.execute("select preferences from preferences where username=%s", userId)
        result = cursor.fetchone()[0]
        print(result)
        noOfPreferences = result.split(",")
        print("Number of Preferences:" + str(len(noOfPreferences)))

        if (len(noOfPreferences) > 1):
            for y in noOfPreferences:
                with open('dictionarycsv.csv', 'a') as f:
                    dictionary = df.loc[df['Topic'] == y]
                    writetocsv = dictionary.head(3)
                    # print(writetocsv)
                    writetocsv.to_csv(f, index=False, header=False)
        else:
            dictionary = df.loc[df['Topic'] == noOfPreferences[0]]
            writetocsv = dictionary.head(3)
            # print(f)
            writetocsv.to_csv("dictionarycsv.csv", index=False, header=False)

        ##JSON FORMAT

        with open('dictionarycsv.csv') as infile:
            # read = csv.reader(infile)
            reader = csv.DictReader(infile, fieldnames=(
            "SNO", "ID", "Title", "Topic", "Section", "Timestamp", "RSS", "Link", "Image",	"Description", "JsonDict",	"Source",
 "Rating"))
            out = json.dumps([row for row in reader])
            # print(out) ##FinalResult for Content Based
        os.remove('dictionarycsv.csv')

    else:
        ##Collaborative Item based knn filtering
        ##Change the path
        path2 = os.path.join(my_path, "Scrape_Data_Lite.csv")
        df_matrix = pd.read_csv(path2)
        news_user_mat = df.pivot(index='ID', columns='Topic', values='Rating').fillna(0)
        news_to_idx = {
            news: i for i, news in
            enumerate(list(df_matrix.set_index('ID').loc[news_user_mat.index].Title))
        }
        news_user_mat_sparse = csr_matrix(news_user_mat.values)
        model_knn = NearestNeighbors(metric='euclidean', algorithm='auto', n_neighbors=10, n_jobs=-1)
        model_knn.fit(news_user_mat_sparse)
        cursor.execute('use myflaskapp')
        cursor.execute("select news_title from user_history where username=%s order by id desc ",userId)

        result = cursor.fetchone()
        print(result)
        if (result == None):
            print("in none")
            my_favorite = 'Drug prices must be revealed in TV ads under new Trump rule'
        else:
            print("in else")
            my_favorite = result[0]
        # Taman
        out = make_recommendation(model_knn=model_knn, data=news_user_mat_sparse, fav_movie=my_favorite,
                                  mapper=news_to_idx,
                                  n_recommendations=5)
        # print(out)
    # global  jsonNewsOut
    if out is not None:
        JSShape.jsonNewsOut = out
        print(out)
        d = json.loads(out)

        # get headers
        print('helll json')
        json_data_list = [];
        for jscontent in d:
            if jscontent['Topic'] not in json_data_list:
                json_data_list.append(jscontent['Topic']);
                jheader = json.dumps(json_data_list)
                yjval = json.loads(jheader)
        print(json.dumps(json_data_list));



        # Show all news
        with open(path,'r', encoding="utf8") as infile:
            # read = csv.reader(infile)
            reader = csv.DictReader(infile, fieldnames=(
                "SNO", "ID", "Title", "Topic", "Section", "Timestamp", "RSS", "Link", "Image", "Description",
                "JsonDict", "Source",
                "Rating"))
            next(reader)
            jsonout = json.dumps([row for row in reader])

            if jsonout is not None:
                JSShape.alljson = json.loads(jsonout)

                json_data_all = [];
                for jscontent in JSShape.alljson:
                    if jscontent['Topic'] not in json_data_all:
                        json_data_all.append(jscontent['Topic']);
                        jheaderall = json.dumps(json_data_all)
                        jheadall = json.loads(jheaderall)
                print(json.dumps(json_data_all));

        return render_template('dashboard.html', jsovalu=d, jsoheader=yjval,latest=ltrNews, allnews=JSShape.alljson, allheader=jheadall)

    return render_template('dashboard.html')





@app.route('/background_feedbackYes', methods=['GET', 'POST'])
def background_feedbackYes():
    try:
        userId = [session['username']];

        fdyes = request.args.get('feedbackYes', 0, type=str)

        # Create cursor
        cur = mysql.connection.cursor()

        cur.execute("SELECT first_login FROM users where username=%s", userId)
        result = cur.fetchone()
        print(result)
        if (result == None):
            print("none")
        else:
            RknType = result['first_login']
            if RknType == 'Y':
                dbRkType='content-based'
            else:
                dbRkType='collaborative-based'



        cur.execute("INSERT INTO feedback(username,feedback,recontype) VALUES(%s, %s, %s)",
                    (session['username'], fdyes, dbRkType))
        mysql.connection.commit()

        print(fdyes)
    except Exception as e:
        return str(e)
    return 'hi'



@app.route('/background_feedbackNo', methods=['GET', 'POST'])
def background_feedbackNo():
    try:
        userId = [session['username']];

        fdNo = request.args.get('feedbackNo', 0, type=str)

        # Create cursor
        cur = mysql.connection.cursor()

        cur.execute("SELECT first_login FROM users where username=%s", userId)
        result = cur.fetchone()
        print(result)
        if (result == None):
            print("none")
        else:
            RknType = result['first_login']
            if RknType == 'Y':
                dbRkType = 'content-based'
            else:
                dbRkType = 'collaborative-based'

        cur.execute("INSERT INTO feedback(username,feedback,recontype) VALUES(%s, %s, %s)",
                    (session['username'], fdNo, dbRkType))
        mysql.connection.commit()

        print(fdNo)
    except Exception as e:
        return str(e)
    return 'hi'




@app.route('/background_like', methods=['GET', 'POST'])
def background_like():
    try:
        like = request.args.get('proglang', 0, type=str)
        title = request.args.get('nTitle', 0, type=str)
        id = request.args.get('nID', 0, type=str)

        userId = [session['username']];

        # Create cursor
        cur = mysql.connection.cursor()
        cur.execute("SELECT id,first_login FROM users WHERE username=%s ", userId)
        result = cur.fetchall()

        for val in result:
            print(val['first_login'])

            if val['first_login'] == 'Y':
                print('First Login')
                cur.execute("UPDATE users SET first_login=%s WHERE username=%s",('N', userId))
                mysql.connection.commit()

                restultHistory = cur.execute("SELECT * FROM user_history WHERE username = %s AND news_ID = %s",
                                             (userId, id))
                if restultHistory > 0:
                    print('Exits')
                else:
                    cur.execute("INSERT INTO user_history(user_ID,username,news_ID,news_title) VALUES(%s, %s, %s, %s)",
                                (val['id'], session['username'], id, title))
                    mysql.connection.commit()

                restultLike = cur.execute("SELECT * FROM rating WHERE username = %s AND newsid = %s", (userId, id))
                cmtLike = cur.fetchall()

                if restultLike > 0:
                    for vaLike in cmtLike:
                        if vaLike['newsid'] == id and vaLike['commentLike'] == '0':
                            cur.execute("UPDATE rating SET commentLike=%s WHERE username=%s AND newsid=%s",
                                        (like, userId, id))
                        #     mysql.connection.commit()
                        # else:
                        #     cur.execute(
                        #         "INSERT INTO rating(commentLike,newsid,username) VALUES(%s, %s, %s)",
                        #         (like, id, userId))
                        #     mysql.connection.commit()
                else:
                    cur.execute(
                        "INSERT INTO rating(commentLike,newsid,username) VALUES(%s, %s, %s)",
                        (like, id, userId))
                    mysql.connection.commit()
        else:
            restultHistory= cur.execute("SELECT * FROM user_history WHERE username = %s AND news_ID = %s", (userId, id))

            if restultHistory > 0:
                print('Exits')
            else:
                cur.execute("INSERT INTO user_history(user_ID,username,news_ID,news_title) VALUES(%s, %s, %s, %s)",
                            (val['id'], session['username'], id, title))
                mysql.connection.commit()


            restultLike = cur.execute("SELECT * FROM rating WHERE username = %s AND newsid = %s", (userId, id))
            cmtLike = cur.fetchall()

            if restultLike > 0:
                for vaLike in cmtLike:
                    if vaLike['newsid'] == id and vaLike['commentLike'] == '0':
                        cur.execute("UPDATE rating SET commentLike=%s WHERE username=%s AND newsid=%s",
                                    (like, userId, id))
                    #     mysql.connection.commit()
                    # else:
                    #     cur.execute(
                    #         "INSERT INTO rating(commentLike,newsid,username) VALUES(%s, %s, %s)",
                    #         (like, id, userId))
                    #     mysql.connection.commit()
            else:
                cur.execute(
                    "INSERT INTO rating(commentLike,newsid,username) VALUES(%s, %s, %s)",
                    (like, id, userId))
                mysql.connection.commit()



        # Close Connection
        cur.close()


        print(id)

    except Exception as e:
        return str(e)
    return 'hi'


@app.route('/background_dislike', methods=['GET', 'POST'])
def background_dislike():
    try:
        dislike = request.args.get('proglang', 0, type=str)
        id = request.args.get('nID', 0, type=str)

        userId = [session['username']];
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM rating WHERE commentLike = %s AND username=%s AND newsid=%s", ('1', userId, id))
        mysql.connection.commit()
    except Exception as e:
        return str(e)
    return 'hi'


# @app.route('/background_love', methods=['GET', 'POST'])
# def background_love():
#     try:
#         lang = request.args.get('proglang', 0, type=str)
#         title = request.args.get('nTitle', 0, type=str)
#         id = request.args.get('nID', 0, type=str)
#         print(lang)
#
#     except Exception as e:
#         return str(e)
#     return 'hi'
#
#
# @app.route('/background_hate', methods=['GET', 'POST'])
# def background_hate():
#     try:
#         lang = request.args.get('proglang', 0, type=str)
#         print(lang)
#
#     except Exception as e:
#         return str(e)
#     return 'hi'






#NewsItem
@app.route('/newsitem/<string:id>/', methods=['GET' , 'POST'])
@is_logged_in
def newitem(id):

    # Make empty for view all news
    JSShape.jval = ''

    # ConJsonOut = json.dumps(jsonNewsOut)
    if JSShape.jsonNewsOut:
        yjval = json.loads(JSShape.jsonNewsOut)
        for x in yjval:
            if x['ID'] == id:
                JSShape.jval = x
                break

        if JSShape.jval == '':
            dpJson = json.dumps(JSShape.alljson)
            Allval = json.loads(dpJson)
            for y in Allval:
                if y['ID'] == id:
                    JSShape.jval = y
                    break

    userId = [session['username']];

    cur = mysql.connection.cursor()

    exitval = cur.execute("SELECT username, commentLike FROM rating  WHERE username = %s AND newsid = %s", (userId, id))

    if not exitval:
        stats='false'
    else:
        stats='true'





    # result = cur.execute("SELECT username,newsid,comment,COUNT(commentLike) as commentLike,COUNT(commentLove) as commentLove ,COUNT(comment) as commentc FROM rating  WHERE newsid=%s",[id])
    result = cur.execute(
        "SELECT username,newsid,comment,COUNT(commentLike) as commentLike FROM rating  WHERE newsid=%s",
        [id])
    if not result:
        msg = 'Not Found'
        return render_template('newsitem.html', msg=msg)
    else:
        ratingdetails = cur.fetchone();
        return render_template('newsitem.html', newsitem=JSShape.jval,latest=ltrNews, ratingdetails=ratingdetails, stats=stats)


    # if result > 0:
    #     ratingdetails = cur.fetchall();
    #     for row in ratingdetails:
    #         print(row)
    #     return render_template('newsitem.html', newsitem=jval, ratingdetails=row )
    # else:
    #     msg = 'Not Found'
    #     return render_template('newsitem.html', msg=msg)
    # Close connection
    cur.close()

    # return render_template('newsitem.html', newsitem=val)





#Preferences
@app.route('/preferences', methods= ['GET','POST'])
def preferences():
    if request.method == 'POST':
       # print(request.form.getlist('hello'))

        values = request.form.getlist('hello')
        str1 = ','.join(values)
        print(str1)
        # Create cursor
        cur = mysql.connection.cursor()
        # Execute query
        #start from menuka
        keys = request.args.get('username')

        #Get the user id to insert in to preferences
        result = cur.execute("SELECT id FROM users  WHERE username=%s",[keys])
        if result>0:
            data=cur.fetchone()
            userid= data['id']



        cur.execute('''INSERT INTO preferences (username, preferences, user_id) VALUES (%s, %s, %s)''', (keys, str1, userid))
        # Commit to DB
        mysql.connection.commit()
        # Close Connection
        cur.close()

        flash('You are now registered', 'succuss')
        return redirect(url_for('login'))
    return render_template('preferences.html')





#UpdatePreferences
@app.route('/updatepreferences', methods= ['GET','POST'])
def updatepreferences():
    if request.method == 'POST':
       # print(request.form.getlist('hello'))

        # values = request.form.getlist('hello')
        # str1 = ','.join(values)
        # print(str1)
        # # Create cursor
        # cur = mysql.connection.cursor()
        # # Execute query
        # #start from menuka
        # keys = request.args.get('username')
        #
        # #Get the user id to insert in to preferences
        # result = cur.execute("SELECT id FROM users  WHERE username=%s",[keys])
        # if result>0:
        #     data=cur.fetchone()
        #     userid= data['id']
        #
        #
        #
        # cur.execute('''INSERT INTO preferences (username, preferences, user_id) VALUES (%s, %s, %s)''', (keys, str1, userid))
        # # Commit to DB
        # mysql.connection.commit()
        # # Close Connection
        # cur.close()
        #
        # flash('You are now registered', 'succuss')


        return redirect(url_for('user'))

    cur = mysql.connection.cursor()

    cur.execute(
        "SELECT preferences FROM preferences WHERE username = %s", [session['username']])
    upprefer = cur.fetchone()

    # newuprefer = upprefer['preferences'].split(',')

    return render_template('updatepreferences.html',upprefer=upprefer)





app.secret_key='secret123'
if __name__ == '__main__':
    app.run(debug=True)
