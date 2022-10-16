from app import current_app, db, crypt
import sqlalchemy as sa
from datetime import datetime


class Admin(db.Model):
    __tablename__ = 'admin'
    admin_id = sa.Column(sa.String(255), primary_key=True)
    password = sa.Column(sa.String(60, _warn_on_bytestring=True)) # password size to be 20 max
    logins = db.relationship("UserLogins", backref = 'admin', cascade = 'all, delete-orphan', uselist = True)
    blogs = db.relationship("Blog", backref = 'admin', cascade = 'all, delete-orphan', lazy="dynamic", uselist = True)

    def __init__(self, admin_id, password):
        self.admin_id = admin_id
        self.password = crypt.generate_password_hash(password).decode('utf-8')

    @staticmethod
    def is_admin_user(input_id:str, input_password:str) -> bool:
        '''
        is input_id and input_password match to any of the entries in 
        the database, the user is allowed as admin.

        Parameters:
            input_id: the id of the input
            input_password: the password of the input

        Returns: Boolean indicating whether the user is allowed to access or not.
        '''
        admin_user_object = Admin.query.get(input_id)
        print(admin_user_object)
        if admin_user_object is not None:
            return crypt.check_password_hash(admin_user_object.password, input_password), admin_user_object
        return False, None

class UserLogins(db.Model):
    __tablename__ = 'user_logins'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    # Admin user id is saved here
    admin_id = sa.Column(sa.String(255), db.ForeignKey('admin.admin_id', ondelete = "CASCADE"), nullable=False)
    login_datetime = sa.Column(sa.DateTime, nullable = False)

    def __init__(self, user:Admin):
        admin_id = user.admin_id
        self.login_datetime = datetime.now()

class Blog(db.Model):
    __tablename__ = 'blog'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    # uploading user
    admin_id = sa.Column(sa.String(255), db.ForeignKey('admin.admin_id', ondelete = "CASCADE"), nullable=False)
    heading = sa.Column(sa.Unicode(500), nullable=False)
    body = sa.Column(sa.Unicode(5000), nullable=False)
    image_link = sa.Column(sa.Unicode(1000))
    post_time = sa.Column(sa.DateTime, nullable = False)


    def __init__(self, heading, body, image_link, admin_id):
        self.heading = heading
        self.body = body
        self.admin_id = admin_id
        self.image_link = image_link
        self.post_time = datetime.now()

    def to_dict(self):
        return {
            'id': self.id,
            'heading': self.heading,
            'body': self.body,
            'image_link': self.image_link,
            'post_time': self.post_time,
            "by": self.admin_id
        }

    def update(self, blog_heading, blog_body, blog_image_link):
        
        if self.heading != blog_heading:
            self.heading = blog_heading
        if self.body != blog_body:
            self.body = blog_body
        if self.image_link != blog_image_link:
            self.image_link = blog_image_link


class Join_Requests(db.Model):
    __tablename__ = 'join_requests'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    name = sa.Column(sa.String(255), nullable=False)
    email = sa.Column(sa.String(255), nullable=False)
    number = sa.Column(sa.String(15), nullable=False)
    roll = sa.Column(sa.Integer, nullable=False)
    reviewed = sa.Column(sa.Boolean, nullable=False)
    join_time = sa.Column(sa.DateTime, nullable=False)

    def __init__(self, name, email, number, roll):
        self.email = email
        self.name = name
        self.number = number
        self.roll = roll
        self.reviewed = False
        self.join_time = datetime.now()

    @property
    def to_dict(self):
        return dict(
            id = sel.id, 
            name=self.name,
            email=self.email,
            number=self.number, 
            roll=self.roll, 
            join_request_time = self.join_time
        )

class Contacts(db.Model):
    __tablename__ = 'contacts'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    profession = sa.Column(sa.String(255), nullable=False)
    name = sa.Column(sa.String(255), nullable=False)
    number = sa.Column(sa.String(15), nullable=False)
    field = sa.Column(sa.String(255), nullable=False)
    date_of_contact = sa.Column(sa.DateTime(), nullable=False)

    def __init__(self,profession, name, number, field):
        self.profession = profession
        self.name = name
        self.number = number
        self.field = field
        self.date_of_contact = datetime.now()

    @property
    def to_dict(self):
        return dict(
            id = self.id, 
            profession = self.profession,
            name = self.name,
            number = self.number,
            field = self.field,
            date_of_contact = self.date_of_contact
        )