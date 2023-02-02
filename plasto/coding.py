from flask import *

app=Flask(__name__)


@app.route('/')
def login():
    return render_template("login.html")

@app.route('/login_post',methods=['post'])
def login_post():
    uname = request.form['textfield']
    passwrd = request.form['textfield2']
    return render_template("login.html")




@app.route('/approved_manufactures')
def approved_manufactures():
    return render_template("Admin/Approved Manufactures.html")


@app.route('/approved_manufactures_post',methods=['post'])
def approved_manufactures_post():
    name=request.form['textfield']
    return render_template("Admin/Approved Manufactures.html")


@app.route('/Change_password')
def Change_password():
    return render_template("Admin/ChangePassword.html")



@app.route('/Change_passwor_post',methods=['post'])
def Change_password():
    current_pass = request.form['textfield']
    new_pass = request.form['textfield2']
    confirm_pass = request.form['textfield3']
    return render_template("Admin/ChangePassword.html")


@app.route('/new_complaint')
def new_complaint():
    return render_template("Admin/NewComplaint.html")




@app.route('/new_complaint_post',methods=['post'])
def new_complaint():
    pro_name = request.form['textfield']
    return render_template("Admin/NewComplaint.html")




@app.route('/replay')
def replay():
    return render_template("Admin/Replay.html")



@app.route('/replay_post',methods=['post'])
def replay_post():
    reply = request.form['textarea']
    return render_template("Admin/Replay.html")



@app.route('/verifing_manufactiores')
def verifing_manufactiores():
    return render_template("Admin/verify_manufactures.html")



@app.route('/verifing_manufactiores_post',methods=['post'])
def verifing_manufactiores_post():
    name = request.form['textfield']
    return render_template("Admin/verify_manufactures.html")




@app.route('/view_user')
def view_user():
    return render_template("Admin/ViewUser.html")


@app.route('/view_user_post',methods=['post'])
def view_user_post():
    name = request.form['textfield']
    return render_template("Admin/ViewUser.html")


@app.route('/catagory_managment')
def catagory_managment():
    return render_template("Manufacters/CatagoryManagment.html")


@app.route('/catagory_managment_post',methods=['post'])
def catagory_managment_post():
    name = request.form['textfield']
    return render_template("Manufacters/CatagoryManagment.html")



@app.route('/delivary_rating')
def delivary_rating():
    return render_template("Manufacters/DelivaryRating.html")





@app.route('/product_managment_add')
def product_managment_add():
    return render_template("Manufacters/ProductManagment-Add.html")


@app.route('/product_managment_add-_post',methods=['post'])
def product_managment_add_post():
    pro_name = request.form['textfield']
    return render_template("Manufacters/ProductManagment-Add.html")



@app.route('/Product_Managment_edit',)
def Product_Managment_edit():
    return render_template("Manufacters/ProductManagment-Edit.html")



@app.route('/Product_Managment_edit_post',methods=['post'])
def Product_Managment_edit_post():
    img = request.files['fileField']
    pro_name = request.form['textfield']
    catgry = request.form['textfield2']
    price = request.form['textfield3']
    qty = request.form['textfield4']
    discr = request.form['textarea']
    return render_template("Manufacters/ProductManagment-Edit.html")




@app.route('/product_review')
def product_review():
    return render_template("Manufacters/ProductReview.html")




@app.route('/profile_managment')
def profile_managment():
    return render_template("Manufacters/ProfileManagment.html")


@app.route('/profile_managment_post',methods=['post'])
def profile_managment_post():
    name = request.form['textfield']
    propri_name = request.form['textfield2']
    ph = request.form['textfield3']
    ema =  request.form['textfield4']
    return render_template("Manufacters/ProfileManagment.html")





@app.route('/sign_up')
def sign_up():
    return render_template("Manufacters/Signup_N.html")



@app.route('/sign_up_post',methods=['post'])
def sign_up_post():
    usrname  = request.form['textfield']
    propri_name  = request.form['textfield2']
    ph = request.form['textfield3']
    ema  = request.form['textfield4']
    place  = request.form['textfield5']
    pst  = request.form['textfield6']
    pin  = request.form['textfield7']
    Latitude = request.form['textfield8']
    Longitude = request.form['textfield9']
    return render_template("Manufacters/Signup_N.html")



@app.route('/staff_managment')
def staff_managment():
    return render_template("Manufacters/StaffManagment-0.html")




@app.route('/staff_managment_add')
def staff_managment_add():
    return render_template("Manufacters/StaffManagment-AddNew.html")




@app.route('/staff_managment_add_post',methods=['post'])
def staff_managment_add_post():
    #syntax to get value from a check box???
    Name = request.form['textfield']
    age = request.form['textfield2']
    phone = request.form['textfield3']
    ema = request.form['textfield4']
    place = request.form['textfield5']
    pin = request.form['textfield6']
    Post = request.form['textfield7']
    city = request.form['textfield8']
    return render_template("Manufacters/StaffManagment-AddNew.html")



@app.route('/product_managment_addnew')
def product_managment_addnew():
    return render_template("Manufacters/Product managment-Add new.html")




@app.route('/product_managment_addnew_post',methods=['post'])
def product_managment_addnew_post():
    imge = request.files['fileField']
    Pname = request.form['textfield']
    Ctgry = request.form['textfield2']
    price = request.form['textfield3']
    qty = request.form['textfield4']
    description = request.form['textarea']
    return render_template("Manufacters/Product managment-Add new.html")


























app.run(debug=True)