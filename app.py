from flask import Flask,url_for,redirect,request
from flask_sqlalchemy import SQLAlchemy
import os
import jinja2
from sqlalchemy import Column, Integer, String, ForeignKey, Date
from config import Config

app = Flask(__name__)

# Initial db
db = SQLAlchemy(app)

# Config app
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:123456@localhost:5432/DatabaseForReStudy'
app.config['SQLALCHEMY_ECHO'] = True

# Create dummy secret key sp we can use sessions
app.config['SECRET_KEY'] = 'secret_key'

# Implement direct mock
template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja2_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir))


# Class ORM
class TableUser(db.Model):
	__tabelname__ = "tblUser"
	id = db.Column('id', Integer, primary_key=True, nullable=False)
	user_name = db.Column('user_name', String, nullable=False)
	email = db.Column('email', String)


class ProcessBussiness():
    @staticmethod
    def get_all_user():
        try:
            conn = Config.connect()
            users = conn.query(TableUser).all()
            return users
        except Exception as identifier:
            print(identifier)
        finally:
            conn.close()
        
    @staticmethod
    def create_user(user):
        try:
            conn = Config.connect()
            conn.add(user)
            conn.commit()
            return True
        except Exception as identifier:
            print(identifier)
        finally:
            conn.close()
        
        
       
    
    @staticmethod
    def delete_user(id):
        try:
            conn = Config.connect()
            user = conn.query(TableUser).filter(TableUser.id == id).first()
            conn.delete(user)
            conn.commit()
            return True
        except Exception as identifier:
            print(identifier)
        finally:
            conn.close()

    @staticmethod
    def update_user(user):
        try:
            conn = Config.connect()
            userdb = conn.query(TableUser).filter(TableUser.id == user.id).first()
            userdb.user_name = user.user_name
            userdb.email = user.email
            conn.commit()
            return True
        except Exception as identifier:
            print(identifier)
        finally:
            conn.close()
       

    @staticmethod
    def get_user_by_id(id):
        try:
            conn = Config.connect()
            user =  conn.query(TableUser).filter(TableUser.id == id).first()
            return user
        except Exception as identifier:
            print(identifier)
        finally:
            conn.close()
        
        

class NavigationWeb():
    @staticmethod
    @app.route('/hello-world')
    def hello_world():
        return 'Hello world'

    @staticmethod
    @app.route('/', methods=['GET'])
    def index():
        users = ProcessBussiness.get_all_user()
        template = jinja2_env.get_template('home.html')
        output = template.render(users=users)
        return output

    @staticmethod
    @app.route('/create-user', methods=['GET', 'POST'])
    def create_user():

        if request.method == 'POST':
            user = TableUser()
            user.user_name = request.form['username']
            user.email = request.form['email']
            ProcessBussiness.create_user(user)
            return redirect(url_for('index'))
        else:
            template = jinja2_env.get_template('create_user.html')
            return template.render(user=None)

    @staticmethod
    @app.route('/delete-user/<id>')
    def delete_user(id):
        ProcessBussiness.delete_user(id)
        return redirect(url_for('index'))

    @staticmethod
    @app.route('/update-user/<id>', methods=['GET', 'POST'])
    def update_user(id):
        if request.method == 'POST':
            user = TableUser()
            user.id = id
            user.user_name = request.form['username']
            user.email = request.form['email']
            ProcessBussiness.update_user(user)
            return redirect(url_for('index'))
        else:
            user = ProcessBussiness.get_user_by_id(id)
            template = jinja2_env.get_template('create_user.html')
            return template.render(user=user)


if __name__ == "__main__":
    # Create database
    db.create_all()

    # Hello world
    print ("hello world")
    # Run app
    app.run(debug=True)