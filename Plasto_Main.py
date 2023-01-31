from flask import *
from DBConnection import Db
app = Flask(__name__)
app.secret_key = "ghhjggm"





@app.route('/')
def login():
    return render_template("index.html")



@app.route('/login_post',methods=['post'])
def login_post():
    uname = request.form['textfield']
    passwrd = request.form['textfield2']
    db=Db()
    qry="select * from login where UserName='"+uname+"' and Password='"+passwrd+"'"
    res=db.selectOne(qry)
    if res is not None:
        session['lid']=res['lid']
        session['log']="lin"
        if res['Type']=='admin':
           return redirect('/Home')
        elif res['Type']=='manufacturer':
             return redirect('/Home_Manufactures')
        elif res['Type']=='retailer':
             return redirect('/Home_Retailer')
        elif res['Type']=='user':
             return redirect('/user_home')
        else:
             return "<script>alert('please check your login credentials');window.location='/'</script>"
    else:
        return "<script>alert('Res is none');window.location='/'</script>"




@app.route('/logout')
def logout():
    session['log']==""
    return render_template("index.html")



#==================================================================================================================ADMIN


@app.route('/Home')
def Home():
    if session['log']=='lin':
        return render_template("Admin/index.html")
    else:
        return "<script>alert('Log out');window.location='/'</script>"



@app.route('/verify_manufactures')
def verify_manufactures():
    db = Db()
    qry = "SELECT * FROM manufacturer where status= 'pending' "
    res = db.select(qry)
    if session['log'] == 'lin':
      return render_template("Admin/verify_manufactures.html", data=res)
    else:
        return "<script>alert('Log out');window.location='/'</script>"


@app.route('/reject_manufactures/<id>')
def reject_manufactures(id):
    db = Db()
    qry="UPDATE `manufacturer` SET `status`='reject' WHERE `man_id`='"+id+"'"
    res=db.update(qry)
    if session['log'] == 'lin':
       return '''<script>alert('Rejected');window.location='/verify_manufactures'</script>'''
    else:
        return "<script>alert('Log out');window.location='/'</script>"



@app.route('/accept_manufactures/<id>')
def accept_manufactures(id):
    db = Db()
    qry="UPDATE `manufacturer` SET `status`='accept' WHERE `man_id`='"+id+"'"
    res=db.update(qry)
    if session['log'] == 'lin':
       return '''<script>alert('Success');window.location='/verify_manufactures'</script>'''
    else:
        return "<script>alert('Log out');window.location='/'</script>"


@app.route('/approved_manufactures')
def approved_manufactures():
    db=Db()
    qry="SELECT * FROM `manufacturer`  where `status`='accept' "
    res=db.select(qry)
    if session['log'] == 'lin':
        return render_template("Admin/Approved Manufactures.html",data=res)
    else:
        return "<script>alert('Log out');window.location='/'</script>"



#
# @app.route('/Change_password')
# def Change_password():
#     if session['log'] == 'lin':
#        return render_template("Admin/ChangePassword.html")
#     else:
#         return "<script>alert('Log out');window.location='/'</script>"
#

#
# @app.route('/Change_passwor_post',methods=['post'])
# def Change_passwor_post():
#     current_pass = request.form['textfield']
#     new_pass = request.form['textfield2']
#     confirm_pass = request.form['textfield3']
#     db = Db()
#     qry="select * from login where password='"+current_pass+"' and lid='"+str(session['lid'])+"'"
#     res=db.selectOne(qry)
#     if res is not None:
#         if new_pass==confirm_pass:
#             qry1=" UPDATE `login` SET `password`='"+new_pass+"' WHERE `lid`='"+str(session['lid'])+"'"
#             res=db.update(qry1)
#     return '''<script>alert('Password changed Successfully');window.location='/Home'</script>'''
#
#================================================================================================================RETAILER


@app.route('/View_User_data')
def View_User_data():
     db = Db()
     qry = "  select * from `quantity` join `USER` on `USER`.`User_id`=`quantity`.`user_id` join `product` on `product`.`pid`=`quantity`.`pid` join `producttype` on `producttype`.`ptId`=`product`.`ptypeid`  where r_lid='"+str(session['lid'])+"' "
     res = db.select(qry)
     if session['log'] == 'lin':
         return render_template('Retailer/ViewUserData.html ',data=res)
     else:
         return "<script>alert('Log out');window.location='/'</script>"



@app.route('/sign_up')
def sign_up():
    return render_template("Retailer/Signup.html")



@app.route('/sign_up_post',methods=['post'])
def sign_up_post():
    shopname  = request.form['textfield']
    o_name  = request.form['textfield2']
    ph = request.form['textfield3']
    ema  = request.form['textfield4']
    place  = request.form['textfield5']
    pst  = request.form['textfield6']
    pin  = request.form['textfield7']
    passwd = request.form['textfield10']
    passwdC = request.form['textfield11']
    db=Db()
    if passwd==passwdC:
        qry="INSERT INTO `login`(UserName,Password,Type) VALUES('"+ema+"','"+passwd+"','retailer')"
        res=db.insert(qry)
        qry2="INSERT INTO retailer(`r_lid`,`s_name`,`o_name`,`phone`,`email`,`place`,`post`,`pin`) VALUES('"+str(res)+"','"+shopname+"','"+o_name+"','"+ema+"','"+ph+"','"+place+"','"+pst+"','"+pin+"')"
        res=db.insert(qry2)
        return redirect('/')
    else:
        "<script>alert('Password dose not match');window.location='/sign_up'</script>"




@app.route('/Home_Retailer')
def Home_Retailer():
    if session['log'] == 'lin':
        return render_template('Retailer/index.html')
    else:
        return "<script>alert('Log out');window.location='/'</script>"





@app.route('/add_user_data')
def add_user_data():
    db = Db()
    qry = "SELECT * FROM `producttype`"
    res = db.select(qry)
    if session['log'] == 'lin':
        return render_template('Retailer/addUserData.html', data=res)
    else:
        return "<script>alert('Log out');window.location='/'</script>"



@app.route('/add_user_data_post', methods=['post'])
def add_user_data_post():
    cardNo = request.form['textfield']
    productId = request.form['textfield2']
    Ptype = request.form['select']
    db = Db()
    qry = " INSERT INTO `quantity`(`r_lid`,`pid`,`user_id`,`PtID`) VALUES('"+str(session['lid'])+"','"+productId+"','"+cardNo+"','"+Ptype+"')"
    res = db.insert(qry)
    if session['log'] == 'lin':
        return "<script>alert('Success');window.location='/add_user_data'</script>"
    else:
        return "<script>alert('Log out');window.location='/'</script>"



#======================================================================================MANU


@app.route('/Home_Manufactures')
def Home_Manufactures():
    if session['log']=='lin':
        return render_template("Manufacturer/index.html")
    else:
        return "<script>alert('Log out');window.location='/'</script>"







@app.route('/manufacturer_registration')
def manufacturer_registration():
    if session['log']=='lin':
        return render_template('/Manufacturer/sign_up.html')
    else:
        return "<script>alert('Log out');window.location='/'</script>"



@app.route('/manufacturer_registration_post', methods=['POST'])
def manufacturer_registration_post():
    cname = request.form['textfield']
    pro = request.form['textfield2']
    email = request.form['textfield3']
    phone = request.form['textfield4']
    place = request.form['textfield5']
    pin = request.form['textfield6']
    post = request.form['textfield7']
    db = Db()
    qry = "INSERT INTO `manufacturer` (`c_name`,`prop_name`,`email`,`phone`,`place`,`pin`,`post`,`status`) VALUES ('"+cname+"','"+pro+"','"+email+"','"+phone+"','"+place+"','"+pin+"','"+post+"','Pending')"
    res = db.insert(qry)
    if session['log'] == 'lin':
        return "<script>alert('Registration Successful');window.location='/'</script>"
    else:
        return "<script>alert('Log out');window.location='/'</script>"



@app.route('/view_manufacturer')
def view_manufacturer():
    db=Db()
    qry="select * from `manufacturer` where `man_lid`= '"+str(session['lid'])+"'"
    res=db.selectOne(qry)
    if session['log'] == 'lin':
        return render_template("Manufacturer/view_company.html", data=res)
    else:
        return "<script>alert('Log out');window.location='/'</script>"

@app.route('/add_product')
def add_product():
    db = Db()
    qry=" select * from producttype"
    res= db.select(qry)
    if session['log'] == 'lin':
        return render_template("Manufacturer/add_product.html", data=res)
    else:
        return "<script>alert('Log out');window.location='/'</script>"


@app.route('/add_product_post', methods=['POST'])
def add_product_post():
    ptypeid=request.form['select']
    pname=request.form['textfield2']
    db = Db()
    qry="INSERT INTO `product` (`man_id`,`p_name`,`ptypeid`) VALUES ('"+str(session['lid'])+"','"+pname+"','"+ptypeid+"')"
    res = db.insert(qry)
    if session['log'] == 'lin':
        return "<script>alert('Product added');window.location='/add_product#about'</script>"
    else:
        return "<script>alert('Log out');window.location='/'</script>"



@app.route('/view_product_manufacture/')
def view_product_manufacture():
    db = Db()
    qry = "SELECT * FROM `product` JOIN `producttype` ON `product`.`ptypeid`=`producttype`.`ptId` where `man_id`='"+str(session['lid'])+"'"
    res = db.select(qry)
    if session['log'] == 'lin':
        return render_template("Manufacturer/view_product_manufacture.html", data=res)
    else:
        return "<script>alert('Log out');window.location='/'</script>"




@app.route('/edit_product/<id>')
def edit_product(id):
    db = Db()
    qry = "SELECT * FROM `product` JOIN `producttype` ON `product`.`ptypeid`=`producttype`.`ptId` where `man_id`='"+str(session['lid'])+"' and pid='"+id+"'"
    res = db.selectOne(qry)
    qry2 = "select * from producttype"
    res2 = db.select(qry2)
    if session['log'] == 'lin':
        return render_template("Manufacturer/edit_product.html", data=res, pd=res2)
    else:
        return "<script>alert('Log out');window.location='/'</script>"



@app.route('/edit_product_post', methods=['POST'])
def edit_product_post():
    id = request.form['id']
    ptypeid = request.form['select']
    pname = request.form['textfield2']
    db = Db()
    qry = "UPDATE `product` SET `p_name`='"+pname+"',`ptypeid`='"+ptypeid+"' WHERE `pid`='"+id+"'"
    res=db.update(qry)
    if session['log'] == 'lin':
        return redirect('/view_product_manufacture#about')
    else:
         return "<script>alert('Log out');window.location='/'</script>"




@app.route('/delete_product/<id>')
def delete_product(id):
    db=Db()
    qry="DELETE FROM  `product` WHERE `pid`='"+id+"'"
    res=db.delete(qry)
    if session['log'] == 'lin':
        return redirect('/view_product_manufacture')
    else:
        return "<script>alert('Log out');window.location='/'</script>"

#============================================================================================================User

@app.route('/user_home')
def user_home():
    if session['log'] == 'lin':
        return  render_template('User/index.html')
    else:
        return "<script>alert('Log out');window.location='/'</script>"



@app.route('/user_signup')
def user_signup():
    return render_template('User/usersign_up.html')




@app.route('/user_signup_post',methods=['post'])
def user_signup_post():
    name = request.form['textfield1']
    Age = request.form['textfield2']
    gender = request.form['textfield3']
    ph = request.form['textfield4']
    ema = request.form['textfield5']
    place = request.form['textfield6']
    post = request.form['textfield7']
    pin = request.form['textfield8']
    passwd = request.form['textfield10']
    c_passwd = request.form['textfield11']
    db=Db()
    if passwd==c_passwd:
        qry="INSERT INTO `login`(UserName,Password,Type) VALUES('"+ema+"','"+passwd+"','retailer')"
        res=db.insert(qry)
        qry2=" insert into user (`User_lid`,`NAME`,`age`,`gender`,`phone`,`email`,`place`,`post`,`pin`) values('"+name+"','"+Age+"','"+gender+"','"+ph+"','"+ema+"','"+place+"','"+post+"','"+pin+"') "
        res=db.insert(qry2)
        return redirect('/')
    else:
        "<script>alert('Password dose not match');window.location='/sign_up'</script>"




@app.route('/profile_managment_view')
def profile_managment_view():
    db = Db()
    qry = "    SELECT * FROM `user` WHERE `User_lid`='"+str(session['lid'])+"'  "
    res = db.selectOne(qry)
    if session['log'] == 'lin':
       return render_template("User/ProfileManagment_View.html",data=res)
    else:
        return "<script>alert('Log out');window.location='/'</script>"



@app.route('/profile_managment')
def profile_managment():
    db = Db()
    qry = "    SELECT * FROM `user` WHERE `User_lid`='"+str(session['lid'])+"'  "
    res = db.selectOne(qry)
    if session['log'] == 'lin':
       return render_template("User/ProfileManagment.html",data=res)
    else:
        return "<script>alert('Log out');window.location='/'</script>"




@app.route('/profile_managment_post',methods=['post'])
def profile_managment_post():
    usrname = request.form['textfield']
    age = request.form['textfield2']
    ph = request.form['textfield3']
    ema = request.form['textfield4']
    place = request.form['textfield5']
    pst = request.form['textfield6']
    pin = request.form['textfield7']
    db = Db()
    qry = "  UPDATE `user` SET `name`='"+usrname+"',`age`='"+age+"',`email`='"+ema+"',`phone`='"+ph+"',`place`='"+place+"',`post`='"+pst+"',`pin`='"+pin+"' WHERE `User_lid`='"+str(session['lid'])+"'  "
    res = db.update(qry)
    if session['log'] == 'lin':
        return redirect("/profile_managment_view")
    else:
        return "<script>alert('Log out');window.location='/'</script>"



@app.route('/product_quantity')
def product_quantity():
    db = Db()
    qry = "select count(`quantity`.`pid`),`quantity`.`PtID`,`producttype`.`TypeName` from `quantity` join  `producttype` on `producttype`.`ptId` = `quantity`.`PtID`  where user_id='2'  GROUP BY `PtID`  "
    res = db.select(qry)
    if session['log'] == 'lin':
        return render_template('User/product_quantity.html', data=res)
    else:
        return "<script>alert('Log out');window.location='/'</script>"







app.run(debug=True,host='0.0.0.0')