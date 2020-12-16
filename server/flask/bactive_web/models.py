from flask_admin import Admin
from flask_sqlalchemy import SQLAlchemy
from flask_admin.contrib.sqla import ModelView


app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://dbadmin:Nam0Buddha!a@db:5432'
db = SQLAlchemy(app)

roles_users_table = db.Table('roles_users',
                             db.Column('users_id', db.Integer(),
                                       db.ForeignKey('users.id')),
                             db.Column('roles_id', db.Integer(),
                                       db.ForeignKey('roles.id')))


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username


class Roles(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))


admin = Admin(app, name='DSSF Data', template_mode='bootstrap3')
# Add administrative views here
admin.add_view(ModelView(User, db.session))
