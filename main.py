from flask import Flask,render_template,request,flash,redirect,url_for,session,send_from_directory
from flask_mysqldb import MySQL
from flask_mail import Mail,Message
import random
import os
from passlib.hash import sha256_crypt
from werkzeug.utils import secure_filename
from PIL import Image
app=Flask(__name__)
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Devyash2@'
app.config['MYSQL_DB'] = 'hostel_db'
mysql=MySQL(app)

app.secret_key="qwertyuiopasdfghjklzxcvbnm"

app.config.update(
    DEBUG=True,
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    MAIL_USERNAME='cs207hostelproject@gmail.com',
    MAIL_PASSWORD='cs207dbms'
)

mail=Mail(app)

def send_otp(reciver,otp):
    msg=Message('OTP',
                sender='cs207hostelproject@gmail.com',
                recipients=[reciver])
    msg.body="Here is your one time password :"+str(otp)
    mail.send(msg)
    flash('otp sent succesfully please validate','success')
    return



@app.before_first_request
def init_app():
    session['hostelname'] = 'WELCOME TO IIT INDORE'
    session['show'] = True
    session['logged_in'] =False
    session['signup']=False
    session['otpverify'] = False
    session['otp_2']=False
    session['update_verify']=False
    session['admin']=False
@app.route('/')
def home():
    session['show'] = True
    session['hostelname'] = 'WELCOME TO IIT INDORE'
    cur=mysql.connection.cursor()
    cur.execute("SELECT * FROM notification WHERE showonhome=%s",('yes',))
    x=cur.fetchall()
    cur.execute("SELECT * FROM event WHERE showonhome=%s",('yes',))
    x1=cur.fetchall()
    return render_template('home.html',items=x,items1=x1)
    #return redirect(url_for('login'))
@app.route('/event/<eid>')
def showimg(eid):
    return send_from_directory('C:\\Users\\devan\\Desktop\\fllask\\static\\img\\events',filename=str(eid)+'.jpg')

@app.errorhandler(404)
def not_found(e):
    return render_template("404.html")


@app.route('/apj')
def apj():
    session['show'] = False
    session['hostelname']='A. P. J ABDUL KALAM'
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM staff WHERE hostelname=%s", ('A. P. J ABDUL KALAM HALL OF RESIDENCE',))
    x = cur.fetchall()
    x1 = x[0]
    x = x[1:]
    return render_template('vsb.html', items=x, items1=x1)
@app.route('/vsb')
def vsb():
    session['hostelname']='VIKRAM SARABHAI'
    cur=mysql.connection.cursor()
    cur.execute("SELECT * FROM staff WHERE hostelname=%s",('VIKRAM SARABHAI HALL OF RESIDENCE',))
    x=cur.fetchall()
    x1=x[0]
    x=x[1:]
    return render_template('vsb.html',items=x,items1=x1)

@app.route('/cvr')
def cvr():
    session['hostelname']='C. V. RAMAN'
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM staff WHERE hostelname=%s", ('C. V. RAMAN HALL OF RESIDENCE',))
    x = cur.fetchall()
    x1 = x[0]
    x = x[1:]
    return render_template('vsb.html', items=x, items1=x1)

@app.route('/devi')
def devi():
    session['hostelname']='DEVI AHILYA'
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM staff WHERE hostelname=%s", ('DEVI AHILYA HALL OF RESIDENCE',))
    x = cur.fetchall()
    x1 = x[0]
    x = x[1:]
    return render_template('vsb.html', items=x, items1=x1)

@app.route('/homi')
def homi():
    session['hostelname']='HOMI JEHANGIR BHABHA'
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM staff WHERE hostelname=%s", ('HOMI JEHANGIR BHABHA HALL OF RESIDENCE',))
    x = cur.fetchall()
    x1 = x[0]
    x = x[1:]
    return render_template('vsb.html', items=x, items1=x1)

@app.route('/jcb')
def jcb():
    session['hostelname']='J. C. BOSE'
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM staff WHERE hostelname=%s", ('J. C. BOSE HALL OF RESIDENCE',))
    x = cur.fetchall()
    x1 = x[0]
    x = x[1:]
    return render_template('vsb.html', items=x, items1=x1)

@app.route('/login',methods=['GET','POST'])
def login():
    if('logged_in' in session and session['logged_in']==True):
        return redirect(url_for('home'))
    if(request.method=='POST'):
        username = request.form.get('username')
        password = request.form.get('password')
        session['username']=username
        cur1 = mysql.connection.cursor()
        x1=cur1.execute("SELECT * FROM admins WHERE adminname=%s and password=%s",(username,password))
        if(x1!=0):
            data=cur1.fetchone()

            x2=cur1.execute("SELECT email FROM admins WHERE adminname=%s",(session['username'],))
            session['email']=cur1.fetchone()[0]
            #print(data[3])
            if(data[3]=='1'):
                session['mainadmin']=True
                #print(session['mainadmin'])
                session['hostelname']='VIKRAM SARABHAI HALL OF RESIDENCE'
            else:
                session['mainadmin'] = False

                session['hostelname']=data[4]
            session['logged_in']=True
            session['admin']=True
            return redirect(url_for('admin'))
        x=cur1.execute("SELECT * FROM users WHERE username=%s",(username,))
        if (x!=0):
            data=cur1.fetchone()
            if(sha256_crypt.verify(password,data[2])):
                session['username'] = data[0]
                session['email']=data[1]
                session['logged_in']=True
                return redirect(url_for('home'))
            else:
                flash('wrong password','danger')
                return render_template('login.html')
        else:
            flash('user not registered')
            return render_template('login.html')
    return render_template('login.html')


@app.route('/logout')
def logout():
    session['logged_in']=False
    session['otpverify'] = False
    session['signup'] = False
    return redirect(url_for('home'))
@app.route('/userdetails',methods=["GET","POST"])
def userdetails():
    if('logged_in' in session and session['logged_in']==True):
        return redirect(url_for('home'))
    if ('signup' in session and session['signup'] == False):
        flash('PLEASE SIGNUP FIRST TO ENTER DETAILS','danger')
        return redirect('signup')
    if ('otp' in session and session['otp'] == False):
        flash('please veryfiy the otp first','danger')
        return redirect(url_for('otp'))
    if(request.method=='POST'):
        name=request.form.get('fullname')
        rollno=request.form.get('rollno')
        branch=request.form.get('branch')
        hostelname=request.form.get('hostelname')
        roomno=request.form.get('roomno')
        mobileno=request.form.get('mobileno')
        
        cur=mysql.connection.cursor()
        x=cur.execute("SELECT * FROM users WHERE rollno=(%s)",(rollno,))
        if(int(x)>0):
            flash("ROLL NO. ALREADY EXIST PLEASE USE ANOTHER",'danger')
            return render_template('userdetails.html')
        if(len(name)==0 or len(rollno)==0 or len(branch)==0 or len(hostelname)==0 or len(roomno)==0 or len(mobileno)!=10):
           flash('enter a valid details','danger')
           return redirect(url_for('userdetails'))
        cur = mysql.connection.cursor()
        password = sha256_crypt.encrypt(session['password'])
        cur.execute("INSERT INTO users(username,email,password,name,rollno,branch,hostelname,roomno,mobileno) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)", (session['username'],session['email'],password,name,rollno,branch,hostelname,roomno,mobileno))
        mysql.connection.commit()
        cur.close()
        session['logged_in'] = True
        return redirect(url_for('home'))
    return render_template('userdetails.html')


@app.route('/otpverification',methods=['GET','POST'])
def otp():
    if('logged_in' in session and session['logged_in']==True):
        return redirect(url_for('home'))
    if ('signup' in session and session['signup'] == False):
        flash('PLEASE SIGNUP FIRST TO ENTER DETAILS','danger')
        return redirect(url_for('signup'))
    if(request.method=='POST'):
        num=request.form.get('otp')
        #print(num,session['otp'])
        if(int(num)==session['otp']):
            session['otpverify']=True
            session['signup'] = True
            flash('Successfully registered please enter your details','success')
            return redirect(url_for('userdetails'))
        else:
            flash('OTP ENTERED IS INCORRECT','danger')
            return render_template('otpverify.html')
    return render_template('otpverify.html')


@app.route('/signup',methods=["GET","POST"])
def signup():
    if('logged_in' in session and session['logged_in']==True):
        return redirect(url_for('home'))
    if(request.method=='POST'):
        #add to data base
        username=request.form.get('username')
        email=request.form.get('email')
        password=request.form.get('password')
        if(email[-10:]!='iiti.ac.in'):
            flash('Please use institute mail id only','danger')
            return redirect(url_for('signup'))
        if(len(username)==0 or len(email)==0 or len(password)==0):
            flash('enter a valid details','danger')
            return redirect(url_for('signup'))
        cur=mysql.connection.cursor()
        x=cur.execute("SELECT * FROM users WHERE username=(%s)",(username,))
        if(int(x)>0):
            flash("USERNAME ALREADY EXIST PLEASE USE ANOTHER",'danger')
            return render_template('signup.html')
        x = cur.execute("SELECT * FROM users WHERE email=(%s)", (email,))
        if (int(x) > 0):
            flash("USER ALREADY REGISTERED WITH THIS EMAIL ID",'danger')
            return render_template('signup.html')
        cur.close()
        x1=random.randrange(111111,999999)
        send_otp(email,x1)
        #d={'x':x1,'username':username,'email':email,'password':password}
        session['username'] = username
        session['email'] = email
        session['password'] = password
        session['otp']=x1
        session['otpverify'] = False
        session['signup'] = True
        return redirect(url_for('otp'))
    return render_template('signup.html')

@app.route('/forgot-password',methods=['GET','POST'])
def forgotpassword():
    if('logged_in' in session and session['logged_in']==True):
        return redirect(url_for('home'))
    if(request.method=='POST'):
        email = request.form.get('email')
        cur = mysql.connection.cursor()
        x = cur.execute("SELECT * FROM users WHERE email=(%s)", (email,))
        if (int(x) > 0):
            x2=random.randrange(111111,999999)
            send_otp(email,x2)
            session['otp-2']=x2
            return redirect(url_for('otp2'))
        else:
            flash('Email not registered','danger')
            return render_template('forgotpassword.html')
    return render_template('forgotpassword.html')

@app.route('/otp-2-verify',methods=['GET','POST'])
def otp2():
    if('logged_in' in session and session['logged_in']==True):
        return redirect(url_for('home'))
    if(request.method=='POST'):
        num=request.form.get('otp')
        #print(num,session['otp'])
        if(int(num)==session['otp-2']): 
            flash('Successfully verified','success')
            return redirect(url_for('resetpassword'))
        else:
            flash('OTP ENTERED IS INCORRECT','danger')
            return render_template('otp2.html')
    return render_template('otp2.html')

@app.route('/reset-password',methods=['GET','POST'])
def resetpassword():
     if('logged_in' in session and session['logged_in']==True):
        return redirect(url_for('home'))
     if(request.method=='POST'):
        username=request.form.get('username')
        password=request.form.get('new password')
        confirm_password=request.form.get('confirm password')
        cur = mysql.connection.cursor()
        x = cur.execute("SELECT * FROM users WHERE username=(%s)", (username,))
        if (int(x) > 0 and password==confirm_password):
            password = sha256_crypt.encrypt(password)
            cur.execute("""update users set password=%s where username=%s""",(password,username,))
            mysql.connection.commit()
            return redirect(url_for('login'))
        else:
            flash("Invalid entry.Please check and try again")
            return render_template('resetpassword.html')
     return render_template('resetpassword.html')
        
    
@app.route('/complaints',methods=['GET','POST'])
def complaints():
    if('logged_in' in session and session['logged_in']==False):
        flash('PLEASE LOG IN FIRST','danger')
        return redirect(url_for('login'))
    session['hostelname']='REGISTER YOUR COMPLAINTS'
    session['show']=True
    if(request.method=='POST'):
        subject=request.form.get('subject')
        category=request.form.get('category')
        urgency=request.form.get('urgency')
        timeofavilibility=request.form.get('timeofavial')
        details=request.form.get('details')
        cur=mysql.connection.cursor()
        cur.execute("INSERT INTO complaints(username,subject,category,time_of_availability,details,urgency) VALUES(%s,%s,%s,%s,%s,%s)",(session['username'],subject,category,timeofavilibility,details,urgency))
        mysql.connection.commit()
        cur.close()
        flash('Complaint registered','success')
        return render_template('complaints.html',scrollToAnchor='complaints')

    return render_template('complaints.html')

@app.route('/suggetions',methods=['GET','POST'])
def suggetions():
    if('logged_in' in session and session['logged_in']==False):
        flash('PLEASE LOG IN FIRST','danger')
        return redirect(url_for('login'))
    session['hostelname']='PROVIDE YOUR VALUEABLE SUGGETIONS'
    session['show']=True
    if(request.method=='POST'):
        subject=request.form.get('subject')
        details=request.form.get('details')
        cur=mysql.connection.cursor()
        cur.execute("INSERT INTO suggetions(username,subject,details) VALUES(%s,%s,%s)",(session['username'],subject,details))
        mysql.connection.commit()
        cur.close()
        flash('THANK YOU FOR YOUR VALUEABLE SUGGETION WE WILL IMPORVE OURSELEVES','success')
        return render_template('suggetions.html',scrollToAnchor='contact')

    return render_template('suggetions.html')

@app.route('/profile',methods=['GET','POST'])
def profile():
    if('logged_in' in session and session['logged_in']==False):
        flash('PLEASE LOG IN FIRST','danger')
        return redirect(url_for('login'))
    session['hostelname'] = 'PROFILE'
    cur=mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE email=(%s)",(session['email'],))
    x = cur.fetchone()
    if(request.method=='POST'):
        username=request.form.get('username')
        if (username==''):      
            username=x[0]
        name=request.form.get('name')
        if (name==''):
            name=x[3]
        rollno=request.form.get('rollno')
        if (rollno==''):
            rollno=x[4]
        branch=request.form.get('branch')
        if (branch==''):
            branch=x[5]
        hostelname=request.form.get('hostelname')
        if(hostelname==''):
            hostelname=x[6]
        roomno=request.form.get('roomno')
        if(roomno==''):
            roomno=x[7]
        mobileno=request.form.get('mobileno')
        if(mobileno==''):
            mobileno=x[8]
        password=request.form.get('password')
        file = request.files['file']
        cur=mysql.connection.cursor()
        x2=cur.execute("SELECT * FROM users WHERE username=%s ",(username,))
        if(x2!=0 and username!=x[0]):
            flash('Username already Exist!!')
            return render_template('profile.html',x=x,scrollToAnchor='profile')
        x2=cur.execute("SELECT * FROM users WHERE rollno=%s",(rollno,))
        if(x2!=0 and rollno!=x[4]):
            flash('Roll No. already Exist!!')
            return render_template('profile.html',x=x,scrollToAnchor='profile')
        else:
            cur.execute("SELECT * FROM users WHERE email=(%s)", (session['email'],))
            x = cur.fetchone()
            if (sha256_crypt.verify(request.form.get('password'), x[2])):

                session['username']=username
               
                cur.execute('update users set username=%s,name=%s,rollno=%s,branch=%s,hostelname=%s,roomno=%s,mobileno=%s where email=%s',(username,name,rollno,branch,hostelname,roomno,mobileno,session['email'],))
                mysql.connection.commit()
                if (file and file.filename != ''):
                    if(os.path.isfile('C:\\Users\\devan\\Desktop\\fllask\\static\\img\\users\\'+str(x[0])+'.jpg')):
                        os.remove('C:\\Users\\devan\\Desktop\\fllask\\static\\img\\users\\'+str(x[0])+'.jpg')
                    l=file.filename.split('.')
                    file.filename = str(session['username']) +'1'+'.'+str(l[-1])
                    filename = secure_filename(file.filename)
                    file.save(os.path.join('C:\\Users\\devan\\Desktop\\fllask\\static\\img\\users', filename))
                    s='C:\\Users\\devan\\Desktop\\fllask\\static\\img\\users\\'+str(filename)
                    img1=Image.open(s)
                    img2=img1.convert('RGB')
                    s = 'C:\\Users\\devan\\Desktop\\fllask\\static\\img\\users\\' + str(session['username'])+'.jpg'
                    img2.save(s)
                    os.remove(os.path.join('C:\\Users\\devan\\Desktop\\fllask\\static\\img\\users', filename))
            else:
                flash('Incorrect Password')
                return render_template('profile.html', x=x, scrollToAnchor='profile')
    return render_template('profile.html', x=x)

@app.route('/update_verify',methods=['GET','POST'])
def update_verify():
    if (request.method=='POST'):
        cur=mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE email=(%s)",(session['email'],))
        x = cur.fetchone()
        if(sha256_crypt.verify(request.form.get('password'), x[2])):
            session['update_verify']=True
            session['username']=x[0]
            return redirect(url_for('profile'))
        else:
            flash('Incorrect Password!')
    return render_template('update_verify.html')

@app.route('/admin')
def admin():
    if ('logged_in' in session and session['logged_in'] == False):
        flash('PLEASE LOG IN FIRST', 'danger')
        return redirect(url_for('login'))
    if ('admin' in session and session['admin']== False):
        return redirect(url_for('home'))
    cur = mysql.connection.cursor()
    cur.execute("SELECT complaints.complaint_id,complaints.username,complaints.subject,complaints.category,complaints.urgency,complaints.time_of_availability,complaints.details,complaints.complain_status FROM complaints NATURAL JOIN users WHERE users.hostelname=%s AND complaints.complain_status=%s",(session['hostelname'],'pending'))
    x = cur.fetchall()
    cur.execute("SELECT suggetions.suggetion_id,suggetions.username,suggetions.subject,suggetions.details FROM suggetions NATURAL JOIN users WHERE users.hostelname=%s",(session['hostelname'],))
    x1=cur.fetchall()
    return render_template('admin/admin.html',items=x,items1=x1)
@app.route('/adminprofile',methods=['GET','POST'])
def adminprofile():
    if ('logged_in' in session and session['logged_in'] == False):
        flash('PLEASE LOG IN FIRST', 'danger')
        return redirect(url_for('login'))
    if ('admin' in session and session['admin']== False):
        return redirect(url_for('home'))
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM admins WHERE adminname=(%s)", (session['username'],))
    x = cur.fetchone()
    if (request.method == 'POST'):
        username = request.form.get('username')
        if (username == ''):
            username = x[1]
        if (request.form.get('password')== x[2]): 
            cur = mysql.connection.cursor()
            cur.execute("UPDATE admins SET adminname=%s WHERE email=%s",(username,x[5]))
            mysql.connection.commit()
            session['username']=username
        else :
            flash('incorrect password')
    return render_template('admin/adminprofile.html',x=x)
@app.route('/changestatus/<cid>')
def changestatus(cid):
    cur=mysql.connection.cursor()
    cur.execute("UPDATE complaints SET complain_status=%s WHERE complaint_id=%s",('resolved',cid))
    mysql.connection.commit()
    return redirect(url_for('admin'))
@app.route('/vikram')
def vikram():
    session['hostelname']='VIKRAM SARABHAI HALL OF RESIDENCE'
    return redirect(url_for('admin'))
@app.route('/abdul')
def abdul():
    session['hostelname']='A. P. J ABDUL KALAM HALL OF RESIDENCE'
    return redirect(url_for('admin'))
@app.route('/devia')
def devia():
    session['hostelname']='DEVI AHILYA HALL OF RESIDENCE'
    return redirect(url_for('admin'))
@app.route('/cvraman')
def cvraman():
    session['hostelname']='C. V. RAMAN HALL OF RESIDENCE'
    return redirect(url_for('admin'))
@app.route('/homijangir')
def homijangir():
    session['hostelname']='HOMI JEHANGIR BHABHA HALL OF RESIDENCE'
    return redirect(url_for('admin'))
@app.route('/jcbose')
def jcbose():
    session['hostelname']='J. C. BOSE HALL OF RESIDENCE'
    return redirect(url_for('admin'))

@app.route('/studentdetails')
def studentdetails():
    if ('logged_in' in session and session['logged_in'] == False):
        flash('PLEASE LOG IN FIRST', 'danger')
        return redirect(url_for('login'))
    if ('admin' in session and session['admin']== False):
        return redirect(url_for('home'))
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE hostelname=%s",(session['hostelname'],))
    item=cur.fetchall()
    return render_template('admin/students.html',items=item)
@app.route('/vikrams')
def vikrams():
    session['hostelname']='VIKRAM SARABHAI HALL OF RESIDENCE'
    return redirect(url_for('studentdetails'))
@app.route('/abduls')
def abduls():
    session['hostelname']='A. P. J ABDUL KALAM HALL OF RESIDENCE'
    return redirect(url_for('studentdetails'))
@app.route('/devias')
def devias():
    session['hostelname']='DEVI AHILYA HALL OF RESIDENCE'
    return redirect(url_for('studentdetails'))
@app.route('/cvramans')
def cvramans():
    session['hostelname']='C. V. RAMAN HALL OF RESIDENCE'
    return redirect(url_for('studentdetails'))
@app.route('/homijangirs')
def homijangirs():
    session['hostelname']='HOMI JEHANGIR BHABHA HALL OF RESIDENCE'
    return redirect(url_for('studentdetails'))
@app.route('/jcboses')
def jcboses():
    session['hostelname']='J. C. BOSE HALL OF RESIDENCE'
    return redirect(url_for('studentdetails'))

@app.route('/hostelstaff')
def hostelstaff():
    if ('logged_in' in session and session['logged_in'] == False):
        flash('PLEASE LOG IN FIRST', 'danger')
        return redirect(url_for('login'))
    if ('admin' in session and session['admin']== False):
        return redirect(url_for('home'))
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM staff WHERE hostelname=%s",(session['hostelname'],))
    item=cur.fetchall()
    return render_template('admin/hstaff.html',items=item)
@app.route('/vikramhs')
def vikramhs():
    session['hostelname']='VIKRAM SARABHAI HALL OF RESIDENCE'
    return redirect(url_for('hostelstaff'))
@app.route('/abdulhs')
def abdulhs():
    session['hostelname']='A. P. J ABDUL KALAM HALL OF RESIDENCE'
    return redirect(url_for('hostelstaff'))
@app.route('/deviahs')
def deviahs():
    session['hostelname']='DEVI AHILYA HALL OF RESIDENCE'
    return redirect(url_for('hostelstaff'))
@app.route('/cvramanhs')
def cvramanhs():
    session['hostelname']='C. V. RAMAN HALL OF RESIDENCE'
    return redirect(url_for('hostelstaff'))
@app.route('/homijangirhs')
def homijangirhs():
    session['hostelname']='HOMI JEHANGIR BHABHA HALL OF RESIDENCE'
    return redirect(url_for('hostelstaff'))
@app.route('/jcbosehs')
def jcbosehs():
    session['hostelname']='J. C. BOSE HALL OF RESIDENCE'
    return redirect(url_for('hostelstaff'))
@app.route('/deletehs/<sid>')
def deletehs(sid):
    if ('logged_in' in session and session['logged_in'] == False):
        flash('PLEASE LOG IN FIRST', 'danger')
        return redirect(url_for('login'))
    if ('admin' in session and session['admin']== False):
        return redirect(url_for('home'))
    cur=mysql.connection.cursor()
    cur.execute("DELETE FROM staff WHERE staff_id=%s",(sid,))
    mysql.connection.commit()
    return redirect(url_for('hostelstaff'))
@app.route('/staffprofile/<sid>',methods=['GET','POST'])
def staffprofile(sid):
    if ('logged_in' in session and session['logged_in'] == False):
        flash('PLEASE LOG IN FIRST', 'danger')
        return redirect(url_for('login'))
    if ('admin' in session and session['admin']== False):
        return redirect(url_for('home'))
    session['updatep']=True
    cur=mysql.connection.cursor()
    cur.execute("SELECT * FROM staff WHERE staff_id=%s",(sid,))
    x=cur.fetchone()
    if (request.method == 'POST'):
        fullname = request.form.get('fullname')
        if (fullname == ''):
            fullname = x[1]
        post = request.form.get('post')
        if (post == ''):
            post = x[2]
        hostelname = request.form.get('hostelname')
        if (hostelname == 'Choose Hostel'):
            hostelname = x[3]
        link = request.form.get('link')
        if (link == ''):
            link = x[4]
        file = request.files['file']
        cur=mysql.connection.cursor()
        cur.execute("UPDATE staff SET fullname=%s,post=%s,hostelname=%s,link=%s WHERE staff_id=%s",(fullname,post,hostelname,link,sid))
        mysql.connection.commit()
        if (file and file.filename != ''):
            if (os.path.isfile('C:\\Users\\devan\\Desktop\\fllask\\static\\img\\staff\\' + str(x[0]) + '.jpg')):
                os.remove('C:\\Users\\devan\\Desktop\\fllask\\static\\img\\staff\\' + str(x[0]) + '.jpg')
            l = file.filename.split('.')
            file.filename = str(sid) + '1' + '.' + str(l[-1])
            filename = secure_filename(file.filename)
            file.save(os.path.join('C:\\Users\\devan\\Desktop\\fllask\\static\\img\\staff', filename))
            s = 'C:\\Users\\devan\\Desktop\\fllask\\static\\img\\staff\\' + str(filename)
            img1 = Image.open(s)
            img2 = img1.convert('RGB')
            s = 'C:\\Users\\devan\\Desktop\\fllask\\static\\img\\staff\\' + str(sid) + '.jpg'
            img2.save(s)
            os.remove(os.path.join('C:\\Users\\devan\\Desktop\\fllask\\static\\img\\staff', filename))
        return redirect(url_for('hostelstaff'))
    return render_template('admin/staffprofile.html',x=x)

@app.route('/addstaff',methods=['POST','GET'])
def addstaff():
    if ('logged_in' in session and session['logged_in'] == False):
        flash('PLEASE LOG IN FIRST', 'danger')
        return redirect(url_for('login'))
    if ('admin' in session and session['admin']== False):
        return redirect(url_for('home'))
    session['updatep']=False
    if (request.method == 'POST'):
        fullname = request.form.get('fullname')
        post = request.form.get('post')
        hostelname = request.form.get('hostelname')
        link = request.form.get('link')
        file = request.files['file']
        cur=mysql.connection.cursor()
        cur.execute("INSERT INTO staff(fullname,post,hostelname,link) VALUES(%s,%s,%s,%s)",(fullname,post,hostelname,link))
        mysql.connection.commit()
        cur=mysql.connection.cursor()
        cur.execute("SELECT * FROM staff WHERE fullname=%s AND post=%s AND hostelname=%s AND link=%s",(fullname,post,hostelname,link))
        x=cur.fetchone()
        if (file and file.filename != ''):
            if (os.path.isfile('C:\\Users\\devan\\Desktop\\fllask\\static\\img\\staff\\' + str(x[0]) + '.jpg')):
                os.remove('C:\\Users\\devan\\Desktop\\fllask\\static\\img\\staff\\' + str(x[0]) + '.jpg')
            l = file.filename.split('.')
            file.filename = str(x[0]) + '1' + '.' + str(l[-1])
            filename = secure_filename(file.filename)
            file.save(os.path.join('C:\\Users\\devan\\Desktop\\fllask\\static\\img\\staff', filename))
            s = 'C:\\Users\\devan\\Desktop\\fllask\\static\\img\\staff\\' + str(filename)
            img1 = Image.open(s)
            img2 = img1.convert('RGB')
            s = 'C:\\Users\\devan\\Desktop\\fllask\\static\\img\\staff\\' + str(x[0]) + '.jpg'
            img2.save(s)
            os.remove(os.path.join('C:\\Users\\devan\\Desktop\\fllask\\static\\img\\staff', filename))
        return redirect(url_for('hostelstaff'))
    else :
        x=[]
    return render_template('admin/staffprofile.html',x=x)

@app.route('/events')
def events():
    if ('logged_in' in session and session['logged_in'] == False):
        flash('PLEASE LOG IN FIRST', 'danger')
        return redirect(url_for('login'))
    if ('admin' in session and session['admin']== False):
        return redirect(url_for('home'))
    cur=mysql.connection.cursor()
    cur.execute("SELECT * FROM notification")
    x=cur.fetchall()
    cur.execute("SELECT * FROM event")
    x1=cur.fetchall()
    return render_template('admin/event.html',items=x,items1=x1)
@app.route('/addnotification',methods=['GET','POST'])
def addnotification():
    if ('logged_in' in session and session['logged_in'] == False):
        flash('PLEASE LOG IN FIRST', 'danger')
        return redirect(url_for('login'))
    if ('admin' in session and session['admin']== False):
        return redirect(url_for('home'))
    if(request.method=='POST'):
        title=request.form.get('title')
        url=request.form.get('url')
        cur=mysql.connection.cursor()
        cur.execute("INSERT INTO notification(title,url) VALUES(%s,%s)",(title,url))
        mysql.connection.commit()
        return redirect(url_for('events'))
    return render_template('admin/notification.html')

@app.route('/changestatusn/<nid>')
def changestatusn(nid):
    if ('logged_in' in session and session['logged_in'] == False):
        flash('PLEASE LOG IN FIRST', 'danger')
        return redirect(url_for('login'))
    if ('admin' in session and session['admin']== False):
        return redirect(url_for('home'))
    cur = mysql.connection.cursor()
    cur.execute("SELECT showonhome FROM notification WHERE notification_id=%s", (nid,))
    if (cur.fetchone()[0] == 'yes'):
        cur.execute("UPDATE notification SET showonhome=%s WHERE notification_id=%s", ('no', nid))
    else:
        cur.execute("UPDATE notification SET showonhome=%s WHERE notification_id=%s", ('yes', nid))
    mysql.connection.commit()
    return redirect(url_for('events'))
@app.route('/changestatuse/<eid>')
def changestatuse(eid):
    if ('logged_in' in session and session['logged_in'] == False):
        flash('PLEASE LOG IN FIRST', 'danger')
        return redirect(url_for('login'))
    if ('admin' in session and session['admin']== False):
        return redirect(url_for('home'))
    cur=mysql.connection.cursor()
    cur.execute("SELECT showonhome FROM event WHERE event_id=%s",(eid,))
    if(cur.fetchone()[0]=='yes'):
        cur.execute("UPDATE event SET showonhome=%s WHERE event_id=%s",('no',eid))
    else:
        cur.execute("UPDATE event SET showonhome=%s WHERE event_id=%s",('yes',eid))
    mysql.connection.commit()
    return redirect(url_for('events'))


@app.route('/addevent',methods=['POST','GET'])
def addevent():
    if ('logged_in' in session and session['logged_in'] == False):
        flash('PLEASE LOG IN FIRST', 'danger')
        return redirect(url_for('login'))
    if ('admin' in session and session['admin']== False):
        return redirect(url_for('home'))
    if(request.method=='POST'):
        title=request.form.get('title')
        cur=mysql.connection.cursor()
        cur.execute("INSERT INTO event(title) VALUES(%s)",(title,))
        mysql.connection.commit()
        file = request.files['file']
        cur.execute('SELECT * FROM event WHERE title=%s',(title,))
        x=cur.fetchone()
        if (file and file.filename != ''):
            if (os.path.isfile('C:\\Users\\devan\\Desktop\\fllask\\static\\img\\events\\' + str(x[0]) + '.jpg')):
                os.remove('C:\\Users\\devan\\Desktop\\fllask\\static\\img\\events\\' + str(x[0]) + '.jpg')
            l = file.filename.split('.')
            file.filename = str(x[0]) + '1' + '.' + str(l[-1])
            filename = secure_filename(file.filename)
            file.save(os.path.join('C:\\Users\\devan\\Desktop\\fllask\\static\\img\\events', filename))
            s = 'C:\\Users\\devan\\Desktop\\fllask\\static\\img\\events\\' + str(filename)
            img1 = Image.open(s)
            img2 = img1.convert('RGB')
            s = 'C:\\Users\\devan\\Desktop\\fllask\\static\\img\\events\\' + str(x[0]) + '.jpg'
            img2.save(s)
            os.remove('C:\\Users\\devan\\Desktop\\fllask\\static\\img\\events\\' + filename)
        return redirect(url_for('events'))
    return render_template('admin/addevent.html')
app.run(debug=True)