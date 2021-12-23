#Music Played while doing this project
#https://www.youtube.com/watch?v=cGYyOY4XaFs&t=2403s&ab_channel=Rousseau
import random

import PIL.Image as Image
import io
import base64

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from flask import Flask, redirect, url_for, render_template, \
    session, flash, request


from database import account_table, gallery_account_table, mondstadt, characters, db, app, liyue, inazuma

app = Flask(__name__)


@app.route("/account-update", methods = ["POST","GET"])
def update_account_page():
    data = account_table.query.filter_by(id = get_user_id()).first()

    if request.method == "POST":
        get_email = request.form["email"]
        get_password = request.form["password"]
        get_old_password = request.form["old password"]

        if data.password != get_old_password:
            flash('Old Password is incorrect!')
            return redirect(url_for("update_account_page"))


        update_account_data(get_email,get_password)


    return render_template("updateaccountpage.html",
                           data = data)

@app.route("/forgot-password", methods = ["POST","GET"])
def forgot_pass_page():
    if request.method == "POST":
        session["code"] = random.randint(1000, 9999)
        get_email = request.form["email"]
        session["email"] = get_email
        if check_email(get_email):


            email_sender(session["code"],get_email)

            flash(f" Check your email for code", "info")
            return redirect(url_for("forgot_pass_code_page"))

        else:
            flash(f" Email not registered to any account", "info")
            return redirect(url_for("forgot_pass_page"))

    return render_template("forgotPasswordPage.html")


def check_email(email):

    user_exists = account_table.query.filter_by(email=email).first()

    if user_exists:
        return True

    return False

@app.route("/forgot-account-update", methods = ["POST","GET"])
def forgot_account_page():
    data = account_table.query.filter_by(email = session["email"]).first()

    if request.method == "POST":
        get_email = request.form["email"]
        get_password = request.form["password"]
        update_account_data(get_email,get_password)

        session.pop("email", None)
        session.pop("code", None)

        return redirect(url_for("login_page"))


    return render_template("forgotAccountPage.html",
                           data = data)

@app.route("/forgot-password-code", methods = ["POST","GET"])
def forgot_pass_code_page():


    if request.method == "POST":

        print(type(session["code"]))
        get_code = int(request.form["code"])

        if get_code == session["code"]:
            return redirect(url_for("forgot_account_page"))

        else:
            flash(f" Wrong Code", "info")

    return render_template("forgotPasswordCodePage.html")



#region pages
@app.route("/Mondstadt", methods = ["POST","GET"])
def mondstadt_page():

    if "user" not in session:
        return redirect(url_for("login_page"))

    user = mondstadt.query.order_by(mondstadt.input_id).filter_by(gallery_id = get_gallery_id()).all()
    # using tobytes data as raw for frombyte function
    input_id_list = []
    image_list = []
    comments_list = []
    region_list = []
    name_list = []
    for i in user:
        input_id_list.append(i.input_id)
        image_list.append(base64.b64encode(i.images).decode('utf-8'))
        region_list.append(i.region)
        name_list.append(i.name)
        comments_list.append(i.description)


    if request.method == "POST":
        get_input_id = request.form['delete']

        delete_mondstadt_data(get_input_id)

        return redirect(url_for("mondstadt_page"))

    return render_template("mondstadtPage.html",
                           len = len(comments_list),
                           input_id_data = input_id_list,
                           img_data = image_list,
                           region_data = region_list,
                           name_data = name_list,
                           comment_data = comments_list)

@app.route("/Liyue", methods = ["POST","GET"])
def liyue_page():

    if "user" not in session:
        return redirect(url_for("login_page"))

    user = liyue.query.order_by(liyue.input_id).filter_by(gallery_id = get_gallery_id()).all()
    # using tobytes data as raw for frombyte function
    input_id_list = []
    image_list = []
    comments_list = []
    region_list = []
    name_list = []
    for i in user:
        input_id_list.append(i.input_id)
        image_list.append(base64.b64encode(i.images).decode('utf-8'))
        region_list.append(i.region)
        name_list.append(i.name)
        comments_list.append(i.description)


    if request.method == "POST":
        get_input_id = request.form['delete']

        delete_liyue_data(get_input_id)

        return redirect(url_for("liyue_page"))

    return render_template("liyuePage.html",
                           len = len(comments_list),
                           input_id_data = input_id_list,
                           img_data = image_list,
                           region_data = region_list,
                           name_data = name_list,
                           comment_data = comments_list)

@app.route("/Inazuma", methods = ["POST","GET"])
def inazuma_page():

    if "user" not in session:
        return redirect(url_for("login_page"))

    user = inazuma.query.order_by(inazuma.input_id).filter_by(gallery_id = get_gallery_id()).all()
    # using tobytes data as raw for frombyte function
    input_id_list = []
    image_list = []
    comments_list = []
    region_list = []
    name_list = []
    for i in user:
        input_id_list.append(i.input_id)
        image_list.append(base64.b64encode(i.images).decode('utf-8'))
        region_list.append(i.region)
        name_list.append(i.name)
        comments_list.append(i.description)


    if request.method == "POST":
        get_input_id = request.form['delete']

        delete_inazuma_data(get_input_id)

        return redirect(url_for("inazuma_page"))

    return render_template("inazumaPage.html",
                           len = len(comments_list),
                           input_id_data = input_id_list,
                           img_data = image_list,
                           region_data = region_list,
                           name_data = name_list,
                           comment_data = comments_list)

#character page



@app.route("/character-gallery", methods = ["POST","GET"])
def character_gallery_page():
    if "user" not in session:
        return redirect(url_for("login_page"))

    vision_dictionary = {
        "Pyro": "red",
        "Cryo": "lightblue",
        "Geo": "yellow",
        "Anemo": "lightgreen",
        "Dendro": "darkgreen",
        "Electro": "purple",
        "Hydro": "blue"
    }


    user = characters.query.order_by(characters.input_id).\
        filter_by(gallery_id=get_gallery_id()).all()

    # using tobytes data as raw for frombyte function
    portrait_list = []
    description_list = []
    name_list = []
    region_list = []
    input_id_list = []
    color_list = []

    for i in user:
        portrait_list.append(base64.b64encode(i.portrait).decode('utf-8'))
        description_list.append(i.description)
        name_list.append(i.name)
        region_list.append(i.region)
        input_id_list.append(i.input_id)
        color_list.append(vision_dictionary[i.vision])


    if request.method == "POST":

        get_input_id = request.form['delete']
        delete_data(get_input_id)


        return redirect(url_for("character_gallery_page"))

    return render_template("characterPage.html",
                           len=len(description_list),
                           img_data=portrait_list,
                           comment_data=description_list,
                           region_data = region_list,
                           name_data=name_list,
                           input_id_data = input_id_list,
                           colors = color_list)




#login
@app.route("/", methods = ["POST","GET"])
def login_page():
    if "user" in session:
        return redirect(url_for("gallery_page"))

    if request.method == "POST":
        get_login_user = request.form["user"]
        get_login_password = request.form["psw"]
        user_found = login(get_login_user,get_login_password)

        if user_found == False :
          flash("user not found!","info")

        else:
          session["user"] = user_found.id

          return redirect(url_for("gallery_page"))



    return render_template("loginpage.html")

#logout
@app.route("/logout", methods = ["POST","GET"])
def logout():

    session.pop("user",None)
    session.pop("region", None)

    return redirect(url_for("login_page"))

@app.route("/gallery")
def gallery_page():

    if "user" not in session:
        return redirect(url_for("login_page"))

    return render_template("galleryPage.html")


#insert stuff
@app.route("/register", methods = ["POST","GET"])
def register_account_page():
    if "user"  in session:
        return redirect(url_for("gallery_page"))

    if request.method == "POST":
        get_username = request.form["username"]
        get_password = request.form["password"]
        get_fname = request.form["fname"]
        get_lname = request.form["lname"]
        get_email = request.form["email"]
        get_gender = request.form["gender"]

        user_exists = insert_account_Data(get_username,
                            get_fname,
                            get_lname,
                            get_email,
                            get_gender,
                            get_password)

        if user_exists:

            flash(f" {get_username} User Already Exists", "info")
            return redirect(url_for("register_account_page"))

        else:
            flash("User Registered", "info")
            return redirect(url_for("login_page"))

    return render_template("registerPage.html")


@app.route("/upload", methods=["POST", "GET"])
def upload_page():
    if "user" not in session:
        return redirect(url_for("login_page"))

    if request.method == "POST":
        try:

            get_file = request.files['image']

            image = Image.open(get_file)

            byteIO = io.BytesIO()
            image.save(byteIO, format='PNG', quality=95)
            get_file = byteIO.getvalue()

            get_region = request.form["region"]
            get_description = request.form["description"]
            get_name = request.form["place"]

            if get_region == "Mondstadt":

                insert_mondstadt_upload_data(get_gallery_id(),
                                         get_file,
                                         get_region,
                                         get_name,
                                         get_description)

                return redirect(url_for("gallery_page"))

            elif get_region == "Liyue":

                insert_liyue_upload_data(get_gallery_id(),
                                             get_file,
                                             get_region,
                                             get_name,
                                             get_description)

                return redirect(url_for("gallery_page"))

            elif get_region == "Inazuma":

                insert_inazuma_upload_data(get_gallery_id(),
                                         get_file,
                                         get_region,
                                         get_name,
                                         get_description)

                return redirect(url_for("gallery_page"))

        except Exception as err:
            print("Error occurred")
            print(err)
            flash(f" Please Remember to actually choose something :D", "info")

            return render_template("uploadPage.html")

    return render_template("uploadPage.html")



@app.route("/character-upload", methods = ["POST","GET"])
def charater_upload_page():
    #For color


    if "user" not in session:
        return redirect(url_for("login_page"))

    if request.method == "POST":
        try:

            get_file = request.files['image']
            get_description = request.form["description"]
            get_character_name = request.form["name"]
            get_region = request.form["region"]
            get_vision = request.form["vision"]
            image = Image.open(get_file)



            byteIO = io.BytesIO()
            image.save(byteIO, format='PNG', quality=95)
            get_file = byteIO.getvalue()

            insert_character_upload_data(get_gallery_id(),
                                         get_character_name,
                                         get_description,
                                         get_file,
                                         get_vision,
                                         get_region)



            return redirect(url_for("character_gallery_page"))

        except Exception as err:
            print("Error occurred")
            print(err)
            flash(f" Please Remember to actually choose something :D", "info")

            return render_template("CharacterUploadPage.html")

    return render_template("CharacterUploadPage.html")





#below are non website func

def update_account_data(email,password):
    user = (account_table.query.filter_by(email=email).first())
    user.email = email
    user.password = password

    db.session.commit()



#delete
def delete_data(id):

    data = characters.query.filter_by(input_id= id ).first()
    db.session.delete(data)
    db.session.commit()


def delete_mondstadt_data(id):

    data = mondstadt.query.filter_by(input_id= id ).first()
    db.session.delete(data)
    db.session.commit()

def delete_inazuma_data(id):

    data = inazuma.query.filter_by(input_id= id ).first()
    db.session.delete(data)
    db.session.commit()

def delete_liyue_data(id):

    data = liyue.query.filter_by(input_id= id ).first()
    db.session.delete(data)
    db.session.commit()



#for login
def login(username, password):


    user_exists = account_table.query.filter_by(username = username).first()

    if user_exists:

        get_user_password = user_exists.password

        if get_user_password == password:

            return user_exists


    return False

#below are insert functions
def insert_account_Data(username,fname,lname,email,gender,password):

    user = account_table(username,fname,lname,email,gender,password)



    user_exists = account_table.query.filter_by(username = username).first()

    if user_exists:

        return True

    else:
        db.session.add(user)

        db.session.commit()
        gallery_account = gallery_account_table(user.id)
        db.session.add(gallery_account)
        db.session.commit()

        return False

def insert_mondstadt_upload_data(gallery_id,file,region, name, description):

    data = mondstadt(gallery_id,
                     file,
                     region,
                     name,
                     description)

    db.session.add(data)
    db.session.commit()


def insert_liyue_upload_data(gallery_id,file,region, name, description):

    data = liyue(gallery_id,
                     file,
                     region,
                     name,
                     description)

    db.session.add(data)
    db.session.commit()

def insert_inazuma_upload_data(gallery_id,file,region, name, description):

    data = inazuma(gallery_id,
                     file,
                     region,
                     name,
                     description)


    db.session.add(data)
    db.session.commit()

def insert_character_upload_data(gallery_id,name, description,portrait,vision,region):

    data = characters(gallery_id,
                      name,
                      description,
                      portrait,
                      vision,
                      region)

    db.session.add(data)
    db.session.commit()


#get current user id
def get_user_id():

    return session["user"]

def get_gallery_id():

    user_id = session["user"]
    gallery_id = gallery_account_table.query.filter_by(account_id = user_id).first()

    return gallery_id.gallery_id




#gmail
def email_sender(code,email):

    password = ""

    mail_content = f'''Hello,
If you did not reset your password please ignore this message

Here is the code for your password recovery {code}
    
Please do make sure that you won't lose it again

Thank You '''



    sender_address = 'thisisaspam.ham@gmail.com'
    sender_pass = 'yametekudasai'
    receiver_address =  email
    #Setup the MIME
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = 'Password Recovery From Genshin Gallery.'   #The subject line
    #The body and the attachments for the mail
    message.attach(MIMEText(mail_content, 'plain'))
    #Create SMTP session for sending the mail
    session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
    session.starttls() #enable security
    session.login(sender_address, sender_pass) #login with mail_id and password
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()
    print('Mail Sent')




if __name__ == "__main__":
    app.run(debug=True)
    db.create_all()