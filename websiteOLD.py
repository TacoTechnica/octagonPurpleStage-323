#!/usr/bin/python
from flask import Flask, render_template, request, redirect
from util import reader,checker

website=Flask(__name__)

main_user = ""




@website.route("/")
def homepage():
    if main_user == "":
        return redirect("/login")
    else:
        return render_template("homepage.html",height = 400, title = 'OPS - Home',user = ", " + main_user)

##############LOGIN AND ACCOUNTS#################

@website.route( '/login/')
def login():
    return render_template("login.html",error = "")


@website.route( '/login/result', methods = ["POST"])
def result():
    user_list = reader.make_dic(reader.read_file("data/users/users.csv"))    
    rf = request.form
    user = rf["txt_user"]
    pw = rf["txt_password"]
    if user == "" or pw == "":
        return render_template("login.html",error = "Both elements must be filled!")
    elif user in user_list.keys() and user_list[user] == pw:
        main_user = user
        print main_user + " ONE"
        return redirect("/")
    else:
        return render_template("login.html",error = "Incorrect username and/or password")

@website.route( '/register/')
def register():
    return render_template("register.html",error = "")



@website.route( '/register/result/',methods = ["POST"])
def registered():
    rf = request.form
    user = rf["txt_user"]
    pw = rf["txt_password"]
    pw2 = rf["txt_password2"]
    if user == "" or pw == "" or pw2 == "":
        return render_template("register.html",error = "ALL elements must be filled!")
    elif pw != pw2:
        return render_template("register.html",error = "Passwords must match")
    elif not checker.pwformat(pw):
        return render_template("register.html",error = "Passwords must contain characters AND numbers.")
    else:

        reader.write_file("data/users/users.csv","\n" + user + "," + pw)
        return redirect("/")
    
    return render_template("register.html",error = "")




if __name__=="__main__":
    website.debug=True
    website.run(host="0.0.0.0",port=5000)
