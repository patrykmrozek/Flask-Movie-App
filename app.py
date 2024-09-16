from flask import Flask, render_template, redirect, url_for, make_response, request, session
from database import get_db, close_db, g
from flask_session import Session
from forms import RegistrationForm, LoginForm, RateForm, SearchForm, AdminMovieForm, UpdateMovieForm, AddUserForm, UpdateUserForm
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import os
from dotenv import load_dotenv

load_dotenv()
load_dotenv(".flaskenv")


app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET-KEY")
app.config["SESSION_PERMANENT"] = False 
app.config["SESSION_TYPE"] = "filesystem"
Session(app) 



@app.before_request
def load_logged_in_user():
    g.user = session.get("user_id", None)

@app.before_request
def load_logged_in_user():
    g.admin = session.get("admin", 0)



def login_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if g.user is None:
            return redirect(url_for('login', next=request.url))
        return view(*args, **kwargs)
    return wrapped_view

def admin_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        if g.admin == 0 :
            return redirect(url_for('home'))
        return view(**kwargs)
    return wrapped_view
    
app.teardown_appcontext(close_db)

methods = ["GET", "POST"]

@app.route("/", methods=methods)
def home():

    db = get_db()
    movies = db.execute(""" SELECT * FROM movies; """).fetchall()

    reviews = db.execute(""" SELECT movie_ratings.user_rating, movies.title, movie_reviews.user_review, movie_reviews.user_id, movies.poster, movies.id FROM movies JOIN movie_reviews JOIN movie_ratings
                              ON movies.id = movie_reviews.movie_id AND movie_reviews.movie_id = movie_ratings.movie_id GROUP BY movie_reviews.user_review ORDER BY movie_reviews.review_id DESC LIMIT 5 """).fetchall()
    

    return render_template("home.html", movies = movies, reviews=reviews)


@app.route("/registration", methods = ["GET", "POST"])
def registration():
    form = RegistrationForm()
    if form.validate_on_submit():
        user_id = form.user_id.data
        password = form.password.data
        password2 = form.password2.data
        pfp = form.profilepic.data
        db = get_db()
        conflict_user = db.execute(''' SELECT * FROM users
               WHERE user_id = ?''', (user_id,)).fetchone() 

        if conflict_user is not None:
            form.user_id.errors.append("User clashes with another")
        else:
            db.execute(''' INSERT INTO users (user_id, password, is_admin, pfp)
                        VALUES (?, ?, ?, ?);''', (user_id, generate_password_hash(password), 0, pfp))
                

            db.commit() 
            return redirect(url_for("login"))
    return render_template("registration.html", form=form)



@app.route("/login", methods=methods)
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user_id = form.user_id.data
        password = form.password.data
        db = get_db()

        user = db.execute(''' SELECT * FROM users
               WHERE user_id = ?''', (user_id,)).fetchone() #if only fetching a single piece of data, use fetchone, which returns one dictionary
        # if there is one (not None):
        if user is None:
            form.user_id.errors.append("No user with that username!")
            #  (encrypted, plain text)
        elif not check_password_hash(user['password'], password):
            form.password.errors.append("Incorrect password.")
        else:
            session.clear()
            session["user_id"] = user_id # puts user id into the session store so that when your user_id is in the store, you are logged in
            session["admin"] = db.execute(""" SELECT is_admin FROM users WHERE user_id = ?;""", (user_id, )).fetchone()[0]
            next_page = request.args.get("next")
            if not next_page:
                next_page = url_for('home')
            return redirect(next_page)
    return render_template("login.html", form=form)


@app.route("/logout")

@login_required
def logout():
    session.clear()
    return redirect(url_for("home"))



@app.route("/movies", methods = methods)
def movies():
    
    db = get_db()
    movies = db.execute(""" SELECT * FROM movies; """).fetchall()

    return render_template("movies.html", movies = movies)



@app.route("/movie/<int:movie_id>", methods=methods)
def movie(movie_id):
    form = RateForm()

    db = get_db()
    movie = db.execute(""" SELECT * FROM movies WHERE id = ?;""", (movie_id,)).fetchone()
    reviews = db.execute( """  SELECT * FROM movie_reviews WHERE movie_id = ?; """, (movie_id,)).fetchall()

    
    if form.validate_on_submit():
        rating = form.rating.data
        review = form.review.data
        favourite = form.favourite.data

           
        
        rating_check = db.execute(""" SELECT user_rating FROM movie_ratings WHERE user_id = ? and movie_id = ?;""", (g.user, movie_id)).fetchone()
        review_check = db.execute(""" SELECT user_review FROM movie_reviews WHERE user_id = ? and movie_id = ?;""", (g.user, movie_id)).fetchone()
        favourite_check = db.execute(""" SELECT movie_id FROM user_favourites WHERE user_id = ? and movie_id = ?;""", (g.user, movie_id)).fetchone()
        

        

        if rating_check is None:
            db.execute(""" INSERT INTO movie_ratings (user_id, movie_id, user_rating) VALUES (?, ?, ?);""", (g.user, movie_id, rating))
        else:
            db.execute(""" UPDATE movie_ratings SET user_rating = ? WHERE user_id = ? and movie_id = ?;""", (rating, g.user, movie_id))
        
        if review != "" and review_check is None:
            db.execute(""" INSERT INTO movie_reviews (user_id, movie_id, user_review) VALUES (?, ?, ?); """, (g.user, movie_id, review))
        elif review_check:
            db.execute(""" UPDATE movie_reviews SET user_review = ? WHERE user_id = ? and movie_id = ?;""", (review, g.user, movie_id))

        if favourite is True:
            if favourite_check != None:
                db.execute(""" DELETE FROM user_favourites WHERE user_id = ? AND movie_id = ? ;""", (g.user, movie_id))
            else:
                db.execute(""" INSERT INTO user_favourites (user_id, movie_id) VALUES (?, ?);""", (g.user, movie_id))



        db.commit()


    return render_template("movie.html", movie=movie, form=form, reviews=reviews)



@app.route("/account", methods = methods)

@login_required
def account():

    db = get_db()

    pfp = db.execute(""" SELECT pfp FROM users WHERE user_id = ?;""", (g.user, )).fetchone()

    ratings = db.execute(""" SELECT movies.title, movie_ratings.user_rating, movies.poster, movies.id FROM movies JOIN movie_ratings
                              ON movies.id = movie_ratings.movie_id WHERE movie_ratings.user_id = ?; """, (g.user, )).fetchall()

    reviews = db.execute(""" SELECT movies.title, movie_reviews.user_review, movies.poster FROM movies JOIN movie_reviews
                              ON movies.id = movie_reviews.movie_id WHERE movie_reviews.user_id = ?; """, (g.user, )).fetchall()
    
    favourite_movies = db.execute(""" SELECT * FROM user_favourites JOIN movies ON movies.id = user_favourites.movie_id WHERE user_favourites.user_id = ? LIMIT 6;""", (g.user,)).fetchall()
    

    return render_template("account.html", ratings=ratings, reviews=reviews, favourite_movies=favourite_movies, pfp=pfp)



@app.route("/search", methods = methods)
def search():
    form=SearchForm()
    movie_results = []
    user_results = []
    select = None

    if form.validate_on_submit():
        search = form.search.data
        sort = form.sort.data
        # sort_choices = form.sort.choices
        select = form.select.data
        # select_choices = form.select.choices

        db = get_db()

        if select == 'movies':
 
            for letterindex in range(len(search)):
                # movie_results = db.execute(""" SELECT * FROM movies WHERE SUBSTR(title, 0, ?) LIKE SUBSTR(?, 0, ?)
                #                             ORDER BY ? DESC """, (letterindex+2, search, letterindex+2, sort)).fetchall()
                movie_results = db.execute(f""" SELECT * FROM movies WHERE SUBSTR(title, 0, ?) LIKE SUBSTR(?, 0, ?)
                                            ORDER BY {sort} DESC """, (letterindex+2, search, letterindex+2)).fetchall()
                
        
        elif select == 'users':
            for letterindex in range(len(search)):
                user_results = db.execute(""" SELECT * FROM users WHERE SUBSTR(user_id, 0, ?) LIKE SUBSTR(?, 0, ?)""", (letterindex+2, search, letterindex+2)).fetchall()

            

        
        

    return render_template("search.html", form=form, movie_results=movie_results, user_results=user_results, select=select)


@app.route("/user/<user_id>", methods=methods)

@login_required
def user(user_id):

    db = get_db()

    pfp = db.execute(""" SELECT pfp FROM users WHERE user_id = ?;""", (user_id, )).fetchone()

    ratings = db.execute(""" SELECT movies.title, movie_ratings.user_rating, movies.poster, movies.id FROM movies JOIN movie_ratings
                              ON movies.id = movie_ratings.movie_id WHERE movie_ratings.user_id = ?; """, (user_id, )).fetchall()

    reviews = db.execute(""" SELECT movies.title, movie_reviews.user_review, movies.poster FROM movies JOIN movie_reviews
                              ON movies.id = movie_reviews.movie_id WHERE movie_reviews.user_id = ?; """, (user_id, )).fetchall()
    
    favourite_movies = db.execute(""" SELECT * FROM user_favourites JOIN movies ON movies.id = user_favourites.movie_id WHERE user_favourites.user_id = ? LIMIT 6;""", (user_id,)).fetchall()
    
    if user_id == g.user:
        return redirect(url_for("account"))

    return render_template("user.html", ratings=ratings, reviews=reviews, user_id=user_id, favourite_movies=favourite_movies, pfp=pfp)



@app.route("/admin", methods=methods)

@admin_required
def admin():
    form = AdminMovieForm()

    if form.validate_on_submit():
        title = form.title.data
        score = form.score.data
        year = form.year.data
        description = form.description.data
        poster = form.poster.data
        director = form.director.data


        db = get_db()

        db.execute("""INSERT INTO movies (title, year, score, director, poster, description) VALUES (?, ?, ?, ?, ?, ?)""", (title, year, score, director, poster, description))
            

        db.commit()
        return redirect(url_for("movies"))
    return render_template("admin.html", form=form)


@app.route('/update_movie/<int:movie_id>', methods=methods)

@admin_required
def update_movie(movie_id):
    form = UpdateMovieForm()

    db = get_db()


    movie_data = db.execute(""" SELECT title, year, score, director, poster, description FROM movies WHERE id = ? """, (movie_id, )).fetchall()[0]

    form = UpdateMovieForm(title=movie_data[0], year=movie_data[1], score=movie_data[2], director=movie_data[3], poster=movie_data[4], description=movie_data[5])
    
    if form.validate_on_submit():
        title = form.title.data
        score = form.score.data
        year = form.year.data
        description = form.description.data
        poster = form.poster.data
        director = form.director.data

        db.execute(""" UPDATE movies SET title=?, year=?, score=?, director=?, poster=?, description=? WHERE id=?;""", (title, year, score, director, poster, description, movie_id))

        db.commit()
        return redirect(url_for("movies"))
    
    return render_template("update_movie.html", form=form)


@app.route("/delete_movie/<int:movie_id>", methods=methods)
@admin_required
def delete_movie(movie_id):
    db = get_db()

    db.execute("""DELETE FROM movies WHERE id = ?;""", (movie_id, ))

    db.commit()

    return redirect(url_for("movies"))

        

@app.route("/add_user", methods=methods)

@admin_required
def add_user():
    form = AddUserForm()
    db = get_db()
    

    if form.validate_on_submit():
        user_id = form.user_id.data
        password = generate_password_hash(form.password.data)
        is_admin = form.admin.data
        pfp = form.profilepic.data

        print(is_admin)

        conflict_user = db.execute(''' SELECT * FROM users
               WHERE user_id = ?''', (user_id,)).fetchone() 

        if conflict_user is not None:
            form.user_id.errors.append("User clashes with another")
        else:
            db.execute("""INSERT INTO users (user_id, password, is_admin, pfp) VALUES (?, ?, ?, ?)""", (user_id, password, is_admin, pfp))

                
            

            db.commit()
            return redirect(url_for("home"))
    return render_template("add_user.html", form=form)

    



@app.route('/update_user/<user_id>', methods=methods)

@admin_required
def update_user(user_id):
    form = UpdateUserForm()

    db = get_db()
    
    if form.validate_on_submit():
        admin = form.admin.data

        db.execute(""" UPDATE users SET is_admin=? WHERE user_id = ?;""", (admin, user_id))

        db.commit()
        print("hello")
        return redirect(url_for("home"))
    
    return render_template("update_user.html", form=form, user_id=user_id)