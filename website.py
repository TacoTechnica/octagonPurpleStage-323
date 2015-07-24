#!/usr/bin/python
from flask import Flask, render_template, request, redirect, session
from util import reader,checker

website=Flask(__name__)




@website.route("/")
def homepage():
    if not 'username' in session:
        main_user = ""
        return redirect("login/")
    else:
        return render_template("home.html",height = 400, title = 'OPS - Home',username = ", " + session['username'],session = session)

##############LOGIN AND ACCOUNTS#################

@website.route( '/login/')
def login():
    if not 'username' in session:
        return render_template("login.html",error = "",session = session)
    else:
        return redirect("/")


@website.route( '/logout/')
def logout():
    if 'username' in session:
        session.pop('username', None)
    main_user = ""
    return redirect("/")


@website.route( '/login/result', methods = ["POST"])
def result():
    user_list = reader.make_dic(reader.read_file("data/users/users.csv"))
    rf = request.form
    user = rf["txt_user"]
    pw = rf["txt_password"]
    if user == "" or pw == "":
        return render_template("login.html",error = "Both elements must be filled!")
    elif user in user_list.keys() and user_list[user] == pw:
        session['username'] = user
        main_user = user
        return redirect("/")
    else:
        return render_template("login.html",error = "Incorrect username and/or password",session = session)

@website.route( '/register/')
def register():
    return render_template("register.html",error = "",session = session)



@website.route( '/register/result/',methods = ["POST"])
def registered():
    rf = request.form
    user = rf["txt_user"]
    pw = rf["txt_password"]
    pw2 = rf["txt_password2"]
    if user == "" or pw == "" or pw2 == "":
        return render_template("register.html",error = "ALL elements must be filled!",session = session)
    elif pw != pw2:
        return render_template("register.html",error = "Passwords must match",session = session)
    elif not checker.pwformat(pw):
        return render_template("register.html",error = "Passwords must contain characters AND numbers.",session = session)
    else:

        reader.write_file("data/users/users.csv",user + "," + pw + "\n")
        return redirect("/")
    
    return render_template("register.html",error = "",session = session)

#############################################END OF LOGIN#########

##################USER STUFF######################################
@website.route( '/account/<usr>')
def account(usr):
    user_list = reader.make_dic(reader.read_file("data/users/users.csv"))
    if not usr in user_list.keys():
        return render_template("error.html",error = "The username you have provided does not exist.")
    return render_template("account.html",user = usr,user_list = user_list)


if __name__=="__main__":
    
    website.secret_key ="""@t/"Iq^7y5cV>`\'<Rlv"""
    website.config['SESSION_TYPE'] = 'filesystem'
    #sess = Session()
    #sess.init_app(website)
    website.debug=True
    website.run(host="0.0.0.0",port=5000)
