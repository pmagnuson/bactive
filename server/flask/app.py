from flask import Flask, redirect, render_template, url_for
from flask_admin import Admin
from flask_admin import helpers as admin_helpers
from flask_admin.contrib.sqla import ModelView
from flask_security import current_user, Security, SQLAlchemyUserDatastore, UserMixin
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from database import db_session, init_db
from models import User, Role

# Instantiate the Flask application with configurations
app = Flask(__name__)
# Configure a specific Bootswatch theme
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
# app.run(debug=True)
# app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
# secret key for sessions
app.config[
    'SECRET_KEY'] = b"T\xb6\x84\x086\x9aQY\xe2\xa8\x0b.\xd2L\xdb,\xd0H\xe2u\xc0w'adc\x1d\xd9\xbdJ\xda\xdb}\x16KU{\x8d\xd0\xcf\x86\x92'\xdb\xc0u\xa8D\xacc\xb2\x0c\x7fki\x02\xe0\xdd\x00\xa3L\x98g\x88"
app.config['SECURITY_PASSWORD_SALT'] = b">'\x1c-\x150!cR\xcc\xeb\x10\xf2\xba\x95\xb9\x05\xa5\x1e~\xa1\x1f#\x1c\xf9\xec\x88\x9d\x17\xb9\x1e\xad"
# Configure application to route to the Flask-Admin index view upon login
app.config['SECURITY_POST_LOGIN_VIEW'] = '/admin/'
# Configure application to route to the Flask-Admin index view upon logout
app.config['SECURITY_POST_LOGOUT_VIEW'] = '/admin/'
# Configure application to route to the Flask-Admin index view upon registering
app.config['SECURITY_POST_REGISTER_VIEW'] = '/admin/'
app.config['SECURITY_REGISTERABLE'] = True
# Configure application to not send an email upon registration
app.config['SECURITY_SEND_REGISTER_EMAIL'] = False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://localhost/flask-admin-flask-security-db'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://dbadmin:Nam0Buddha!a@db:5432'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://dbadmin:Nam0Buddha!a@127.0.0.1:5432'

# Instantiate the database
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class UserModelView(ModelView):
    def is_accessible(self):
        return (current_user.is_active and
                current_user.is_authenticated)

    def _handle_view(self, name):
        if not self.is_accessible():
            return redirect(url_for('security.login'))

    column_list = ['email', 'password', 'roles']


# Create a datastore and instantiate Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

# Create the tables for the users and roles and add a user to the user table
# This decorator registers a function to be run before the first request to the app
#  i.e. calling localhost:5000 from the browser
@app.before_first_request
def create_user():
    init_db()
    user_datastore.create_user(email='admin', password='admin')
    user_datastore.create_role(name='admin', description='global admin access')
    user_datastore.create_role(
        name='sanghaAdmin', description='admin access for one Sangha')
    db.session.commit()


# Instantiate Flask-Admin
admin = Admin(app, name='Admin',
              #   base_template='my_master.html',
              template_mode='bootstrap3')


# Add administrative views to Flask-Admin
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Role, db.session))

# Add the context processor
@security.context_processor
def security_context_processor():
    return dict(
        admin_base_template=admin.base_template,
        admin_view=admin.index_view,
        get_url=url_for,
        h=admin_helpers
    )

# Define the index route
@app.route('/')
def index():
    return render_template('index.html')


if __name__ == "__main__":
    app.run()
