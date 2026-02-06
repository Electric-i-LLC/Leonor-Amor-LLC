from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, IntegerField, FloatField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

from app.models import User

class RegistrationForm(FlaskForm):
    #phone = StringField('Phone (optional)',
    #                       validators=[Length(min=10, max=16)])
    email = StringField('Email',
                        validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    # def validate_phone(self, phone):
    #    user = User.query.filter_by(phone=phone.data).first()
    #    if user:
    #        raise ValidationError('That phone is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')


class RequestResetForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. You must register first.')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')




class CategoryForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    submit = SubmitField('Submit')


# class UserForm(FlaskForm):
#    submit = SubmitField('Submit')


class MessageCreateForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])

    email = StringField('Recipient (Email)', validators=[DataRequired(), Email()])
    submit = SubmitField('Send')

class ProductCreateForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    refund_policy = TextAreaField('Refund Policy', validators=[DataRequired()])

    price = FloatField('Price', validators=[DataRequired()])
    supply = IntegerField('Supply', validators=[])
    # pending = FloatField('Pending', validators=[])

    length = FloatField('Length (inches)', validators=[DataRequired()])
    width = FloatField('Width (inches)', validators=[DataRequired()])
    height = FloatField('Height (inches)', validators=[DataRequired()])
    weight = FloatField('Weight (pounds)', validators=[DataRequired()])

    picture_1 = FileField('Picture 1', validators=[FileAllowed(['jpg', 'png', 'jpeg']), DataRequired()])
    picture_2 = FileField('Picture 2', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    picture_3 = FileField('Picture 3', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    picture_4 = FileField('Picture 4', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    picture_5 = FileField('Picture 5', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    picture_6 = FileField('Picture 6', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    picture_7 = FileField('Picture 7', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    picture_8 = FileField('Picture 8', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    picture_9 = FileField('Picture 9', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    video = FileField('Video', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])

    quantity_in_box = IntegerField('Quantity in a box', validators=[])
    request = StringField('Request (Y/N)', validators=[DataRequired()])

    category = StringField('Category', validators=[DataRequired()])
    submit = SubmitField('Create')

class ProductEditForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    refund_policy = TextAreaField('Refund Policy', validators=[DataRequired()])

    price = FloatField('Price', validators=[DataRequired()])
    supply = IntegerField('Supply', validators=[])
    # pending = FloatField('Pending', validators=[])

    length = FloatField('Length (inches)', validators=[DataRequired()])
    width = FloatField('Width (inches)', validators=[DataRequired()])
    height = FloatField('Height (inches)', validators=[DataRequired()])
    weight = FloatField('Weight (pounds)', validators=[DataRequired()])

    picture_1 = FileField('Picture 1', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    picture_2 = FileField('Picture 2', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    picture_3 = FileField('Picture 3', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    picture_4 = FileField('Picture 4', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    picture_5 = FileField('Picture 5', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    picture_6 = FileField('Picture 6', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    picture_7 = FileField('Picture 7', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    picture_8 = FileField('Picture 8', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    picture_9 = FileField('Picture 9', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    video = FileField('Video', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])

    quantity_in_box = IntegerField('Quantity in a box', validators=[])
    request = StringField('Request (Y/N)', validators=[])
    active = StringField('Active (Y/N)', validators=[DataRequired()])

    category = StringField('Category', validators=[DataRequired()])
    submit = SubmitField('Publish')


class ShippingCalculateForm(FlaskForm):
    length = FloatField('Length (inches)', validators=[DataRequired()])
    width = FloatField('Width (inches)', validators=[DataRequired()])
    height = FloatField('Height (inches)', validators=[DataRequired()])
    weight = FloatField('Weight (pounds)', validators=[DataRequired()])

    name = StringField('First & Last Name', validators=[DataRequired()])
    street1 = StringField('Street 1', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    state = StringField('State', validators=[DataRequired()])
    zipcode = StringField('Zipcode', validators=[DataRequired()])
    country = StringField('Country', validators=[DataRequired()])

    company = StringField('Company (Optional)', validators=[])
    email = StringField('Email (Optional)', validators=[])
    phone = StringField('Phone (Optional)', validators=[])
    street2 = StringField('Street 2 (Optional)', validators=[])
    street3 = StringField('Street 3 (Optional)', validators=[])
    street_no = StringField('Street No# (Optional)', validators=[])


    submit = SubmitField('Calculate shipping')

    def validate_country(self, country):
        if len(country.data) != 2:
            raise ValidationError('Country must be a 2 digit code. Example: (US)')


class ContactForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    selection = SelectField('Reasoning for message', choices=[('request', 'Request event planning'), ('questions', 'General questions'), ('help', 'Technical help')])

    message = TextAreaField('Message', validators=[DataRequired()])

    picture_1 = FileField('Picture 1 (optional)', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    picture_2 = FileField('Picture 2 (optional)', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    picture_3 = FileField('Picture 3 (optional)', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    
    submit = SubmitField('Send Message')


class CartForm(FlaskForm):
    product = IntegerField('Product', validators=[DataRequired()])
    quantity = IntegerField('Quantity', validators=[DataRequired()])
    notes = TextAreaField('Notes (optional)', validators=[])

    submit = SubmitField('Update')

class DeleteCartForm(FlaskForm):
    product = IntegerField('Product', validators=[DataRequired()])
    submit = SubmitField('Delete')


class CheckoutAddressForm(FlaskForm):
    #length = FloatField('Length', validators=[DataRequired()])
    #width = FloatField('Width', validators=[DataRequired()])
    #height = FloatField('Height', validators=[DataRequired()])
    #weight = FloatField('Weight', validators=[DataRequired()])

    first_name = StringField('First name *', validators=[DataRequired()])
    last_name = StringField('Last name *', validators=[DataRequired()])
    street1 = StringField('Street *', validators=[DataRequired()])
    city = StringField('City *', validators=[DataRequired()])
    state = StringField('State *', validators=[DataRequired()])
    zipcode = StringField('Zipcode *', validators=[DataRequired()])
    country = StringField('Country *', validators=[DataRequired()])

    company = StringField('Company (Optional)', validators=[])
    email = StringField('Email *', validators=[DataRequired()])
    phone = StringField('Phone (Optional)', validators=[])
    street2 = StringField('Street 2 (Optional)', validators=[])
    street3 = StringField('Street 3 (Optional)', validators=[])
    street_no = StringField('No #', validators=[])


    submit = SubmitField('Choose shipping')

    def validate_country(self, country):
        if len(country.data) != 2:
            raise ValidationError('Country must be a 2 digit code. Example: (US)')

class CheckoutShippingForm(FlaskForm):
    product = IntegerField('Product', validators=[DataRequired()])
    quantity = IntegerField('Quantity', validators=[DataRequired()])
    shipping = StringField('Shipping Option', validators=[DataRequired()])

    notes = TextAreaField('Notes (optional)', validators=[])
    submit = SubmitField('Select')

'''
class CategoryCreateForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField("Description", validators=[DataRequired()])
    refund_policy = TextAreaField('Refund Policy', validators=[])

    picture_1 = FileField('Picture 1', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    picture_2 = FileField('Picture 2', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    picture_3 = FileField('Picture 3', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    picture_4 = FileField('Picture 4', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    picture_5 = FileField('Picture 5', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    picture_6 = FileField('Picture 6', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    picture_7 = FileField('Picture 7', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    picture_8 = FileField('Picture 8', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    picture_9 = FileField('Picture 9', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    # video = FileField('Picture 9', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])

    supply = IntegerField('Supply', validators=[DataRequired()])
    price = FloatField('Price', validators=[DataRequired()])

    length = FloatField('Length', validators=[DataRequired()])
    width = FloatField('Width', validators=[DataRequired()])
    height = FloatField('Height', validators=[DataRequired()])
    weight = FloatField('Weight', validators=[DataRequired()])

    quantity_in_box = IntegerField('Quantity in a box', validators=[DataRequired()])





    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
    '''


class GalleryForm(FlaskForm):
    title = TextAreaField('Title', validators=[DataRequired()])
    description = TextAreaField('Description (optional)', validators=[])

    picture_1 = FileField('Picture 1', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    
    submit = SubmitField('Upload Photo')