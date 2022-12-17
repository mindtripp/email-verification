from flask_app import app
from flask import render_template,redirect,request,session,flash

# import the class from user.py
from flask_app.models.user import User

@app.route("/")
def index():
    # call the get all classmethod to get all friends
    friends = User.get_all()
    print(friends)
    return render_template("index.html", all_friends=friends)

@app.route("/users/new")
def new_page():
    return render_template("create_page.html")

@app.route('/create', methods=["POST"])
def create():
    user_info = request.form
    if User.is_valid_user(user_info):
        User.save(user_info)
        print("PASS")
        return redirect('/')
    print("FAIL")
    return redirect('/users/new')