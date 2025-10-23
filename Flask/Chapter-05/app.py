"""
Chapter 5: Flask Forms and WTForms
==================================

This chapter covers:
1. Introduction to Flask-WTF and WTForms
2. Form creation and validation
3. CSRF protection
4. File uploads
5. Form rendering and customization
6. Advanced form features

Prerequisites:
- Basic understanding of Flask routes
- HTML form knowledge
- Python basics

Let's start with a comprehensive Flask app that demonstrates form handling.
"""

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, send_from_directory
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, TextAreaField, SelectField, RadioField, BooleanField, IntegerField, FloatField, DateField, PasswordField, SubmitField, HiddenField, FieldList, FormField
from wtforms.validators import DataRequired, Email, Length, NumberRange, Optional, Regexp, EqualTo, ValidationError
from wtforms.widgets import TextArea
import os
from datetime import datetime, date
import secrets

# Create Flask application instance
app = Flask(__name__)

# Secret key for CSRF protection (in production, use environment variables)
app.secret_key = 'your-secret-key-here'

# Configuration for file uploads
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'docx'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Create upload directory if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Sample data for demonstration
users_data = []
posts_data = []

# Custom validators
def validate_username(form, field):
    """Custom validator for username"""
    if field.data.lower() in ['admin', 'root', 'user']:
        raise ValidationError('This username is not allowed.')

def validate_age(form, field):
    """Custom validator for age"""
    if field.data < 13:
        raise ValidationError('You must be at least 13 years old.')
    if field.data > 120:
        raise ValidationError('Please enter a valid age.')

# Form Definitions
class ContactForm(FlaskForm):
    """Simple contact form"""
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=50)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    subject = StringField('Subject', validators=[DataRequired(), Length(min=5, max=100)])
    message = TextAreaField('Message', validators=[DataRequired(), Length(min=10, max=1000)])
    submit = SubmitField('Send Message')

class UserRegistrationForm(FlaskForm):
    """User registration form with validation"""
    username = StringField('Username', validators=[
        DataRequired(), 
        Length(min=3, max=20),
        Regexp('^[A-Za-z0-9_]+$', message='Username can only contain letters, numbers, and underscores'),
        validate_username
    ])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=8, message='Password must be at least 8 characters long')
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(),
        EqualTo('password', message='Passwords must match')
    ])
    age = IntegerField('Age', validators=[DataRequired(), NumberRange(min=13, max=120), validate_age])
    country = SelectField('Country', choices=[
        ('', 'Select Country'),
        ('US', 'United States'),
        ('CA', 'Canada'),
        ('UK', 'United Kingdom'),
        ('AU', 'Australia'),
        ('DE', 'Germany'),
        ('FR', 'France'),
        ('JP', 'Japan'),
        ('IN', 'India'),
        ('BR', 'Brazil'),
        ('MX', 'Mexico')
    ], validators=[DataRequired()])
    gender = RadioField('Gender', choices=[
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
        ('prefer_not_to_say', 'Prefer not to say')
    ], validators=[DataRequired()])
    newsletter = BooleanField('Subscribe to newsletter')
    terms = BooleanField('I agree to the Terms and Conditions', validators=[DataRequired()])
    submit = SubmitField('Register')

class UserProfileForm(FlaskForm):
    """User profile form"""
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=2, max=50)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=50)])
    bio = TextAreaField('Bio', validators=[Optional(), Length(max=500)])
    website = StringField('Website', validators=[Optional(), Regexp(r'^https?://', message='Must be a valid URL')])
    birth_date = DateField('Birth Date', validators=[Optional()])
    phone = StringField('Phone', validators=[Optional(), Regexp(r'^\+?1?\d{9,15}$', message='Invalid phone number')])
    submit = SubmitField('Update Profile')

class FileUploadForm(FlaskForm):
    """File upload form"""
    title = StringField('File Title', validators=[DataRequired(), Length(min=1, max=100)])
    description = TextAreaField('Description', validators=[Optional(), Length(max=500)])
    file = FileField('Choose File', validators=[
        FileRequired(),
        FileAllowed(ALLOWED_EXTENSIONS, 'File type not allowed!')
    ])
    category = SelectField('Category', choices=[
        ('document', 'Document'),
        ('image', 'Image'),
        ('other', 'Other')
    ], validators=[DataRequired()])
    submit = SubmitField('Upload File')

class SearchForm(FlaskForm):
    """Search form"""
    query = StringField('Search', validators=[DataRequired(), Length(min=1, max=100)])
    category = SelectField('Category', choices=[
        ('all', 'All'),
        ('users', 'Users'),
        ('posts', 'Posts'),
        ('files', 'Files')
    ], default='all')
    submit = SubmitField('Search')

class PostForm(FlaskForm):
    """Blog post form"""
    title = StringField('Title', validators=[DataRequired(), Length(min=5, max=200)])
    content = TextAreaField('Content', validators=[DataRequired(), Length(min=10, max=5000)])
    category = SelectField('Category', choices=[
        ('general', 'General'),
        ('technology', 'Technology'),
        ('lifestyle', 'Lifestyle'),
        ('travel', 'Travel'),
        ('food', 'Food'),
        ('sports', 'Sports')
    ], validators=[DataRequired()])
    tags = StringField('Tags (comma-separated)', validators=[Optional()])
    is_published = BooleanField('Publish immediately')
    submit = SubmitField('Create Post')

class DynamicForm(FlaskForm):
    """Dynamic form with field lists"""
    name = StringField('Form Name', validators=[DataRequired()])
    items = FieldList(StringField('Item'), min_entries=1, max_entries=10)
    submit = SubmitField('Submit Dynamic Form')

class SurveyForm(FlaskForm):
    """Survey form with various field types"""
    name = StringField('Your Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    age_group = RadioField('Age Group', choices=[
        ('18-25', '18-25'),
        ('26-35', '26-35'),
        ('36-45', '36-45'),
        ('46-55', '46-55'),
        ('55+', '55+')
    ], validators=[DataRequired()])
    interests = SelectField('Primary Interest', choices=[
        ('technology', 'Technology'),
        ('science', 'Science'),
        ('arts', 'Arts'),
        ('sports', 'Sports'),
        ('music', 'Music'),
        ('travel', 'Travel')
    ], validators=[DataRequired()])
    rating = IntegerField('Overall Rating (1-10)', validators=[DataRequired(), NumberRange(min=1, max=10)])
    comments = TextAreaField('Additional Comments', validators=[Optional()])
    subscribe = BooleanField('Subscribe to updates')
    submit = SubmitField('Submit Survey')

# Routes
@app.route('/')
def index():
    """Home page with form examples"""
    return render_template('index.html', 
                         title='Flask Forms Demo',
                         user_count=len(users_data),
                         post_count=len(posts_data))

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    """Contact form route"""
    form = ContactForm()
    
    if form.validate_on_submit():
        # Process form data
        contact_data = {
            'name': form.name.data,
            'email': form.email.data,
            'subject': form.subject.data,
            'message': form.message.data,
            'timestamp': datetime.now()
        }
        
        flash('Thank you for your message! We will get back to you soon.', 'success')
        print(f"Contact form submitted: {contact_data}")
        return redirect(url_for('contact'))
    
    return render_template('forms/contact.html', 
                         form=form,
                         title='Contact Us')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration form route"""
    form = UserRegistrationForm()
    
    if form.validate_on_submit():
        # Process registration
        user_data = {
            'id': len(users_data) + 1,
            'username': form.username.data,
            'email': form.email.data,
            'age': form.age.data,
            'country': form.country.data,
            'gender': form.gender.data,
            'newsletter': form.newsletter.data,
            'created_at': datetime.now()
        }
        
        users_data.append(user_data)
        flash(f'Registration successful! Welcome, {form.username.data}!', 'success')
        return redirect(url_for('users_list'))
    
    return render_template('forms/register.html', 
                         form=form,
                         title='User Registration')

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    """User profile form route"""
    form = UserProfileForm()
    
    if form.validate_on_submit():
        # Process profile update
        profile_data = {
            'first_name': form.first_name.data,
            'last_name': form.last_name.data,
            'bio': form.bio.data,
            'website': form.website.data,
            'birth_date': form.birth_date.data,
            'phone': form.phone.data,
            'updated_at': datetime.now()
        }
        
        flash('Profile updated successfully!', 'success')
        print(f"Profile updated: {profile_data}")
        return redirect(url_for('profile'))
    
    return render_template('forms/profile.html', 
                         form=form,
                         title='User Profile')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    """File upload form route"""
    form = FileUploadForm()
    
    if form.validate_on_submit():
        # Process file upload
        file = form.file.data
        filename = f"{secrets.token_hex(8)}_{file.filename}"
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        upload_data = {
            'id': len(posts_data) + 1,
            'title': form.title.data,
            'description': form.description.data,
            'filename': filename,
            'original_filename': file.filename,
            'category': form.category.data,
            'file_size': os.path.getsize(file_path),
            'uploaded_at': datetime.now()
        }
        
        posts_data.append(upload_data)
        flash(f'File "{form.title.data}" uploaded successfully!', 'success')
        return redirect(url_for('files_list'))
    
    return render_template('forms/upload.html', 
                         form=form,
                         title='File Upload')

@app.route('/search', methods=['GET', 'POST'])
def search():
    """Search form route"""
    form = SearchForm()
    results = []
    
    if form.validate_on_submit():
        query = form.query.data.lower()
        category = form.category.data
        
        if category == 'all' or category == 'users':
            for user in users_data:
                if query in user['username'].lower() or query in user['email'].lower():
                    results.append({'type': 'user', 'data': user})
        
        if category == 'all' or category == 'posts':
            for post in posts_data:
                if query in post.get('title', '').lower() or query in post.get('content', '').lower():
                    results.append({'type': 'post', 'data': post})
    
    return render_template('forms/search.html', 
                         form=form,
                         results=results,
                         title='Search')

@app.route('/post/create', methods=['GET', 'POST'])
def create_post():
    """Blog post creation form route"""
    form = PostForm()
    
    if form.validate_on_submit():
        # Process post creation
        post_data = {
            'id': len(posts_data) + 1,
            'title': form.title.data,
            'content': form.content.data,
            'category': form.category.data,
            'tags': [tag.strip() for tag in form.tags.data.split(',') if tag.strip()],
            'is_published': form.is_published.data,
            'created_at': datetime.now()
        }
        
        posts_data.append(post_data)
        flash(f'Post "{form.title.data}" created successfully!', 'success')
        return redirect(url_for('posts_list'))
    
    return render_template('forms/create_post.html', 
                         form=form,
                         title='Create Post')

@app.route('/survey', methods=['GET', 'POST'])
def survey():
    """Survey form route"""
    form = SurveyForm()
    
    if form.validate_on_submit():
        # Process survey
        survey_data = {
            'name': form.name.data,
            'email': form.email.data,
            'age_group': form.age_group.data,
            'interests': form.interests.data,
            'rating': form.rating.data,
            'comments': form.comments.data,
            'subscribe': form.subscribe.data,
            'submitted_at': datetime.now()
        }
        
        flash('Survey submitted successfully! Thank you for your feedback.', 'success')
        print(f"Survey submitted: {survey_data}")
        return redirect(url_for('survey'))
    
    return render_template('forms/survey.html', 
                         form=form,
                         title='User Survey')

@app.route('/dynamic', methods=['GET', 'POST'])
def dynamic_form():
    """Dynamic form route"""
    form = DynamicForm()
    
    if form.validate_on_submit():
        # Process dynamic form
        dynamic_data = {
            'name': form.name.data,
            'items': form.items.data,
            'submitted_at': datetime.now()
        }
        
        flash(f'Dynamic form "{form.name.data}" submitted with {len(form.items.data)} items!', 'success')
        print(f"Dynamic form submitted: {dynamic_data}")
        return redirect(url_for('dynamic_form'))
    
    return render_template('forms/dynamic.html', 
                         form=form,
                         title='Dynamic Form')

@app.route('/users')
def users_list():
    """Display registered users"""
    return render_template('users.html', 
                         users=users_data,
                         title='Registered Users')

@app.route('/posts')
def posts_list():
    """Display blog posts"""
    return render_template('posts.html', 
                         posts=posts_data,
                         title='Blog Posts')

@app.route('/files')
def files_list():
    """Display uploaded files"""
    return render_template('files.html', 
                         files=posts_data,
                         title='Uploaded Files')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    """Serve uploaded files"""
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# AJAX route for dynamic form fields
@app.route('/api/add-field', methods=['POST'])
def add_field():
    """Add a new field to dynamic form"""
    data = request.get_json()
    field_count = data.get('field_count', 0)
    
    if field_count < 10:  # Max 10 fields
        return jsonify({'success': True, 'field_count': field_count + 1})
    else:
        return jsonify({'success': False, 'message': 'Maximum 10 fields allowed'})

# Error handlers
@app.errorhandler(413)
def too_large(e):
    """Handle file too large error"""
    flash('File is too large. Maximum size is 16MB.', 'error')
    return redirect(url_for('upload'))

@app.errorhandler(404)
def not_found(error):
    """Custom 404 error page"""
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    """Custom 500 error page"""
    return render_template('errors/500.html'), 500

if __name__ == '__main__':
    # Create necessary directories
    os.makedirs('templates', exist_ok=True)
    os.makedirs('templates/forms', exist_ok=True)
    os.makedirs('templates/errors', exist_ok=True)
    os.makedirs('static/css', exist_ok=True)
    os.makedirs('static/js', exist_ok=True)
    
    # Run the application
    app.run(debug=True, host='0.0.0.0', port=5000)
