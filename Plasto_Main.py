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
        # if res['Type']=='admin':
        return redirect('/Home')
        # elif res['Type']=='manufacture':
        #     return redirect('/Home_Manufactures')
        # elif res['Type']=='retailer':
        #     return redirect('/Home_Retailer')
        # else:
        #     return "<script>alert('please check your login credentials');window.location='/'</script>"
    else:
        return "<script>alert('Res is none');window.location='/'</script>"



#==================================================================================================================ADMIN



@app.route('/logout')
def logout():
    session['log']==""
    return render_template("index.html")



@app.route('/Home')
def Home():
    if session['log']=='lin':
        return render_template("Admin/Admin_Home.html")
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
#================================================================================================================MANUFACTERRS







app.run(debug=True,host='0.0.0.0')