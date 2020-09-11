from flask import Flask, render_template, flash, redirect, url_for, session, request, send_file
from flask_mysqldb import MySQL
from wtforms import Form,SelectField, StringField, PasswordField, DateField, IntegerField, TextAreaField, validators
from functools import wraps
import pandas as pd
from io import BytesIO
import csv

app = Flask(__name__)
app.secret_key='secret1234'


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'test'
app.config['MYSQL_DB'] = 'dataentry'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

   



class RegisterForm(Form):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    password = PasswordField('Password',[
    validators.DataRequired(),
    validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password')





# User Login
@app.route('/', methods=['GET','POST'])
def login():
    if request.method == 'POST':
      # get from fields
      username = request.form['username']
      password_candidate = request.form['password']


      # create cursor 
      cur = mysql.connection.cursor()

      # Get user by username
      result = cur.execute("SELECT * FROM users WHERE username = %s",[username])

      if result > 0:
          # Get Stored hash
          data = cur.fetchone()
          password = data['password']

          #compare the passwords
          if (password_candidate == password):
            # Passed
            session['logged_in'] = True
            session['username'] = username

            flash('You are now logged in', 'success')
            return redirect(url_for('dataentry'))
          else:
                error = 'Invalid login'
                return render_template('home.html', error=error )
            #close connection
          cur.close()
      else:
            error = 'Username not found'
            return render_template('home.html', error=error )

    return render_template('home.html')

#Check if user logged in
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login', 'danger')
            return redirect(url_for('login'))
    return wrap

#Logout
@app.route('/logout')
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('login'))

class DataentryFormTV(Form):
    date = DateField('Date', [validators.DataRequired()],format='%Y-%m-%d')
    name_of_channel = SelectField('Name of the channel', [validators.DataRequired(), validators.Length(min=1, max=500)], choices=[('None', 'Please select an option'), ('NDTV', 'NDTV 24*7'),('Republic TV', 'Republic TV'), ('3', '...'), ('4', '....'),
    ('5', '...'),('6', '...'),('7', '...'),('8', '...')], default= None)
    name_of_the_programme = StringField('Name of the Programme', [validators.DataRequired(), validators.Length(min=1, max=300)])
    prime_time_slot = StringField('Prime time Slot',[validators.DataRequired(), validators.Length(min=1, max=300)])
    name_of_anchor = StringField('Name of Anchor', [validators.Length(min=0, max=500)])
    gender_of_anchor = StringField([validators.Length(min=1, max=100)])
   
    topic = SelectField('Topic', choices=[('None',' Please select an option'),('1', '...'),('2', '...'), ('3', '...'), ('4', '....'),
    ('5', '...'),('6', '...'),('7', '...'),('8', '...'),('9', '...'),('10', '...'),('11', '...'),('12', '...'),('13', '...'),('14', '...'),('15', '...')], default=None)

    topic1 = SelectField('Topic1:', choices=[('None', 'Please select an option'),('1', '...'),('2', '...'), ('3', '...'), ('4', '....'),
    ('5', '...'),('6', '...'),('7', '...'),('8', '...'),('9', '...'),('10', '...'),('11', '...'),('12', '...'),('13', '...'),('14', '...'),('15', '...')], default=None)

    topic2 = SelectField('Topic2:', choices=[('None','Please select an option'), ('1', '...'),('2', '...'), ('3', '...'), ('4', '....'),
    ('5', '...'),('6', '...'),('7', '...'),('8', '...'),('9', '...'),('10', '...'),('11', '...'),('12', '...'),('13', '...'),('14', '...'),('15', '...')], default=None)

    topic3 = SelectField('Topic3:', choices=[('None','Please select an option'), ('1', '...'),('2', '...'), ('3', '...'), ('4', '....'),
    ('5', '...'),('6', '...'),('7', '...'),('8', '...'),('9', '...'),('10', '...'),('11', '...'),('12', '...'),('13', '...'),('14', '...'),('15', '...')], default=None)

    topic4 = SelectField('Topic4:', choices=[('None', 'Please select an option'),('1', '...'),('2', '...'), ('3', '...'), ('4', '....'),
    ('5', '...'),('6', '...'),('7', '...'),('8', '...'),('9', '...'),('10', '...'),('11', '...'),('12', '...'),('13', '...'),('14', '...'),('15', '...')], default=None)

    topic5 = SelectField('Topic5:', choices=[('None', 'Please select an option'),('1', '...'),('2', '...'), ('3', '...'), ('4', '....'),
    ('5', '...'),('6', '...'),('7', '...'),('8', '...'),('9', '...'),('10', '...'),('11', '...'),('12', '...'),('13', '...'),('14', '...'),('15', '...')], default=None)

    name_of_panellist = StringField('Name of Panellist', [validators.Length(min=0, max=500)])
    gender_of_panellist = StringField([validators.Length(min=1, max=100)])
    field_of_panellist = SelectField('Field of Panellist', choices=[('None','Please select an option'),('1', '...'),('2', '...'), ('3', '...'), ('4', '....'),
    ('5', '...'),('6', '...'),('7', '...'),('8', '...'),('9', '...'),('10', '...')], default=None)
    name_of_person_entering_data = StringField('Name of person entering data', [validators.Length(min=0, max=100)])
    comments = TextAreaField('Comments', [validators.Length(min=0, max=400)])

class DataentryFormNewspaper(Form):
    date = DateField('Date',[validators.DataRequired()], format='%Y-%m-%d')
    name_of_newspaper = SelectField('Name of Newspaper', [validators.DataRequired(), validators.Length(min=1, max=500)], choices=[('None', 'Please select an option'), ('Indian Express', 'Indian Express'),('Times of India', 'Times of India'), ('3', '...'), ('4', '....'),
    ('5', '...'),('6', '...'),('7', '...'),('8', '...')], default= None)
    pageNO = IntegerField('Page Number', [validators.DataRequired()])
    page_title = StringField('Page Title',[validators.Length(min=0, max=300)])
    name_of_journalist = StringField('Name of Journalist', [validators.Length(min=0, max=500)])
    gender_of_journalist = StringField([validators.Length(min=1, max=100)])

    topic = SelectField('Topic', choices=[('None',' Please select an option'),('1', '...'),('2', '...'), ('3', '...'), ('4', '....'),
    ('5', '...'),('6', '...'),('7', '...'),('8', '...'),('9', '...'),('10', '...'),('11', '...'),('12', '...'),('13', '...'),('14', '...'),('15', '...')], default=None)

    topic1 = SelectField('Topic1:', choices=[('None', 'Please select an option'),('1', '...'),('2', '...'), ('3', '...'), ('4', '....'),
    ('5', '...'),('6', '...'),('7', '...'),('8', '...'),('9', '...'),('10', '...'),('11', '...'),('12', '...'),('13', '...'),('14', '...'),('15', '...')], default=None)

    topic2 = SelectField('Topic2:', choices=[('None','Please select an option'), ('1', '...'),('2', '...'), ('3', '...'), ('4', '....'),
    ('5', '...'),('6', '...'),('7', '...'),('8', '...'),('9', '...'),('10', '...'),('11', '...'),('12', '...'),('13', '...'),('14', '...'),('15', '...')], default=None)

    topic3 = SelectField('Topic3:', choices=[('None','Please select an option'), ('1', '...'),('2', '...'), ('3', '...'), ('4', '....'),
    ('5', '...'),('6', '...'),('7', '...'),('8', '...'),('9', '...'),('10', '...'),('11', '...'),('12', '...'),('13', '...'),('14', '...'),('15', '...')], default=None)

    topic4 = SelectField('Topic4:', choices=[('None', 'Please select an option'),('1', '...'),('2', '...'), ('3', '...'), ('4', '....'),
    ('5', '...'),('6', '...'),('7', '...'),('8', '...'),('9', '...'),('10', '...'),('11', '...'),('12', '...'),('13', '...'),('14', '...'),('15', '...')], default=None)

    topic5 = SelectField('Topic5:', choices=[('None', 'Please select an option'),('1', '...'),('2', '...'), ('3', '...'), ('4', '....'),
    ('5', '...'),('6', '...'),('7', '...'),('8', '...'),('9', '...'),('10', '...'),('11', '...'),('12', '...'),('13', '...'),('14', '...'),('15', '...')], default=None)

    name_of_person_entering_data = StringField('Name of person entering data', [validators.Length(min=0, max=100)])
    comments = TextAreaField('Comments', [validators.Length(min=0, max=400)])





    

# Data Entry  
@app.route('/dataentry', methods=['GET', 'POST'])
@is_logged_in
def dataentry():
    form = DataentryFormTV(request.form)
    if request.method == 'POST' and form.validate():
        date = form.date.data
        name_of_channel = form.name_of_channel.data
        name_of_the_programme = form.name_of_the_programme.data
        prime_time_slot = form.prime_time_slot.data
        name_of_anchor = form.name_of_anchor.data 
        gender_of_anchor = request.form.get('gender_of_anchor')
        topic = form.topic.data
        topic1 = form.topic1.data
        topic2 = form.topic2.data
        topic3 = form.topic3.data
        topic4 = form.topic4.data
        topic5 = form.topic5.data
        name_of_panellist = form.name_of_panellist.data
        gender_of_panellist = request.form.get('gender_of_panellist')
        field_of_panellist = form.field_of_panellist.data
        name_of_person_entering_data = form.name_of_person_entering_data.data 
        comments = form.comments.data


        #create cursor
        cur = mysql.connection.cursor()
        
        #Execute Query
        cur.execute("INSERT INTO tv(date, name_of_channel, name_of_the_programme, prime_time_slot, name_of_anchor, gender_of_anchor, topic, topic1, topic2, topic3, topic4, topic5, name_of_panellist, gender_of_panellist, field_of_panellist, name_of_person_entering_data, comments)  VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (date, name_of_channel, name_of_the_programme, prime_time_slot, name_of_anchor, gender_of_anchor, topic, topic1, topic2, topic3, topic4, topic5, name_of_panellist, gender_of_panellist, field_of_panellist, name_of_person_entering_data, comments ))

        # Commit to DB
        mysql.connection.commit()

        flash('Data Entered', 'success')

        return redirect(url_for('dataentry'))

    return render_template('dataentry.html', form = form ) 

@app.route('/newspaper',methods=['GET', 'POST'] )
@is_logged_in
def newspaper():
    form = DataentryFormNewspaper(request.form)
    if request.method == 'POST' and form.validate():
        date = form.date.data
        name_of_newspaper = form.name_of_newspaper.data
        pageNO = form.pageNO.data
        page_title = form.page_title.data
        name_of_journalist = form.name_of_journalist.data 
        gender_of_journalist = request.form.get('gender_of_journalist')
        topic = form.topic.data
        topic1 = form.topic1.data
        topic2 = form.topic2.data
        topic3 = form.topic3.data
        topic4 = form.topic4.data
        topic5 = form.topic5.data
        name_of_person_entering_data = form.name_of_person_entering_data.data 
        comments = form.comments.data


        #create cursor
        cur = mysql.connection.cursor()
        
        #Execute Query
        cur.execute("INSERT INTO newspaper(date, name_of_newspaper, pageNO, page_title, name_of_journalist, gender_of_journalist, topic, topic1, topic2, topic3, topic4, topic5, name_of_person_entering_data, comments)  VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (date, name_of_newspaper, pageNO, page_title, name_of_journalist, gender_of_journalist, topic, topic1, topic2, topic3, topic4, topic5, name_of_person_entering_data, comments))

        # Commit to DB
        mysql.connection.commit()

        flash('Data Entered', 'success')

        return redirect(url_for('newspaper'))

    return render_template('newspaper.html', form = form ) 

# Dashboard
@app.route('/dashboard')   
@is_logged_in
def dashboard():  

    cur = mysql.connection.cursor()

    cur.execute("SELECT * FROM tv")

    tv = cur.fetchall()

    return render_template('dashboard.html',tv=tv)

@app.route('/dashboardnewspaper')   
@is_logged_in
def dashboardnewspaper():  

    cur = mysql.connection.cursor()

    cur.execute("SELECT * FROM newspaper")

    newspaper = cur.fetchall()

    return render_template('dashboard_news.html',newspaper=newspaper)

# Edit TV Entry
@app.route('/edit_entry/<string:id>', methods=['GET','POST'])
def edit_entry(id):
    
    cur = mysql.connection.cursor()

    #Get entry by id 
    result = cur.execute("SELECT * FROM tv WHERE id = %s", [id])

    row = cur.fetchone()
    cur.close()

    form = DataentryFormTV(request.form) 
    
    form.date.data = row['date']
    form.name_of_channel.data = row['name_of_channel']
    form.name_of_the_programme.data = row['name_of_the_programme']
    form.prime_time_slot.data = row['prime_time_slot']
    form.name_of_anchor.data = row['name_of_anchor']
    form.gender_of_anchor.data = row['gender_of_anchor']
    form.topic.data = row['topic']
    form.topic1.data = row['topic1']
    form.topic2.data = row['topic2']
    form.topic3.data = row['topic3']
    form.topic4.data = row['topic4']
    form.topic5.data = row['topic5']
    form.name_of_panellist.data = row['name_of_panellist']
    form.gender_of_panellist.data = row['gender_of_panellist']
    form.field_of_panellist.data = row['field_of_panellist']
    form.name_of_person_entering_data.data  = row['name_of_person_entering_data']
    form.comments.data = row['comments']
    
    
        
    if request.method == 'POST' and form.validate():
            date = request.form['date']
            name_of_channel = request.form['name_of_channel']
            name_of_the_programme = request.form['name_of_the_programme']
            prime_time_slot = request.form['prime_time_slot']
            name_of_anchor = request.form['name_of_anchor']
            gender_of_anchor = request.form.get('gender_of_anchor')
            topic = request.form['topic']
            topic1 = request.form['topic1']
            topic2 = request.form['topic2']
            topic3 = request.form['topic3']
            topic4 = request.form['topic4']
            topic5 = request.form['topic5']
            name_of_panellist = request.form['name_of_panellist']
            gender_of_panellist = request.form.get('gender_of_panellist')
            field_of_panellist = request.form['field_of_panellist']
            name_of_person_entering_data = request.form['name_of_person_entering_data']
            comments = request.form['comments']

        
            cur = mysql.connection.cursor()

            cur.execute("UPDATE tv SET date= %s, name_of_channel= %s, name_of_the_programme=%s, prime_time_slot=%s, name_of_anchor=%s, gender_of_anchor=%s, topic=%s, topic1=%s, topic2=%s, topic3=%s, topic4=%s, topic5=%s, name_of_panellist=%s, gender_of_panellist=%s, field_of_panellist=%s, name_of_person_entering_data=%s, comments=%s WHERE id=%s",(date, name_of_channel, name_of_the_programme, prime_time_slot, name_of_anchor, gender_of_anchor, topic, topic1, topic2, topic3, topic4, topic5, name_of_panellist, gender_of_panellist, field_of_panellist, name_of_person_entering_data, comments,id))

            mysql.connection.commit()

            cur.close()

            flash('entry Updated', 'success')

            return redirect(url_for('dashboard'))

    return render_template('edit_entry.html', form = form)

 # Edit Newspaper Entry
@app.route('/edit_entry_news/<string:id>', methods=['GET','POST'])
def edit_entry_news(id):
    
    cur = mysql.connection.cursor()

    #Get entry by id 
    result = cur.execute("SELECT * FROM newspaper WHERE id = %s", [id])

    row = cur.fetchone()
    cur.close()

    form = DataentryFormNewspaper(request.form) 
    
    form.date.data = row['date']
    form.name_of_newspaper.data = row['name_of_newspaper']
    form.pageNO.data = row['pageNO']
    form.page_title.data = row['page_title']
    form.name_of_journalist.data = row['name_of_journalist']
    form.gender_of_journalist.data = row['gender_of_journalist']
    form.topic.data = row['topic']
    form.topic1.data = row['topic1']
    form.topic2.data = row['topic2']
    form.topic3.data = row['topic3']
    form.topic4.data = row['topic4']
    form.topic5.data = row['topic5']
    form.name_of_person_entering_data.data  = row['name_of_person_entering_data']
    form.comments.data = row['comments']
    
    
        
    if request.method == 'POST' and form.validate():
            date = request.form['date']
            name_of_newspaper = request.form['name_of_newspaper']
            pageNO = request.form['pageNO']
            page_title = request.form['page_title']
            name_of_journalist = request.form['name_of_journalist']
            gender_of_journalist = request.form.get('gender_of_journalist')
            topic = request.form['topic']
            topic1 = request.form['topic1']
            topic2 = request.form['topic2']
            topic3 = request.form['topic3']
            topic4 = request.form['topic4']
            topic5 = request.form['topic5']
            name_of_person_entering_data = request.form['name_of_person_entering_data']
            comments = request.form['comments']

        
            cur = mysql.connection.cursor()

            cur.execute("UPDATE newspaper SET date= %s, name_of_newspaper= %s, pageNO=%s, page_title=%s, name_of_journalist=%s, gender_of_journalist=%s, topic=%s, topic1=%s, topic2=%s, topic3=%s, topic4=%s, topic5=%s, name_of_person_entering_data=%s, comments=%s WHERE id=%s",(date, name_of_newspaper, pageNO, page_title, name_of_journalist, gender_of_journalist, topic, topic1, topic2, topic3, topic4, topic5, name_of_person_entering_data, comments,id))

            mysql.connection.commit()

            cur.close()

            flash('entry Updated', 'success')

            return redirect(url_for('dashboardnewspaper'))

    return render_template('edit_entry_news.html', form = form)
   

# Delete TV Entry
@app.route('/delete_entry/<string:id>', methods=['POST'])

def delete_entry(id):

    cur = mysql.connection.cursor()

    cur.execute("DELETE FROM tv WHERE id=%s", [id])

    mysql.connection.commit()

    cur.close()

    flash('Entry Deleted','success')

    return redirect(url_for('dashboard'))

# Delete Newspaper Entry
@app.route('/delete_entry_news/<string:id>', methods=['POST'])

def delete_entry_news(id):

    cur = mysql.connection.cursor()

    cur.execute("DELETE FROM newspaper WHERE id=%s", [id])

    mysql.connection.commit()

    cur.close()

    flash('Entry Deleted','success')

    return redirect(url_for('dashboardnewspaper'))

# Download TV entries
@app.route('/download')
@is_logged_in

def download():


    cur = mysql.connection.cursor()

    cur.execute("SELECT * FROM tv")
    

    columns = [desc[0] for desc in cur.description]
    tv = cur.fetchall()
    df = pd.DataFrame(list(tv), columns=columns)

    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')  # pylint: disable=abstract-class-instantiated
    df.to_excel(writer, sheet_name='Sheet1')
    writer.save()
    output.seek(0)
    return send_file(output, attachment_filename='output.xlsx', as_attachment=True)


    return redirect(url_for('dashboard'))

    return render_template('dashboard.html',tv=tv)

# Download Newspaper entries
@app.route('/downloadnewspaper')
@is_logged_in

def download_news():


    cur = mysql.connection.cursor()

    cur.execute("SELECT * FROM newspaper")
    

    columns = [desc[0] for desc in cur.description]
    newspaper = cur.fetchall()
    df = pd.DataFrame(list(newspaper), columns=columns)

    
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')  # pylint: disable=abstract-class-instantiated
    df.to_excel(writer, sheet_name='Sheet1')
    writer.save()
    output.seek(0)
    return send_file(output, attachment_filename='output2.xlsx', as_attachment=True) 

    return redirect(url_for('dashboardnewspaper'))

    return render_template('dashboard_news.html',newspaper=newspaper)

if __name__ == ' __main__ ':
    
    app.run(debug=True)