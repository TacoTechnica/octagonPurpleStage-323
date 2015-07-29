#!/usr/bin/python
from flask import Flask, render_template, request, redirect, session
from util import reader,checker

website=Flask(__name__)




@website.route("/")
def homepage():
    if not 'username' in session:
        main_user = ""
        return redirect("/login/")
    else:
        return redirect("/tags")


@website.route("/tags/")
def tag_list():
    post_dic = reader.make_postdic("data/posts/posts.csv")
    tag_list = reader.make_taglist(post_dic)
    return render_template("tags.html",tags = tag_list)
    
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
    user_list = reader.make_dic(reader.read_file("data/users/user_auth.csv"))
    #print "BEFORE: " + str(user_list)
    #user_list = checker.reformat(user_list)
    #print "AFTER: " + str(user_list)
    rf = request.form
    user = rf["txt_user"]
    pw = rf["txt_password"]
    if user == "" or pw == "":
        return render_template("login.html",error = "Both elements must be filled!")
    elif user in user_list.keys() and user_list[user][0] == pw:
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
    user_list = reader.make_dic(reader.read_file("data/users/user_auth.csv"))
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
    elif user in user_list.keys():
        return render_template("register.html",error = "Username already exists.",session = session)
    else:
        reader.write_file("data/users/user_auth.csv",user + "," + pw +  "," + "..static/img/default.png" + "\n")
        return redirect("/")
    
    return render_template("register.html",error = "",session = session)

#############################################end of LOGIN#########

##################USER STUFF######################################
@website.route( '/account/<usr>')
def account(usr):
    user_list = reader.make_dic(reader.read_file("data/users/user_auth.csv"))
    if not usr in user_list.keys():
        return render_template("error.html",error = "The username you have provided does not exist.")
    return render_template("account.html",user = usr,user_list = user_list)

@website.route('/account/change_profile_img',methods = ["POST"])
def account_change_profile_img():
    directory = "data/users/user_auth.csv"
    url = request.form["image"]
    text = reader.read_file(directory)
    index = text[( text.find(session['username']) ):].find("\n")
    print "TEXT AFTER USERNAME: " + str(text[( text.find(session['username']) ):]) #works
    print "TEXT UNTIL NEWLINE: " + str(text[( text.find(session['username']) ):index]) #works
    i = 0
    while(text[index - i] != ","): #From the end of the user line, it goes down until it finds a comma.
        i+=1
    print "TEXT OF IMAGE: " + str(text[index-i:index])
    text = text[:(index-i)] + "," + url + text[(index):]
    reader.replace_file(directory,text)
    return redirect("/")
##################end of USER STUFF###############################
@website.route('/about/')
def about():
    return render_template("about.html")


###################POSTING AND REPLYING#############################
@website.route( '/post/')
def post():
    if not 'username' in session:
        main_user = ""
        return redirect("login/")
    else:
        post_dic = reader.make_postdic("data/posts/posts.csv")
        #post_dic = checker.reformat(post_dic)
        return render_template("post.html",dic = post_dic,tags = reader.get_tags(post_dic),message = "All Posts")

@website.route( '/post/post',methods = ["POST"])
def post_content():
    post_dir = "data/posts/posts.csv"
    rf = request.form
    reader.write_file(post_dir,rf["title"] + "<,>"+ session["username"] + "<,>" + str(rf["tags"].split(",")) + "<,>" + rf["content"] + "<,>" + rf["images"] + "," + "<,>" + "\<end>\n")
    return redirect("/post")


@website.route('/post/tag/<tag>')
def post_by_tag(tag):
    post_dic = reader.make_postdic("data/posts/posts.csv")
    tags = reader.get_post_by_tag(post_dic,tag)
    
    #print "TAGS: " + str(tags)
    post_dic_tags = []
    for i in tags:
        #print "POST_TAGS: " + str(tags[i])
        post_dic_tags.append(post_dic[i])
    return render_template("post.html",dic = post_dic_tags,tags = reader.get_tags(post_dic_tags),message = "Posts by tag: " + tag)


@website.route( '/post/user/<usr>')
def post_by_user(usr):
    user_list = reader.make_dic(reader.read_file("data/users/user_auth.csv"))
    if not usr in user_list.keys():
        return render_template("error.html",error = "The username you have provided does not exist.")

    post_dic = reader.make_postdic("data/posts/posts.csv")
    post_dic_user = reader.get_post_by_user(post_dic,usr)

    return render_template("post.html",dic = post_dic_user,tags = reader.get_tags(post_dic_user),message = "Posts by " + usr)

@website.route('/post/reply/<index>', methods = ["POST"])
def post_reply(index):
    directory = "data/posts/posts.csv"
    reply = request.form["reply"]
    #post_dic = reader.make_postdic("data/posts/posts.csv")
    text = reader.read_file(directory)


    i = 1
    count = 0
    
    while ((count <= int(index)) and (i < len(text))):
        if reader.string_at(i,"\\<end>\n",text):
            count+=1
            
        i+=1
    #if count != 0:
    #    print "WAHT THAS IASJDSOJHAMNIK"
    #    i-=1



    i -= 1 #8 is the length of string "/<end>\n"
    text = text[:i] + reply + "{,}" + session["username"] + "{{,}}" + text[i:]
    reader.replace_file(directory,text)
    return redirect("/post")
###################end of POSTING AND REPLYING#############################



##########ERROR SITE #######################
@website.route('/<error>')
def error_page(error):
    return render_template("error.html",error =  error + " does not exist on the site.")

if __name__=="__main__":
    
    website.secret_key ="""@t/"Iq^7y5cV>`\'<Rlv"""
    website.config['SESSION_TYPE'] = 'filesystem'
    #sess = Session()
    #sess.init_app(website)
    website.debug=True
    website.run(host="0.0.0.0",port=5000)
    
    #session["user_auth"] = reader.make_dic(reader.read_file("data/users/user_auth.csv"))
    #print "THING: " + str(session["user_auth"])
