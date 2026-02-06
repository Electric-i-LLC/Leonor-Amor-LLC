from flask import render_template, url_for, redirect, request, flash, abort, make_response, jsonify
from app import create_app, db, bcrypt, mail

from app.utils import (save_picture, const_hash,  delete_picture, send_email)

from app.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
                             PostForm, RequestResetForm, ResetPasswordForm,
                             CategoryForm, MessageCreateForm, 
                             ProductCreateForm, ProductEditForm,
                             ShippingCalculateForm, ContactForm, CartForm, DeleteCartForm,
                             CheckoutAddressForm, CheckoutShippingForm, GalleryForm)

from app.models import User, Message, Appointment
from flask_login import login_user, current_user, logout_user, login_required
from datetime import datetime
from cryptography.fernet import Fernet  
from sqlalchemy import desc, asc


@create_app.route('/about', methods=['GET', 'POST'])
def about():

    form = ContactForm()

    if form.validate_on_submit():
        email = form.email.data.lower()
        hashed_email = const_hash(email)
        user = User.query.filter_by(email_hash=hashed_email).first()

        key = create_app.config.get('FERNET_KEY')
        fernet = Fernet(key.encode())
        default = 'default.jpg'


        if not user:
            user = User(email=fernet.encrypt(email.encode()).decode(), email_hash=hashed_email,
                    admin=False, profile_picture=fernet.encrypt(default.encode()).decode())

            db.session.add(user)
            db.session.flush()
            db.session.refresh(user)



        message = Message(title=fernet.encrypt(form.selection.data.encode()).decode(), 
                          description=fernet.encrypt(form.message.data.encode()).decode(), 
                          sender=user.id, receiver=int(create_app.config.get('ADMIN_ID')),
                          message_type=fernet.encrypt(form.selection.data.encode()).decode())

        pictures = [None, None, None]
        if form.picture_1.data:
            pictures[0] = save_picture(form.picture_1.data)
            message.gallery_1 = fernet.encrypt(pictures[0].encode()).decode()
        if form.picture_2.data:
            pictures[1] = save_picture(form.picture_2.data)
            message.gallery_2 = fernet.encrypt(pictures[1].encode()).decode()
        if form.picture_3.data:
            pictures[2] = save_picture(form.picture_3.data)
            message.gallery_3 = fernet.encrypt(pictures[2].encode()).decode()


        db.session.add(message)
        db.session.commit()

        if form.selection.data == 'request':
            msg_body = f'''Thank you for inquiring about an event needing to be planned! One of our team members will reach out to you shortly.
Message: {form.message.data}

Sincerely,
    Leonor Amor LLC
'''
            send_email(subject='Event Planning Request', sender='leonoramorllc@gmail.com', recipients=[email], body=msg_body, attachment_1=pictures[0], attachment_2=pictures[1], attachment_3=pictures[2])
        
            msg_body = f'''{email} inquired about a custom order.
Message: {form.message.data}
'''
            send_email(subject='Event Planning Request Received', sender='leonoramorllc@gmail.com', recipients=['leonoramorllc@gmail.com'], body=msg_body, attachment_1=pictures[0], attachment_2=pictures[1], attachment_3=pictures[2])
        
        elif form.selection.data == 'questions':
            msg_body = f'''Thank you for inquiring about a general question! One of our team members will reach out to you shortly.
Message: {form.message.data}

Sincerely,
    Leonor Amor LLC
'''
            send_email(subject='General Question', sender='leonoramorllc@gmail.com', recipients=[email], body=msg_body, attachment_1=pictures[0], attachment_2=pictures[1], attachment_3=pictures[2])
            
            msg_body = f'''{email} inquired about a general question.
Message: {form.message.data}
'''
            send_email(subject='General Question Received', sender='leonoramorllc@gmail.com', recipients=['leonoramorllc@gmail.com'], body=msg_body, attachment_1=pictures[0], attachment_2=pictures[1], attachment_3=pictures[2])
        
        elif form.selection.data == 'help':
            msg_body = f'''Thank you for inquiring about a technical problem! One of our team members will reach out to you shortly.
Message: {form.message.data}

Sincerely,
    Leonor Amor LLC
'''
            send_email('Technical Help/Problem Request', sender='leonoramorllc@gmail.com', recipients=[email], body=msg_body, attachment_1=pictures[0], attachment_2=pictures[1], attachment_3=pictures[2])
            
            msg_body = f'''{email} inquired about a technical problem.
Message: {form.message.data}
'''
            send_email(subject='Technical Help/Problem Request Received', sender='leonoramorllc@gmail.com', recipients=['leonoramorllc@gmail.com'], body=msg_body, attachment_1=pictures[0], attachment_2=pictures[1], attachment_3=pictures[2])

        flash('Inquiry submitted!', 'success')
        return redirect(url_for('about'))

    return render_template('about.html', title='About Us', form=form)
    # return render_template('footer/about.html', title='About Us', cart=cart)


@create_app.route('/', methods=['GET', 'POST'])
@create_app.route('/home', methods=['GET', 'POST'])
@create_app.route('/index', methods=['GET', 'POST'])
def home():
    server_now = datetime.now()

    # For Gallery
    key = create_app.config.get('FERNET_KEY')
    fernet = Fernet(key.encode())

    messages = Message.query.filter_by(message_type='gallery').order_by(desc(Message.created))

   
    return render_template('home.html', title='Home', len=len, messages=messages, fernet=fernet, server_now=server_now.isoformat())





@create_app.route('/register', methods=['GET', 'POST'])
def register():
    # Register in future patch update
    return redirect(url_for('login'))

    if current_user.is_authenticated:
        return redirect(url_for('home'))


    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

        email = form.email.data.lower()
        email_hash = const_hash(email)

        user = User.query.filter_by(email_hash=email_hash).first()        
        if user:
            flash('Email is already registerd', 'danger')
            return redirect(url_for('register'))

        key = create_app.config.get('FERNET_KEY')
        fernet = Fernet(key.encode())

        default = 'default.jpg'
        user = User(email=fernet.encrypt(email.encode()).decode(), email_hash=email_hash, password=hashed_password,
                    admin=True, profile_picture=fernet.encrypt(default.encode()).decode())

        db.session.add(user)
        db.session.commit()

        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('home'))
    
    return render_template('users/register.html', title='Register', form=form)



@create_app.route('/login', methods=['GET', 'POST'])
def login():
    
    if current_user.is_authenticated:
        return redirect(url_for('home'))


    form = LoginForm()

    if form.validate_on_submit():
        email = form.email.data.lower()
        email_hash = const_hash(email)

        user = User.query.filter_by(email_hash=email_hash).first()

        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')

            flash(f'Login successful!', 'success')
            
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash(f'Login Unsuccessful. Please check email and password', 'danger')
    
    return render_template('users/login.html', title='Login', form=form)


@create_app.route('/logout')
def logout():
    logout_user()
    flash('Logged out.', 'success')
    return redirect(url_for('home'))




@create_app.route('/gallery')
@create_app.route('/photo_gallery')
def photo_gallery():
    key = create_app.config.get('FERNET_KEY')
    fernet = Fernet(key.encode())

    messages = Message.query.filter_by(message_type='gallery').order_by(desc(Message.created))


    return render_template('gallery/showcase.html', title='Gallery Showcase', messages=messages, fernet=fernet)





@create_app.route("/calendar-selection", methods=["POST"])
def calendar_selection():
    data = request.get_json()
    selected_date = data.get("selected_date")
    selected_month = data.get("selected_month")
    selected_time = data.get("selected_time")
    phone_number = data.get("phoneInput")
    email = data.get("emailInput")

    whatsapp = data.get("whatsapp", False)
    telegram = data.get("telegram", False)
    signal = data.get("signal", False)


    print("Selected date:", selected_date)
    print("Selected month:", selected_month)
    print("Selected time:", selected_time)
    print("Phone:", phone_number)
    print("Email:", email)
    print("WhatsApp:", whatsapp)
    print("Telegram:", telegram)
    print("Signal:", signal)

    datetime_date = datetime.strptime(selected_date, "%Y-%m-%d")
    datetime_time = datetime.strptime(selected_time, "%H:%M")
    appointment_datetime = datetime_date.replace(hour=datetime_time.hour, minute=datetime_time.minute)

    if not phone_number:
        phone_number = "NULL"

    key = create_app.config.get('FERNET_KEY')
    fernet = Fernet(key.encode())

    try:

        appointment = Appointment(selected_datetime=appointment_datetime, email=fernet.encrypt(email.encode()).decode(), 
                             phone_number=fernet.encrypt(phone_number.encode()).decode(), whatsapp=whatsapp, telegram=telegram, signal=signal)

        db.session.add(appointment)
        db.session.commit()

    
        # Format the datetime to a user-friendly string for the flash message
        formatted_date = appointment_datetime.strftime("%B %d, %Y")  # Example: "February 13, 2026"
        formatted_time = appointment_datetime.strftime("%I:%M %p")  # Example: "01:00 PM"

        # Success response with message
        return jsonify({"message": f"Appointment created for {formatted_date} at {formatted_time}", "success": True}), 200
    except Exception as e:
        # Error handling and response
        return jsonify({"message": f"Failed to create appointment. {str(e)}", "success": False}), 400
    #return {"message": "Appointment request received!"}, 200
# ----------------------------------------------------------------------------------------- #






@create_app.route('/terms-of-service')
def terms_of_service():

    return render_template('terms-of-service.html', title='Terms of Service')

@create_app.route('/privacy-policy', methods=['GET', 'POST'])
def privacy_policy():

    return render_template('privacy-policy.html', title='Privacy Policy')











































































# ----------------------------------------------------------------------------------------- #

# Admin Dashboard

@create_app.route('/admin/users', methods=['GET', 'POST'])
@create_app.route('/dashboard/users', methods=['GET', 'POST'])
def users():
    if not current_user.is_authenticated:
        flash(f'Admins only.', 'danger')
        return redirect(url_for('login'))

    if not current_user.admin:
        flash(f'Admins only.', 'danger')
        return redirect(url_for('home'))


    # page = request.args.get('page', 1, type=int)
    users = User.query.all()#\
            #.order_by(User.created.desc())\
            #.paginate(page=page, per_page=5)

    if users == None:
        return redirect(url_for('register'))

    '''
    form = UserForm()
    if form.validate_on_submit():
        user.query.get_or_404(id=user_id)
        if not user.admin:
            user.admin =True
        else:
            user.admin =False
        db.session.commit()

        flash('user priveleges changed', 'success')
        return redirect(url_for('users'))
    '''



    key = create_app.config.get('FERNET_KEY')
    fernet = Fernet(key.encode())  

    return render_template('users/dashboard.html', title='Users Dashboard', users=users, fernet=fernet)

'''
@create_app.route('/admin/user/create')
@create_app.route('/dashboard/user/create')
def users_create():
    if not current_user.is_authenticated:
        flash(f'Admins only.', 'danger')
        return redirect(url_for('login'))

    if not current_user.admin:
        flash(f'Admins only.', 'danger')
        return redirect(url_for('home'))


    return redirect('users')
    # return render_template('users/create.html')
'''
'''
@create_app.route('/admin/user/edit/<int:user_id>', methods=['GET', 'POST'])
@create_app.route('/dashboard/user/edit/<int:user_id>', methods=['GET', 'POST'])
def users_edit(user_id):
    
    # form = UserForm()
    
    user.query.get_or_404(id=user_id)
    if not user.admin:
        user.admin =True
    else:
        user.admin =False
    db.session.commit()

        flash('user priveleges changed', 'success')
        return redirect(url_for('users'))

    return render_template('users/edit.html', title ='Admin - User Edit', form=form)
'''









@create_app.route('/admin/calendar', methods=['GET', 'POST'])
@create_app.route('/dashboard/calendar', methods=['GET', 'POST'])
def calendar_dashboard():
    if not current_user.is_authenticated:
        flash(f'Admins only.', 'danger')
        return redirect(url_for('login'))

    if not current_user.admin:
        flash(f'Admins only.', 'danger')
        return redirect(url_for('home'))


    # page = request.args.get('page', 1, type=int)
    appointments = Appointment.query.all()#\
            #.order_by(User.created.desc())\
            #.paginate(page=page, per_page=5)


    key = create_app.config.get('FERNET_KEY')
    fernet = Fernet(key.encode())  

    return render_template('calendar/dashboard.html', title='Calendar Dashboard', appointments=appointments, fernet=fernet)






















@create_app.route('/admin')
@create_app.route('/dashboard')
@create_app.route('/dashboard/messages', methods=['GET', 'POST'])
def messages_dashboard():
    if not current_user.is_authenticated:
        flash(f'Admins only.', 'danger')
        return redirect(url_for('login'))

    if not current_user.admin:
        flash(f'Admins only.', 'danger')
        return redirect(url_for('home'))


    messages = Message.query.filter(Message.message_type != 'gallery').order_by(desc(Message.created)).all()

    key = create_app.config.get('FERNET_KEY')
    fernet = Fernet(key.encode())

    return render_template('messages/dashboard.html', title='Messages Dashboard', messages=messages, len=len, fernet=fernet, User=User)

@create_app.route('/dashboard/message/create', methods=['GET', 'POST'])
def messages_create():
    if not current_user.is_authenticated:
        flash(f'Admins only.', 'danger')
        return redirect(url_for('login'))

    if not current_user.admin:
        flash(f'Admins only.', 'danger')
        return redirect(url_for('home'))


    form = MessageCreateForm()
    if form.validate_on_submit():
        receiver = User.query.filter_by(email=form.email.data).first()
        if not receiver:
            abort(403)

        message = Message(title=form.title.data, description=form.description.data, 
                          sender=current_user.id, receiver=receiver.id)

        db.session.add(message)
        db.session.commit()
        flash('Message sent!', 'success')
        return redirect(url_for('messages_dashboard'))

    return render_template('messages/create.html', title='Message Create', form=form)

@create_app.route('/dashboard/message/view/<int:message_id>')
def messages_view(message_id):
    if not current_user.is_authenticated:
        flash(f'Admins only.', 'danger')
        return redirect(url_for('login'))

    if not current_user.admin:
        flash(f'Admins only.', 'danger')
        return redirect(url_for('home'))


    message = Message.query.filter_by(id=message_id).first()
    if not message:
        abort(404)

    message.status = "OPENED"
    db.session.commit()

    key = create_app.config.get('FERNET_KEY')
    fernet = Fernet(key.encode())

    return render_template('messages/view.html', title='Message - View', fernet=fernet, message=message)


@create_app.route('/admin/message/delete/<int:message_id>')
@create_app.route('/dashboard/message/delete/<int:message_id>')
def messages_delete(message_id):
    if not current_user.is_authenticated:
        flash(f'Admins only.', 'danger')
        return redirect(url_for('login'))

    if not current_user.admin:
        flash(f'Admins only.', 'danger')
        return redirect(url_for('home'))


    message = Message.query.filter_by(id=message_id).first()
    if not message:
        abort(404)

    key = create_app.config.get('FERNET_KEY')
    fernet = Fernet(key.encode())
    
    if message.gallery_1:
        if not delete_picture(fernet.decrypt(message.gallery_1.encode()).decode()):
            flash('Error deleting picture 1', 'danger')

    if message.gallery_2:
        if not delete_picture(fernet.decrypt(message.gallery_2.encode()).decode()):
            flash('Error deleting picture 2', 'danger')

    if message.gallery_3:
        if not delete_picture(fernet.decrypt(message.gallery_3.encode()).decode()):
            flash('Error deleting picture 3', 'danger')

    db.session.delete(message)
    db.session.commit()

    flash(f"Message was deleted!", 'info')
    return redirect(url_for('messages_dashboard'))







@create_app.route('/dashboard/gallery/create', methods=['GET', 'POST'])
def gallery_create():
    if not current_user.is_authenticated:
        flash(f'Admins only.', 'danger')
        return redirect(url_for('login'))

    if not current_user.admin:
        flash(f'Admins only.', 'danger')
        return redirect(url_for('home'))


    form = GalleryForm()
    if form.validate_on_submit():

        key = create_app.config.get('FERNET_KEY')
        fernet = Fernet(key.encode())

        if not form.description.data:
            form.description.data = "NONE"

        photo = save_picture(form.picture_1.data)

        message = Message(title=fernet.encrypt(form.title.data.encode()).decode(), description=fernet.encrypt(form.description.data.encode()).decode(), 
                          message_type='gallery', sender=current_user.id, receiver=create_app.config.get('ADMIN_ID'),
                          gallery_1=fernet.encrypt(photo.encode()).decode())

        db.session.add(message)
        db.session.commit()
        flash('Gallery created!', 'success')
        return redirect(url_for('gallery_dashboard'))

    return render_template('gallery/create.html', title='Gallery Create', form=form)


@create_app.route('/admin/gallery/delete/<int:message_id>')
@create_app.route('/dashboard/gallery/delete/<int:message_id>')
def gallery_delete(message_id):
    if not current_user.is_authenticated:
        flash(f'Admins only.', 'danger')
        return redirect(url_for('login'))

    if not current_user.admin:
        flash(f'Admins only.', 'danger')
        return redirect(url_for('home'))


    message = Message.query.filter_by(id=message_id).first()
    if not message:
        abort(404)

    key = create_app.config.get('FERNET_KEY')
    fernet = Fernet(key.encode())
    
    if message.gallery_1:
        if not delete_picture(fernet.decrypt(message.gallery_1.encode()).decode()):
            flash('Error deleting picture 1', 'danger')

    if message.gallery_2:
        if not delete_picture(fernet.decrypt(message.gallery_2.encode()).decode()):
            flash('Error deleting picture 2', 'danger')

    if message.gallery_3:
        if not delete_picture(fernet.decrypt(message.gallery_3.encode()).decode()):
            flash('Error deleting picture 3', 'danger')

    db.session.delete(message)
    db.session.commit()

    flash(f"Photo gallery was deleted!", 'info')
    return redirect(url_for('gallery_dashboard'))


@create_app.route('/dashboard/gallery', methods=['GET', 'POST'])
def gallery_dashboard():
    if not current_user.is_authenticated:
        flash(f'Admins only.', 'danger')
        return redirect(url_for('login'))

    if not current_user.admin:
        flash(f'Admins only.', 'danger')
        return redirect(url_for('home'))


    messages = Message.query.filter_by(message_type='gallery').order_by(desc(Message.created))

    key = create_app.config.get('FERNET_KEY')
    fernet = Fernet(key.encode())

    return render_template('gallery/dashboard.html', title='Gallery Dashboard', messages=messages, fernet=fernet)



'''
@create_app.route('/calendar', methods=['GET', 'POST'])
def calendar():
    products = Product.query.order_by(Product.created.desc()).all()


    

    # Cookie cart counter
    cart = 0
    if not current_user.is_authenticated:
        products_cookies = request.cookies.get('products')
        if products_cookies:
            cart = int(products_cookies)


    # return render_template('footer/about.html', title='About Us', cart=cart)
    return render_template('calendar.html', title='About Us', cart=cart)
'''
