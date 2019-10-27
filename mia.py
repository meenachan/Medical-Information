from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash 
from flask_mysqldb import MySQL 
import MySQLdb.cursors
import json


app = Flask(__name__)
app.static_folder = 'static'
app.secret_key = 'yo'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '123'
app.config['MYSQL_DB'] = 'mia'

mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('index.html')


#doctor sign up
@app.route('/dsign.html',methods=['GET', 'POST'])
def dsign():
    if request.method == "POST":
        details = request.form
        Doc_id = details['Doc_id']
        Passwd = details['Passwd']
        Name = details['Name']
        Specialization = details['Specialization']
        Experience = details['Experience']
        Qualification = details['Qualification']
        Clinic = details['Clinic']
        Patient_id = details['Patient_id']
        Contact = details['Contact']
        cur = mysql.connection.cursor()
        try:
            cur.execute("INSERT INTO Doctors (Doc_id, Name, Specialization , Experience, Clinic, Qualification, Contact ,Patient_id, Passwd) VALUES (%s,  %s , %s , %s , %s , %s, %s, %s, %s)", (Doc_id, Name, Specialization, Experience, Clinic, Qualification, Contact, Patient_id, Passwd))
            mysql.connection.commit()
        except Exception as e:
            flash("Error!! Try Again!")
            return render_template('dsign.html',msg=e)   
        cur.close()
        return redirect(url_for('signup'))

    return render_template('dsign.html')


#patient sign up
@app.route('/psign.html',methods=['GET', 'POST'])
def psign():
    msg= ' '
    if request.method == "POST":
        details = request.form
        Pat_id = details['Pat_id']
        passwd = details['passwd']
        Name = details['Name']
        Contact = details['Contact']
        Insurance_id = details['Insurance_id']
        Medical_info = details['Medical_info']
        #Clinic = details['Clinic']
        Doc_Id = details['Doc_Id']
        #Contact = details['Contact']
        cur = mysql.connection.cursor()
        try:
            cur.execute("INSERT INTO Patient(Pat_id, Name, Contact, Insurance_id, Medical_info, Doc_Id, passwd) VALUES (%s,  %s , %s , %s , %s , %s, %s)", (Pat_id, Name, Contact, Insurance_id, Medical_info, Doc_Id, passwd))
            mysql.connection.commit()
        except Exception as e:
            flash("Error !! ")
            return render_template('psign.html', msg=e)    
        cur.close()
        return redirect(url_for('logpat'))
    return render_template('psign.html')
   

 #business sign up  
@app.route('/esign.html',methods=['GET', 'POST'])
def esign():
    if request.method == "POST":
        details = request.form
        licence= details['licence']
        passwd = details['passwd']
        Name = details['Name']
        Address = details['Address']
        owner = details['owner']
        cur = mysql.connection.cursor()
        try:
            cur.execute("INSERT INTO Retailer(licence, Name, Address, owner, passwd) VALUES (%s,  %s , %s , %s, %s)", (licence, Name, Address, owner, passwd))
            mysql.connection.commit()
        except Exception as e:
            flash("Error!!!!Try again!")
            return render_template('esign.html', msg=e)
        cur.close()
        return redirect(url_for('logenter'))
    return render_template('esign.html')


#doctors sign in 
@app.route('/signup.html', methods=['GET', 'POST'])
def signup():
    msg = ''
    if request.method == "POST":
        details = request.form
        Doc_id = details['doc_id']
        Passwd = details['passwd']
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM Doctors where Doc_id = %s AND Passwd = %s", (Doc_id, Passwd)) 
        username = cur.fetchone()
        if username:
            session['loggedin'] = True
            session['Doc_id'] = username[0]
            session['Name'] = username[1]
            session['Specialization'] = username[2]
            session['Experience'] = username[3]
            session['Clinic'] = username[4]
            session['Qualification'] = username[5]
            session['Contact'] = username[6]
            session['Patient_id'] = username[7]

            # Redirect to home page
            return redirect(url_for('home'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
    # Show the login form with message (if any)
    return render_template('signup.html', msg=msg)
       
       
       
    #     # if username:
    #     #      dread(Doc_id,Passwd)
    #     # else:
    #     #     print('error')
    #     mysql.connection.commit()
    #     cur.close()    
    # return render_template('signup.html')
#patient
@app.route('/logpat.html', methods=['GET', 'POST'])
def logpat():
    msg=' '
    if request.method == "POST":
        details = request.form
        pat_id = details['pat_id']
        passwd = details['passwd']
        cur = mysql.connection.cursor()
        try:
            cur.execute("SELECT * FROM Patient where Pat_id = %s and passwd = %s",(pat_id, passwd)) 
            username = cur.fetchone()
            if username:
                session['loggedin'] = True
                session['Pat_id'] = username[0]
                session['Name'] = username[1]
                session['Contact'] = username[2]
                session['Insurance_id'] = username[3]
                session['Medical_info'] = username[4]
                session['Doc_id'] = username[5]
                session['passwd'] = username[6]
             # Redirect to home page
                return redirect(url_for('phome'))
            
            mysql.connection.commit()    
        except Exception as e:
            flash("Error!!!")
            # Account doesnt exist or username/password incorrect
            return render_template('logpat.html', msg=e)
        
        cur.close()    
    return render_template('logpat.html')


#shop
@app.route('/logenter.html', methods=['GET', 'POST'])
def logenter():
    msg=''
    if request.method == "POST":
        details = request.form
        licence = details['licence']
        passwd = details['passwd']
        cur = mysql.connection.cursor()
        try:
            cur.execute("SELECT * FROM Retailer where licence = %s and passwd = %s",(licence, passwd)) 
            username = cur.fetchone()
            if username:
                session['loggedin'] = True
                session['licence'] = username[0]
                session['Name'] = username[1]
                session['Address'] = username[2]
                session['owner'] = username[3]
                session['passwd'] = username[4]
             # Redirect to home page
                return redirect(url_for('ehome'))
            mysql.connection.commit()    
       
        except Exception as e:
            flash("Error!!!")
            # Account doesnt exist or username/password incorrect
       
        cur.close()    
    return render_template('logenter.html')


#
# @app.route('/showUsers')
# def display():
#     return render_template('display.html')

@app.route('/udisplay.html')
def pread( pat_id , passwd):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Patient WHERE Pat_id = %s and passwd = %s)",(pat_id,passwd))
    names = cur.fetchall()
    names_dict = []
    for name in names:
        name_dict = {
            'Name': name[0],
            'LastName': name[1]}
        names_dict.append(name_dict)
    data = jsonify(names_dict)
    return render_template('display.html', data=names)


@app.route('/ddisplay.html')
def dread( doc_id , passwd):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Doctors WHERE Doc_id = %s and Passwd = %s)", (doc_id,passwd))
    names = cur.fetchall()
    names_dict = []
    for name in names:
        name_dict = {
            'Doc_id': name[0],
            'Name': name[1]}
        names_dict.append(name_dict)
    data = jsonify(names_dict)
    return render_template('ddisplay.html', data=names)




@app.route('/edisplay.html')
def eread( lic , passwd):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Retailer WHERE licence = %s and passwd = %s)",(lic,passwd))
    names = cur.fetchall()
    names_dict = []
    for name in names:
        name_dict = {
            'Licence': name[0],
            'Name': name[1]}
        names_dict.append(name_dict)
    data = jsonify(names_dict)
    return render_template('edisplay.html', data=names)

@app.route('/signup/home')
def home():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        return render_template('home.html', name=session['Name'])
    # User is not loggedin redirect to login page
    return redirect(url_for('signup'))

@app.route('/signup/profile')
def profile():
    # Check if user is loggedin
    if 'loggedin' in session:
        # We need all the account info for the user so we can display it on the profile page
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM Doctors WHERE Doc_id = %s', [session['Doc_id']])
        username = cursor.fetchone()
        # Show the profile page with account info
        return render_template('profile.html', username=username)
    # User is not loggedin redirect to login page
    return redirect(url_for('signup'))

@app.route('/signup/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('Doc_id', None)
   session.pop('Name', None)
   # Redirect to login page
   return redirect(url_for('signup'))

@app.route('/profile/search', methods=['GET', 'POST'])
def search():
    if request.method == "POST":
        Pat_id = request.form['Pat_id']
        # search by pat_id 
        cur = mysql.connection.cursor()
        cur.execute(" SELECT * FROM Patient WHERE Pat_id = %s", [Pat_id])
        data = cur.fetchall()
        # #all in the search box will return all the tuples
        if len(data) == 0 or Pat_id == 'all': 
            cur.execute("SELECT * from Patient")
            data = cur.fetchall()
            mysql.connection.commit()
        return render_template('search.html', data = data)
           
    return render_template('search.html')   

@app.route('/profile/med',methods=['GET', 'POST'])
def med():
    msg = ""
    if request.method == "POST":
        details = request.form
        Drug_name = details['Drug_name']
        Disease = details['Disease']
        shop_id = details['shop_id']
        company = details['company']
        cur = mysql.connection.cursor()
        try:
            cur.execute("INSERT INTO  Drugs(Drug_name, Disease , Shop_id, company) VALUES (%s,  %s , %s , %s)", (Drug_name, Disease , shop_id , company))
            mysql.connection.commit()
          
        except Exception as e:
            flash(" Error !!!Please check the details again")
        
        cur.close()
        return render_template('med.html', msg=e)
        
    return render_template('med.html',msg=msg)

@app.route('/signup/dupdate.html', methods=['GET', 'POST'])
def dupdate():
    msg = ""
    if request.method == "POST":
        details = request.form
        # Doc_id = details['Doc_id']
        # Passwd = details['Passwd']
        Name = details['Name']
        Specialization = details['Specialization']
        Experience = details['Experience']
        Qualification = details['Qualification']
        Clinic = details['Clinic']
        # Patient_id = details['Patient_id']
        Contact = details['Contact']
        cur = mysql.connection.cursor()
        try:
            cur.execute("UPDATE Doctors  SET  Name = %s , Specialization = %s, Experience = %s,  Clinic = %s, Qualification= %s, Contact =%s  WHERE Doc_id = %s",(Name,Specialization,Experience,Clinic,Qualification,Contact,[session['Doc_id']]))
            mysql.connection.commit()
            flash("Updated!!")
        except Exception as e:
            flash(e)
            return render_template('dupdate.html',msg=e)
            
        cur.close()

    return render_template('dupdate.html')



#doctors appointment page
@app.route('/signup/appt.html', methods=['POST', 'GET'])
def appt():
    msg=' '
    if request.method == "POST":
        #search by date
        date = request.form['date']
        cur = mysql.connection.cursor()
        try:
            cur.execute(" SELECT * FROM docapt WHERE date = %s", [date])
            data = cur.fetchall()
            mysql.connection.commit()
        # to handle exceptions
        except Exception  as e:
            flash("Try again!!")
            return render_template('appt.html',msg=e)
        if len(data)==0:
            flash("Try again")
        return render_template('appt.html', data=data)
        cur.close()
    return render_template('appt.html')
#--------------------------------------------------------------------------------------------------




#patient route
@app.route('/logpat/phome')
def phome():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        return render_template('phome.html', name=session['Name'])
    # User is not loggedin redirect to login page
    return redirect(url_for('logpat'))

@app.route('/logpat/uprofile')
def uprofile():
    # Check if user is loggedin
    if 'loggedin' in session:
        # We need all the account info for the user so we can display it on the profile page
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM Patient WHERE Pat_id = %s', [session['Pat_id']])
        username = cursor.fetchone()
        # Show the profile page with account info
        return render_template('uprofile.html', username=username)
    # User is not loggedin redirect to login page
    return redirect(url_for('logpat'))

@app.route('/logpat/plogout')
def plogout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('Pat_id', None)
   session.pop('Name', None)
   # Redirect to login page
   return redirect(url_for('plogpat'))

@app.route('/logpat/pupdate.html', methods=['GET', 'POST'])
def pupdate():
    msg = ""
    if request.method == "POST":
        details = request.form
        # Doc_id = details['Doc_id']
        # Passwd = details['Passwd']
        Name = details['Name']
        Medical_info = details['Medical_info']
        Insurance_id = details['Insurance_id']
        Doc_id = details['Doc_id']
        # Clinic = details['Clinic']
        # Patient_id = details['Patient_id']
        Contact = details['Contact']
        cur = mysql.connection.cursor()
        try:
            cur.execute("UPDATE Patient  SET  Name = %s , Medical_info = %s, Insurance_id = %s,  Doc_id = %s, Contact =%s  WHERE Pat_id = %s",(Name,Medical_info,Insurance_id,Doc_id,Contact,[session['Pat_id']]))
            mysql.connection.commit()
            flash("Updated!!")
        except Exception as e:
            flash(e)
            return render_template('pupdate.html',msg=e)
            
        cur.close()

    return render_template('pupdate.html')



@app.route('/uprofile/search', methods=['GET', 'POST'])
def usearch():
    if request.method == "POST":
        Specialization = request.form['Specialization']
        # search by Specialization
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM Doctors WHERE Specialization = %s", [Specialization])
        data = cur.fetchall()
        # #all in the search box will return all the tuples
        if len(data) == 0 or Specialization == 'all': 
            cur.execute("SELECT * from Doctors")
            data = cur.fetchall()
            mysql.connection.commit()
        return render_template('usearch.html', data = data)
           
    return render_template('usearch.html')   


@app.route('/logpat/uappt.html', methods=['POST', 'GET'])
def uappt():
    msg=' '
    if request.method == "POST":
        #search by date
        Doc_id = request.form['Doc_id']
        date = request.form['date']
        time = request.form['time']
        cur = mysql.connection.cursor()
        try:
            cur.execute("INSERT INTO docapt(Doc_id,Pat_id,date,time) VALUES(%s , %s ,%s, %s )" ,(Doc_id,session['Pat_id'],date, time))
            cur.execute(" SELECT * FROM docapt WHERE date = %s", [date])
            data = cur.fetchall()
            mysql.connection.commit()
            
        # to handle exceptions
        except Exception  as e:
            flash("Try again!!")
            return render_template('uappt.html',msg=e)
       
        return render_template('uappt.html', data=data)
        cur.close()
    return render_template('uappt.html')
#-------------------------------------------------------------------------------------------------------
#Business Man
#home
@app.route('/logenter/ehome')
def ehome():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        return render_template('ehome.html', name=session['Name'])
    # User is not loggedin redirect to login page
    return redirect(url_for('logenter'))


#profile
@app.route('/logenter/eprofile')
def eprofile():
    # Check if user is loggedin
    if 'loggedin' in session:
        # We need all the account info for the user so we can display it on the profile page
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM Retailer WHERE licence= %s', [session['licence']])
        username = cursor.fetchone()
        # Show the profile page with account info
        return render_template('eprofile.html', username=username)
    # User is not loggedin redirect to login page
    return redirect(url_for('logenter'))

#logout
@app.route('/logenter/elogout')
def elogout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('licence', None)
   session.pop('Name', None)
   # Redirect to login page
   return redirect(url_for('logenter'))

#update profile
@app.route('/logenter/eupdate.html', methods=['GET', 'POST'])
def eupdate():
    msg = ""
    if request.method == "POST":
        details = request.form
        # Doc_id = details['Doc_id']
        # Passwd = details['Passwd']
        Name = details['Name']
        Address = details['Address']
        owner = details['owner']
        passwd= details['passwd']
        # Clinic = details['Clinic']
        # Patient_id = details['Patient_id']
        cur = mysql.connection.cursor()
        try:
            cur.execute("UPDATE Retailer  SET  Name = %s , Address = %s, owner = %s,  passwd = %s  WHERE licence = %s",(Name,Address,owner,passwd,[session['licence']]))
            mysql.connection.commit()
            flash("Updated!! Please Log In Again")
        except Exception as e:
            flash(e)
            return render_template('eupdate.html',msg=e)
            
        cur.close()

    return render_template('eupdate.html')

# to check alternative medicine
@app.route('/eprofile/esearch', methods=['GET', 'POST'])
def esearch():
    if request.method == "POST":
        Disease = request.form['Disease']
        # search by Disease
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM Drugs WHERE Disease = %s", [Disease])
        data = cur.fetchall()
        #  the search box will return no  tuples if nothing is entered else it shows error
        if len(data) == 0: 
            flash("Something Went Wrong. Please try again")
            mysql.connection.commit()
        return render_template('esearch.html', data = data)
           
    return render_template('esearch.html')   



# to update the stocks 

@app.route('/eprofile/stock',methods=['GET', 'POST'])
def stock():
    msg = ""
    if request.method == "POST":
        details = request.form
        Shop_id = details['Shop_id']
        Drug = details['Drug']
        price = details['price']
        quantity = details['quantity']
        cur = mysql.connection.cursor()
        try:
            cur.execute("INSERT INTO  Stock (Shop_id, Drug ,price, quantity) VALUES (%s,%s,%s,%s)", (Shop_id,Drug,price,quantity))
            mysql.connection.commit()
            flash("Updated!!")
        except Exception as e:
            flash(" Error !!!Please check the details again")
        
        cur.close()
        return render_template('stock.html')
        
    return render_template('stock.html')


# to display the inventory / stocks
@app.route('/eprofile/inventory', methods=['GET', 'POST'])
def inventory():
    if request.method == "POST":
        Drug = request.form['Drug']
        # search by Drug name
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM Stock WHERE Drug = %s", [Drug])
        data = cur.fetchall()
        #  the search box will return no  tuples if nothing is entered else it shows error
        if Drug=='all' or len(data)==0:
             cur.execute("SELECT * from Stock")
             data = cur.fetchall()
             flash("Displaying entire Inventory")
        mysql.connection.commit()
        return render_template('inventory.html', data = data)
           
    return render_template('inventory.html')   


if __name__ == "__main__":
    app.run()
