from flask import (Flask, render_template, redirect, 
                   url_for)
from form import ContactForm
from flask_ckeditor import CKEditor
import sqlite3
from flaskwebgui import FlaskUI as ui
import os
import sys
import sqlite3

db_path = os.path.join(os.getcwd(), "flask_ckeditor_desktop/message.db")

# conn = sqlite3.connect(db_path)

# conn.execute("""
# CREATE TABLE IF NOT EXISTS message (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     name TEXT,
#     email TEXT,
#     subscribe TEXT,
#     message TEXT
# )
# """)
# conn.commit()

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

app = Flask(
    __name__,
    template_folder=resource_path("templates")
)

app.config['SECRET_KEY'] = 'mysecretkey'
app.config['CKEDITOR_PKG_TYPE'] = 'full-all'

ckeditor = CKEditor(app)
################# Route ##################
@app.route('/')
def index():
    form = ContactForm()
    return render_template('contact.html', form=form)

@app.route('/message', methods=['GET','POST'])
def submit():
    form = ContactForm()
    
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        subscribe = form.subscribe.data
        message = form.message.data
        
        db_path = os.path.join(os.getcwd(), "message.db")
        conn = sqlite3.connect(db_path)
        
        # conn = sqlite3.connect(app.config.get('DATABASE', 'flask_ckeditor/message.db'))
        # conn = sqlite3.connect("flask_ckeditor/message.db")
        c = conn.cursor()
        try:
            query = ("""INSERT INTO message
                        VALUES (:id, :name, :email, :subscribe, :message)""")

            my_data = {
                'id' : None,
                'name': name,
                'email': email,
                'subscribe': subscribe,
                'message': message
                }
         
            content = c.execute(query, my_data)
            conn.commit()

            print(f"Data Added ID: " + str(content.lastrowid))

        except sqlite3.Error as e:
            print(e)
       
        return redirect(url_for('thankyou'))
    
    return render_template('contact.html', form=form)

@app.route('/thankyou')
def thankyou():
    return render_template('thankyou.html')

if __name__ == '__main__':
    # app.run(host='127.0.0.1', port=5000, debug=True)
    ui(app=app, server="flask", width=1000, height=1000).run()
    
# python flask_ckeditor/app.py

'''
pip install pyinstaller
python flask_ckeditor_desktop/app.py

under the powershell
pyinstaller --onefile `
--add-data "flask_ckeditor_desktop\templates;templates" `
--add-data "flask_ckeditor_desktop\message.db;." `
--icon "D:\Learning App\Flask-learning\Flask_ckeditor_desktop\my.ico" `
flask_ckeditor_desktop\app.py

pyinstaller --onefile --noconsole `
--add-data "flask_ckeditor_desktop\templates;templates" `
--add-data "flask_ckeditor_desktop\message.db;." `
--icon "Flask_ckeditor_desktop\my.ico" `
flask_ckeditor_desktop\app.py
'''
