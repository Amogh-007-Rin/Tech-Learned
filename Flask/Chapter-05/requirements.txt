# Chapter 5: Flask Forms and WTForms

## Overview
This chapter covers comprehensive form handling in Flask using WTForms and Flask-WTF, including form creation, validation, CSRF protection, file uploads, and advanced form features.

## What You'll Learn
- **WTForms Integration**: Using Flask-WTF for form handling
- **Form Creation**: Creating various types of forms
- **Field Validation**: Built-in and custom validators
- **CSRF Protection**: Security against cross-site request forgery
- **File Uploads**: Handling file uploads securely
- **Form Rendering**: Customizing form appearance
- **Dynamic Forms**: Creating forms with dynamic fields
- **Form Processing**: Handling form submission and validation

## Files Structure
```
Chapter-05/
├── app.py                 # Main Flask application with forms
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── uploads/              # File upload directory
├── templates/            # Jinja2 templates
│   ├── base.html         # Base template
│   ├── index.html        # Home page
│   ├── users.html        # Users list
│   ├── posts.html        # Posts list
│   ├── files.html        # Files list
│   ├── forms/            # Form templates
│   │   ├── contact.html      # Contact form
│   │   ├── register.html     # User registration
│   │   ├── profile.html      # User profile
│   │   ├── upload.html       # File upload
│   │   ├── create_post.html  # Blog post creation
│   │   ├── survey.html       # Survey form
│   │   ├── dynamic.html      # Dynamic form
│   │   └── search.html       # Search form
│   └── errors/           # Error pages
│       ├── 404.html      # Not found page
│       └── 500.html      # Server error page
└── static/               # Static files
    ├── css/
    │   └── style.css     # Custom styles
    └── js/
        └── main.js       # Custom JavaScript
```

## Installation and Setup

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Application**:
   ```bash
   python app.py
   ```

3. **Access the Application**:
   Open your browser and go to `http://localhost:5000`

## Key Concepts

### 1. Flask-WTF Setup
```python
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email, Length

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Required for CSRF
```

### 2. Form Definition
```python
class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=50)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    message = TextAreaField('Message', validators=[DataRequired(), Length(min=10)])
    submit = SubmitField('Send Message')
```

### 3. Form Rendering
```html
<form method="POST">
    {{ form.hidden_tag() }}  <!-- CSRF token -->
    {{ form.name.label(class="form-label") }}
    {{ form.name(class="form-control") }}
    {{ form.submit(class="btn btn-primary") }}
</form>
```

### 4. Form Processing
```python
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        # Process form data
        name = form.name.data
        email = form.email.data
        message = form.message.data
        # Save to database, send email, etc.
        flash('Message sent successfully!', 'success')
        return redirect(url_for('contact'))
    return render_template('contact.html', form=form)
```

### 5. Custom Validators
```python
def validate_username(form, field):
    if field.data.lower() in ['admin', 'root']:
        raise ValidationError('This username is not allowed.')

class UserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), validate_username])
```

### 6. File Uploads
```python
from flask_wtf.file import FileField, FileRequired, FileAllowed

class UploadForm(FlaskForm):
    file = FileField('File', validators=[
        FileRequired(),
        FileAllowed(['jpg', 'png', 'pdf'], 'File type not allowed!')
    ])

# In route
if form.validate_on_submit():
    file = form.file.data
    filename = secure_filename(file.filename)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
```

## Form Types Demonstrated

### 1. Contact Form
- **Fields**: Name, Email, Subject, Message
- **Validation**: Required fields, email format, length limits
- **Features**: CSRF protection, error handling

### 2. User Registration Form
- **Fields**: Username, Email, Password, Confirm Password, Age, Country, Gender, Newsletter, Terms
- **Validation**: Custom username validation, password confirmation, age limits
- **Features**: Radio buttons, select dropdown, checkboxes

### 3. File Upload Form
- **Fields**: Title, Description, File, Category
- **Validation**: File type restrictions, size limits
- **Features**: Secure file handling, file type validation

### 4. Dynamic Form
- **Fields**: Form name, dynamic item list
- **Validation**: Minimum/maximum items
- **Features**: JavaScript-powered field addition/removal

### 5. Survey Form
- **Fields**: Name, Email, Age Group, Interests, Rating, Comments, Subscribe
- **Validation**: Required fields, number ranges
- **Features**: Radio buttons, select dropdown, number input

## Field Types Used

### Text Fields
- `StringField` - Single line text input
- `TextAreaField` - Multi-line text input
- `PasswordField` - Password input (hidden)

### Selection Fields
- `SelectField` - Dropdown selection
- `RadioField` - Radio button group
- `BooleanField` - Checkbox

### Special Fields
- `FileField` - File upload
- `DateField` - Date picker
- `IntegerField` - Number input
- `FloatField` - Decimal input
- `FieldList` - Dynamic field list

### Form Controls
- `SubmitField` - Submit button
- `HiddenField` - Hidden input
- `FormField` - Nested form

## Validators Used

### Built-in Validators
- `DataRequired` - Field must not be empty
- `Email` - Valid email format
- `Length` - String length limits
- `NumberRange` - Number range limits
- `Regexp` - Regular expression validation
- `EqualTo` - Field must match another field
- `Optional` - Field is optional

### Custom Validators
- Username validation (restricted names)
- Age validation (minimum/maximum age)
- Business logic validation

## Security Features

### 1. CSRF Protection
```python
# Automatically included in all forms
{{ form.hidden_tag() }}
```

### 2. File Upload Security
```python
# File type validation
FileAllowed(['jpg', 'png', 'pdf'], 'File type not allowed!')

# Secure filename generation
filename = secure_filename(file.filename)

# File size limits
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB
```

### 3. Input Validation
- Server-side validation for all inputs
- Client-side validation enhancement
- Sanitization of user input

## Routes and Features

- **`/`** - Home page with form overview
- **`/contact`** - Contact form
- **`/register`** - User registration form
- **`/profile`** - User profile form
- **`/upload`** - File upload form
- **`/create_post`** - Blog post creation form
- **`/survey`** - Survey form
- **`/dynamic`** - Dynamic form with field management
- **`/search`** - Search form
- **`/users`** - Display registered users
- **`/posts`** - Display blog posts
- **`/files`** - Display uploaded files

## JavaScript Features

### 1. Form Enhancement
- Real-time validation
- Password strength indicator
- Character counters for textareas
- File upload preview

### 2. Dynamic Forms
- Add/remove fields dynamically
- Field count limits
- User-friendly interface

### 3. User Experience
- Loading states
- Form submission feedback
- Auto-dismissing alerts
- Smooth animations

## Best Practices

### 1. Form Design
- Use appropriate field types
- Provide clear labels and help text
- Group related fields
- Use consistent styling

### 2. Validation
- Validate on both client and server
- Provide clear error messages
- Use appropriate validators
- Implement custom validation when needed

### 3. Security
- Always use CSRF protection
- Validate file uploads
- Sanitize user input
- Use HTTPS in production

### 4. User Experience
- Provide immediate feedback
- Use loading states
- Handle errors gracefully
- Make forms accessible

## Common Patterns

### Form with Validation
```html
<div class="mb-3">
    {{ form.field.label(class="form-label") }}
    {{ form.field(class="form-control" + (" is-invalid" if form.field.errors else "")) }}
    {% if form.field.errors %}
        <div class="invalid-feedback">
            {% for error in form.field.errors %}
                {{ error }}
            {% endfor %}
        </div>
    {% endif %}
</div>
```

### File Upload Handling
```python
if form.validate_on_submit():
    file = form.file.data
    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)
    flash('File uploaded successfully!', 'success')
```

### Dynamic Form Fields
```python
class DynamicForm(FlaskForm):
    items = FieldList(StringField('Item'), min_entries=1, max_entries=10)
```

## Troubleshooting

### Common Issues
1. **CSRF Token Missing**: Ensure `{{ form.hidden_tag() }}` is included
2. **Form Not Validating**: Check validators and form setup
3. **File Upload Fails**: Verify file types and size limits
4. **Validation Errors**: Check validator parameters

### Debug Tips
1. Use `form.errors` to see validation errors
2. Check browser console for JavaScript errors
3. Verify form field names match form definition
4. Test with different input values

## Next Steps
After completing this chapter, you should understand:
- How to create and use WTForms
- Form validation and security
- File upload handling
- Dynamic form creation
- Form rendering and styling
- JavaScript form enhancement

## Additional Resources

- [Flask-WTF Documentation](https://flask-wtf.readthedocs.io/)
- [WTForms Documentation](https://wtforms.readthedocs.io/)
- [Form Security Best Practices](https://owasp.org/www-community/attacks/csrf)
- [File Upload Security](https://owasp.org/www-community/vulnerabilities/Unrestricted_File_Upload)
