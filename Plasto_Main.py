from flask import *
import smtplib
import cv2
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
        elif res['Type']=='collector':
             return redirect('/c_home')
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


@app.route('/add_collector')
def add_collector():
    return render_template("Admin/add_collector.html")

@app.route('/add_collector_post',methods=['post'])
def add_collector_post():
    name = request.form['textfield']
    email = request.form['textfield2']
    place = request.form['textfield3']
    passwd = request.form['textfield4']
    print(email)
    db =Db()
    qry = " insert into `login`(`UserName`,`Password`,`Type`) VALUES('"+email+"','"+passwd+"','collector') "
    res = db.insert(qry)
    qry1 = " insert into `collecter`(`c_name`,`email`,`place`,`c_lid`) VALUE('"+name+"','"+email+"','"+place+"','"+str(res)+"')  "
    res1=db.insert(qry1)
    rep = send_email(name,email,passwd)
    #
    # #-----------mail--------------------
    # sender_email = "plastocas@outlook.com"
    # receiver_email = "yedusankarc@gmail.com"
    # password = "jaison2003"
    # message = "Subject: Dear ",name," You are appointed as garbage collector in Plasto Initiative \n Your Username : ",email,"\n Password : ",passwd,"you can now log in"
    #
    # server = smtplib.SMTP("smtp.office365.com", 587) # Connect to Gmail's SMTP server
    # server.starttls() # Start TLS encryption
    # server.login(sender_email, password) # Login to the email account
    # server.sendmail(sender_email, receiver_email, message) # Send the email
    # server.quit() # Logout from the email account'
    return redirect('/add_collector')



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



@app.route('/accept_manufactures/<id>/<email>/<passwd>')
def accept_manufactures(id,email,passwd):
    db = Db()
    qry1="INSERT INTO `login`(UserName,Password,Type) VALUES('"+email+"','"+passwd+"','manufacturer')"
    res1=db.insert(qry1)
    l=str(res1)
    qry2="UPDATE `manufacturer` SET `man_lid` ='"+l+"',`status`='accept'  WHERE `man_id`='"+id+"' "
    res2=db.update(qry2)
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
    return render_template("Retailer/Ret_SignUP.html")



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
        return "<script>alert('Registration successful');window.location='/'</script>"

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
    qry2 = "SELECT * FROM `quantity` WHERE qid=(SELECT MAX(qid) FROM `quantity`)"
    res2 = db.selectOne(qry2)
    if session['log'] == 'lin':
        return render_template('Retailer/addUserData.html', data=res,ud=res2)
    else:
        return "<script>alert('Log out');window.location='/addUserData.html'</script>"



@app.route('/add_user_data_post', methods=['post'])
def add_user_data_post():
    cardNo = request.form['textfield']
    productId = request.form['textfield2']
    Ptype = request.form['select']
    db = Db()

    qry = " INSERT INTO `quantity`(`r_lid`,`pid`,`user_id`,`PtID`,`date`,`status`) VALUES('"+str(session['lid'])+"','"+productId+"','"+cardNo+"','"+Ptype+"',curdate(),'active')"
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
        return render_template('Manufacturer/Reg.html')




@app.route('/manufacturer_registration_post', methods=['POST'])
def manufacturer_registration_post():
    cname = request.form['textfield']
    pro = request.form['textfield2']
    email = request.form['textfield3']
    phone = request.form['textfield4']
    place = request.form['textfield5']
    pin = request.form['textfield6']
    post = request.form['textfield7']
    passwd = request.form['textfield10']
    c_passwd = request.form['textfield11']
    db = Db()
    if passwd==c_passwd:
        qry = "INSERT INTO `manufacturer` (`c_name`,`prop_name`,`email`,`phone`,`place`,`pin`,`post`,`status`,`passwd`) VALUES ('"+cname+"','"+pro+"','"+email+"','"+phone+"','"+place+"','"+pin+"','"+post+"','Pending','"+passwd+"')"
        res = db.insert(qry)
        return "<script>alert('Registration Successful');window.location='/'</script>"
    else:
        "<script>alert('Password dose not match');window.location='/sign_up'</script>"




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
    return render_template('User/Signup.html')




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
    print(gender)
    db=Db()
    if passwd==c_passwd:
        qry="INSERT INTO `login`(UserName,Password,Type) VALUES('"+ema+"','"+passwd+"','user')"
        res=db.insert(qry)
        qry2=" insert into user (`User_lid`,`NAME`,`age`,`gender`,`phone`,`email`,`place`,`post`,`pin`) values('"+str(res)+"','"+name+"','"+Age+"','"+gender+"','"+ph+"','"+ema+"','"+place+"','"+post+"','"+pin+"') "
        res=db.insert(qry2)
        return "<script>alert('Registration successful');window.location='/'</script>"
    else:
        return "<script>alert('Password dose not match');window.location='/user_signup'</script>"




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
    qry = "  UPDATE `user` SET `name`='"+usrname+"',`age`='"+age+"',`email`='"+ema+"',`phone`='"+ph+"',`place`='"+place+"',`post`='"+pst+"',`pin`='"+pin+"' WHERE `User_lid`='"+str(session['lid'])+"' AND `status`='active'  "
    res = db.update(qry)
    if session['log'] == 'lin':
        return redirect("/profile_managment_view")
    else:
        return "<script>alert('Log out');window.location='/'</script>"



@app.route('/product_quantity')
def product_quantity():
    db = Db()
    qry = "SELECT COUNT(`quantity`.`pid`),`quantity`.`PtID`,`producttype`.`TypeName` FROM `quantity` JOIN  `producttype` ON `producttype`.`ptId` = `quantity`.`PtID` WHERE MONTH(`date`)=MONTH(curdate()) AND `user_id`='" + str(session['lid']) + "' AND `status`='active' GROUP BY `PtID` "
    res = db.select(qry)
    qry1 = "SELECT `product`.`p_name`,`producttype`.`TypeName`,`retailer`.`s_name`,`quantity`.`date` FROM `quantity` JOIN `product` ON`product`.`pid`=`quantity`.`pid` JOIN `retailer` ON `retailer`.`r_lid`=`quantity`.`r_lid` JOIN `producttype` ON `producttype`.`ptId`=`quantity`.`PtID`WHERE MONTH(`date`)=MONTH(curdate()) AND CURDATE() AND `user_id`='" + str(session['lid']) + "' AND `status`='active' "
    res1 = db.select(qry1)
    if session['log'] == 'lin':
        return render_template('User/product_quantity.html', data=res, data1=res1)
    else:
        return "<script>alert('Log out');window.location='/'</script>"


@app.route('/product_quantity_previous/<num>')
def product_quantity_previous(num):
    print(num)
    db = Db()
    qry = "SELECT COUNT(`quantity`.`pid`),`quantity`.`PtID`,`producttype`.`TypeName` FROM `quantity` JOIN  `producttype` ON `producttype`.`ptId` = `quantity`.`PtID` WHERE `date`= DATE_ADD(curdate(), INTERVAL -1 MONTH) AND `user_id`='"+str(session['lid'])+"' AND `status`='active' GROUP BY `PtID` "
    res = db.select(qry)
    qry1 = "SELECT `product`.`p_name`,`producttype`.`TypeName`,`retailer`.`s_name`,`quantity`.`date` FROM `quantity` JOIN `product` ON`product`.`pid`=`quantity`.`pid` JOIN `retailer` ON `retailer`.`r_lid`=`quantity`.`r_lid` JOIN `producttype` ON `producttype`.`ptId`=`quantity`.`PtID`WHERE `date` BETWEEN DATE_ADD(CURDATE(), INTERVAL -1 MONTH) AND CURDATE() AND `user_id`='" + str(session['lid']) + "' AND `status`='active' "
    res1 = db.select(qry1)
    if session['log'] == 'lin':
        return render_template('User/product_quantity_pre.html', data=res, data1=res1)
    else:
        return "<script>alert('Log out');window.location='/'</script>"



@app.route('/product_quantity_six')
def product_quantity_six():
    db = Db()
    qry = "SELECT COUNT(`quantity`.`pid`),`quantity`.`PtID`,`producttype`.`TypeName` FROM `quantity` JOIN  `producttype` ON `producttype`.`ptId` = `quantity`.`PtID` WHERE `date` BETWEEN DATE_ADD(CURDATE(), INTERVAL -6 MONTH) AND CURDATE() AND `user_id`='"+str(session['lid'])+"' AND `status`='active' GROUP BY `PtID` "
    res = db.select(qry)
    qry1 = "SELECT `product`.`p_name`,`producttype`.`TypeName`,`retailer`.`s_name`,`quantity`.`date` FROM `quantity` JOIN `product` ON`product`.`pid`=`quantity`.`pid` JOIN `retailer` ON `retailer`.`r_lid`=`quantity`.`r_lid` JOIN `producttype` ON `producttype`.`ptId`=`quantity`.`PtID`WHERE `date` BETWEEN DATE_ADD(CURDATE(), INTERVAL -6 MONTH) AND CURDATE() AND `user_id`='" + str(session['lid']) + "' AND `status`='active' "
    res1 = db.select(qry1)
    if session['log'] == 'lin':
        return render_template('User/product_quantity_six.html', data=res, data1=res1)
    else:
        return "<script>alert('Log out');window.location='/'</script>"



@app.route('/product_quantity_year')
def product_quantity_year():
    db = Db()
    qry = "SELECT COUNT(`quantity`.`pid`),`quantity`.`PtID`,`producttype`.`TypeName` FROM `quantity` JOIN  `producttype` ON `producttype`.`ptId` = `quantity`.`PtID` WHERE `date` BETWEEN DATE_ADD(CURDATE(), INTERVAL -1 YEAR) AND CURDATE() AND `user_id`='"+str(session['lid'])+"' AND `status`='active' GROUP BY `PtID` "
    res = db.select(qry)
    qry1 = "SELECT `product`.`p_name`,`producttype`.`TypeName`,`retailer`.`s_name`,`quantity`.`date` FROM `quantity` JOIN `product` ON`product`.`pid`=`quantity`.`pid` JOIN `retailer` ON `retailer`.`r_lid`=`quantity`.`r_lid` JOIN `producttype` ON `producttype`.`ptId`=`quantity`.`PtID`WHERE `date` BETWEEN DATE_ADD(CURDATE(), INTERVAL -1 YEAR) AND CURDATE() AND `user_id`='"+str(session['lid'])+"' AND `status`='active' "
    res1 = db.select(qry1)
    if session['log'] == 'lin':
        return render_template('User/product_quantity_year.html', data=res,data1=res1)
    else:
        return "<script>alert('Log out');window.location='/'</script>"


@app.route('/view_score')
def view_score():
    db = Db()
    qry=""
    res=db.select(qry)
    if session['log'] == 'lin':
        return render_template(' ', data=res)
    else:
        return "<script>alert('Log out');window.location='/'</script>"




# ==================================================================collection============================================



@app.route('/c_home')
def c_home():
    if session['log'] == 'lin':
        return render_template('collector/index.html')
    else:
        return "<script>alert('Log out');window.location='/'</script>"




@app.route('/collect')
def collect():
    db =Db()
    qry= "  SELECT * FROM USER  WHERE `User_id` IN(SELECT `user_id` FROM `quantity`WHERE `status`='active')"
    res = db.select(qry)
    return render_template("collector/list.html",data=res)




@app.route('/view_usage_c/<id>')
def view_usage_c(id):
    db = Db()
    qry = "select count(`quantity`.`pid`),`quantity`.`PtID`,`producttype`.`TypeName`,`quantity`.`user_id` from `quantity` join  `producttype` on `producttype`.`ptId` = `quantity`.`PtID`  where user_id='"+id+"' and  `quantity`.`status`='active' GROUP BY `PtID`  "
    res = db.select(qry)
    if session['log'] == 'lin':
        return render_template('collector/usage.html', data=res)
    else:
        return "<script>alert('Log out');window.location='/'</script>"



@app.route('/collect_search', methods=['POST'])
def collect_search():
    db=Db()
    srch = request.form['textfield']
    qry=" SELECT * FROM USER  WHERE `User_id` IN(SELECT `user_id` FROM `quantity`WHERE `status`='active')  AND `place` LIKE '%"+srch+"%' OR `name` LIKE '%"+srch+"%' OR `User_id` LIKE '%"+srch+"%'"
    res=db.select(qry)
    return render_template("collector/list.html",data=res)



@app.route('/remove_quantity/<ptid>/<uid>')
def remove_quantity(ptid,uid):
    db = Db()
    print(ptid)
    print(uid)
    qry =" UPDATE quantity SET `status`='returned' WHERE `PtID`='"+ptid+"' AND `user_id`='"+uid+"'"
    res = db.update(qry)
    return redirect('/view_usage_c/'+uid+'')




@app.route('/add_score_post', methods=['post'])
def add_score_post():
    cardNo = request.form['textfield']
    productId = request.form['textfield2']
    Ptype = request.form['select']
    db = Db()
    qry = " INSERT INTO `quantity`(`r_lid`,`pid`,`user_id`,`PtID`,`date`,`status`) VALUES('"+str(session['lid'])+"','"+productId+"','"+cardNo+"','"+Ptype+"',curdate(),'active')"
    res = db.insert(qry)
    if session['log'] == 'lin':
        return "<script>alert('Success');window.location='/add_user_data'</script>"
    else:
        return "<script>alert('Log out');window.location='/'</script>"


# @app.route("/send_email")
def send_email(n,e,p):
    print(n)
    print(e)
    print(p)
    sender_email = "plastocasn@outlook.com"
    receiver_email = e
    password = "Prashanth@1"
    message = "Subject: Test EmailThis is a test email sent using Python smtplib library in Flask."

    server = smtplib.SMTP("smtp.office365.com", 587) # Connect to Gmail's SMTP server
    server.starttls() # Start TLS encryption
    server.login(sender_email, password) # Login to the email account
    server.sendmail(sender_email, receiver_email, message) # Send the email
    server.quit() # Logout from the email account
    return "Email sent successfully"


@app.route('/qrread')
def qrread():
    return render_template('User/scan.html')

@app.route('/qrread_post', methods=['POST'])
def qrread_post():
    qr = request.files['image']
    qr.save('qrcode.png')

    path ='qrcode.png'
    # path = "/static/images/" + 'qrcode.png'

    filename = cv2.imread('qrcode.png')
    detector = cv2.QRCodeDetector()
    val, p, s, = detector.detectAndDecode(filename)
    print(val)
    db = Db()
    qry = "SELECT * FROM `quantity` JOIN `user` ON `quantity`.`user_id`=`user`.`User_id` JOIN `producttype` ON `quantity`.`PtID`=`producttype`.`ptId` where user.user_id='"+val+"'"
    res = db.selectOne(qry)

    return render_template('User/view_scan.html', data=res)

app.run(debug=True,host='0.0.0.0')