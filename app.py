import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
if os.path.exists("env.py"):
    import env


app = Flask(__name__)


app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")


mongo = PyMongo(app)


# events.html
@app.route("/")
@app.route("/get_events")
def get_events():
    events = list(mongo.db.events.find().sort("date", 1))
    return render_template("events.html", events=events)


@app.route("/search", methods=["GET", "POST"])
def search():
    query = request.form.get("query")
    events = list(mongo.db.events.find({"$text": {"$search": query}}))
    return render_template("events.html", events=events)


# register.html
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # check if username already exists in db
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            flash("Username already exists")
            return redirect(url_for("register"))
        register = {
            "username": request.form.get("username").lower(),
            "password": generate_password_hash(request.form.get("password"))
        }
        mongo.db.users.insert_one(register)

        # put the new user into 'session' cookie
        session["user"] = request.form.get("username").lower()
        flash("Registration Successful!")
        return redirect(url_for("profile", username=session["user"]))
    return render_template("register.html")


# login.html
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # check if username exists in db
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            # ensure hashed password matches user input
            if check_password_hash(
                    existing_user["password"], request.form.get("password")):
                session["user"] = request.form.get("username").lower()
                flash("Welcome, {}".format(
                    request.form.get("username")))
                return redirect(url_for(
                    "profile", username=session["user"]))
            else:
                # invalid password match
                flash("Incorrect Username and/or Password")
                return redirect(url_for("login"))
        else:
            # username doesn't exist
            flash("Incorrect Username and/or Password")
            return redirect(url_for("login"))
    return render_template("login.html")


# profile.html
@app.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):
    # grab the session user's username from db
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]
    if session["user"]:
        events = list(mongo.db.events.find(
            {"created_by": username}))
        return render_template(
            "profile.html", username=username, events=events)
    return redirect(url_for("login"))


# logout
@app.route("/logout")
def logout():
    # remove user from session cookie
    flash("You have been logged out")
    session.pop("user")
    return redirect(url_for("login"))


# new_event.html
@app.route("/new_event", methods=["GET", "POST"])
def new_event():
    if request.method == "POST":
        event = {
            "category_name": request.form.get("category_name"),
            "event_name": request.form.get("event_name"),
            "location": request.form.get("location"),
            "date": request.form.get("date"),
            "event_details": request.form.get("event_details"),
            "link": request.form.get("link"),
            "image": request.form.get("image"),
            "created_by": session["user"]
        }
        mongo.db.events.insert_one(event)
        flash("New Event Successfully Added")
        return redirect(url_for("get_events"))
    categories = mongo.db.categories.find().sort("category_name", 1)
    return render_template("new_event.html", categories=categories)


# edit_event.html
@app.route("/edit_event/<event_id>", methods=["GET", "POST"])
def edit_event(event_id):
    if request.method == "POST":
        submit = {"$set": {
            "category_name": request.form.get("category_name"),
            "event_name": request.form.get("event_name"),
            "location": request.form.get("location"),
            "date": request.form.get("date"),
            "event_details": request.form.get("event_details"),
            "link": request.form.get("link"),
            "image": request.form.get("image"),
            "created_by": session["user"]
        }}
        mongo.db.events.update_one({"_id": ObjectId(event_id)}, submit)
        flash("Event Successfully Updated")

    event = mongo.db.events.find_one({"_id": ObjectId(event_id)})
    categories = mongo.db.categories.find().sort("category_name", 1)
    return render_template ("edit_event.html", event=event, categories=categories)


# delete event
@app.route("/delete_event/<event_id>")
def delete_event(event_id):
    mongo.db.events.delete_one({"_id": ObjectId(event_id)})
    flash("Event Successfully Deleted!")
    return redirect(url_for("get_events"))


# categories.html
@app.route("/get_categories")
def get_categories():
    categories = list(mongo.db.categories.find().sort("category_name", 1))
    return render_template("categories.html", categories=categories)


# new_category.html
@app.route("/new_category", methods=["GET", "POST"])
def new_category():
    if request.method == "POST":
        category = {
            "category_name": request.form.get("category_name")
        }
        mongo.db.categories.insert_one(category)
        flash("New Category Added")
        return redirect(url_for("get_categories"))
    return render_template("new_category.html")


# edit_category.html
@app.route("/edit_category/<category_id>", methods=["GET", "POST"])
def edit_category(category_id):
    if request.method == "POST":
        submit = {"$set": {
            "category_name": request.form.get("category_name")
        }}
        mongo.db.categories.update_one({"_id": ObjectId(category_id)}, submit)
        flash("Category Successfully Updated")
        return redirect(url_for("get_categories"))
    category = mongo.db.categories.find_one({"_id": ObjectId(category_id)})
    return render_template("edit_category.html", category=category)


# delete_category
@app.route("/delete_category/<category_id>")
def delete_category(category_id):
    mongo.db.categories.delete_one({"_id": ObjectId(category_id)})
    flash("Category Successfully Deleted")
    return redirect(url_for("get_categories"))


# 404 errors
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=False)
