# Chapter 7: Flask Authentication and Sessions

## Overview
This chapter covers comprehensive user authentication and session management in Flask, including user registration, login/logout, password security, role-based access control, and protected routes.

## What You'll Learn
- **User Authentication**: Complete login/logout system
- **Session Management**: Secure session handling
- **Password Security**: Hashing and validation
- **User Registration**: Account creation with validation
- **Role-based Access**: Admin and user permissions
- **Protected Routes**: Decorators for access control
- **Password Reset**: Token-based password recovery
- **Profile Management**: User account management

## Files Structure
```
Chapter-07/
├── app.py                 # Main Flask application with authentication
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── instance/             # Database files
├── templates/            # Jinja2 templates
│   ├── base.html         # Base template with navigation
│   ├── index.html        # Home page
│   ├── profile.html      # User profile page
│   ├── users.html        # Users list
│   ├── user_detail.html  # User details
│   ├── posts.html        # Posts list
│   ├── post_detail.html  # Post details
│   ├── auth/             # Authentication templates
│   │   ├── login.html        # Login form
│   │   ├── register.html     # Registration form
│   │   ├── edit_profile.html # Profile editing
│   │   ├── change_password.html # Password change
│   │   ├── forgot_password.html # Password reset request
│   │   └── reset_password.html  # Password reset form
│   ├── admin/            # Admin templates
│   │   ├── dashboard.html     # Admin dashboard
│   │   └── users.html         # User management
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

### 1. Flask-Login Setup
```python
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
```

### 2. User Model with Authentication
```python
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    is_admin = db.Column(db.Boolean, default=False)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
```

### 3. Login Route
```python
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter(
            (User.username == form.username.data) | 
            (User.email == form.username.data)
        ).first()
        
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect(url_for('index'))
        else:
            flash('Invalid credentials.', 'error')
    
    return render_template('auth/login.html', form=form)
```

### 4. Protected Routes
```python
@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html')

@app.route('/admin')
@admin_required
def admin_dashboard():
    return render_template('admin/dashboard.html')
```

### 5. Role-based Access Control
```python
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('Admin access required.', 'error')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function
```

### 6. Password Reset System
```python
class PasswordReset(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    token = db.Column(db.String(100), unique=True, nullable=False)
    expires_at = db.Column(db.DateTime, nullable=False)
    used = db.Column(db.Boolean, default=False)
```

## Authentication Features

### 1. User Registration
- **Fields**: Username, Email, First Name, Last Name, Password, Confirm Password
- **Validation**: Username uniqueness, email format, password strength
- **Security**: Password hashing, CSRF protection

### 2. User Login
- **Fields**: Username/Email, Password, Remember Me
- **Features**: Login tracking, session management, redirect handling
- **Security**: Password verification, account status checking

### 3. Profile Management
- **Features**: Profile editing, password change, avatar upload
- **Validation**: Email uniqueness, password confirmation
- **Security**: Current password verification

### 4. Password Reset
- **Process**: Email-based token generation, secure reset links
- **Security**: Token expiration, one-time use, secure generation
- **Features**: Email validation, password strength requirements

### 5. Role-based Access
- **Roles**: Admin, Regular User
- **Features**: Permission checking, protected routes, admin dashboard
- **Security**: Decorator-based access control

## Database Models

### User Model
- **Fields**: id, username, email, password_hash, first_name, last_name, bio, avatar_url
- **Flags**: is_active, is_admin, is_verified
- **Timestamps**: created_at, updated_at, last_login
- **Tracking**: login_count

### Role Model
- **Fields**: id, name, description, permissions
- **Relationships**: Many-to-many with users

### PasswordReset Model
- **Fields**: id, user_id, token, expires_at, used, created_at
- **Security**: Token-based, time-limited, one-time use

## Security Features

### 1. Password Security
```python
# Password hashing
def set_password(self, password):
    self.password_hash = generate_password_hash(password)

def check_password(self, password):
    return check_password_hash(self.password_hash, password)
```

### 2. Session Security
```python
# Session configuration
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=24)
app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'
```

### 3. CSRF Protection
```html
<!-- In forms -->
{{ form.hidden_tag() }}
```

### 4. Access Control
```python
# Login required decorator
@login_required
def protected_route():
    pass

# Admin required decorator
@admin_required
def admin_route():
    pass
```

## Routes and Features

- **`/`** - Home page with authentication status
- **`/login`** - User login
- **`/logout`** - User logout
- **`/register`** - User registration
- **`/profile`** - User profile page
- **`/profile/edit`** - Edit profile
- **`/change-password`** - Change password
- **`/forgot-password`** - Request password reset
- **`/reset-password/<token>`** - Reset password with token
- **`/users`** - List users (login required)
- **`/user/<id>`** - User details
- **`/admin`** - Admin dashboard (admin required)
- **`/admin/users`** - User management (admin required)
- **`/posts`** - Posts list (login required)
- **`/post/<id>`** - Post details (login required)

## Demo Credentials

### Admin User
- **Username**: admin
- **Password**: admin123
- **Access**: Full admin access to all features

### Regular User
- **Username**: user
- **Password**: user123
- **Access**: Standard user access

## Authentication Flow

### 1. Registration Flow
1. User fills registration form
2. Form validation (username, email uniqueness)
3. Password hashing and user creation
4. Success message and redirect to login

### 2. Login Flow
1. User enters credentials
2. System finds user by username/email
3. Password verification
4. Account status check
5. Session creation and login tracking
6. Redirect to intended page

### 3. Password Reset Flow
1. User requests password reset
2. System generates secure token
3. Token stored with expiration
4. User receives reset link
5. Token validation on reset page
6. Password update and token invalidation

## Best Practices

### 1. Security
- Always hash passwords
- Use strong secret keys
- Implement CSRF protection
- Validate all inputs
- Use HTTPS in production

### 2. User Experience
- Provide clear error messages
- Remember user preferences
- Implement "Remember Me" functionality
- Handle session expiration gracefully

### 3. Code Organization
- Use decorators for access control
- Separate authentication logic
- Implement proper error handling
- Use consistent naming conventions

## Common Patterns

### Login Required Decorator
```python
@login_required
def protected_view():
    return render_template('protected.html')
```

### Admin Required Decorator
```python
@admin_required
def admin_view():
    return render_template('admin.html')
```

### Current User Access
```python
# In templates
{% if current_user.is_authenticated %}
    <p>Welcome, {{ current_user.username }}!</p>
{% endif %}
```

### Session Management
```python
# Set permanent session
session.permanent = True

# Check session
if 'user_id' in session:
    user = User.query.get(session['user_id'])
```

## Troubleshooting

### Common Issues
1. **Login not working**: Check password hashing and user lookup
2. **Session not persisting**: Verify secret key and session configuration
3. **Access denied**: Check user roles and decorators
4. **Password reset fails**: Verify token generation and expiration

### Debug Tips
1. Check user authentication status
2. Verify session data
3. Test with different user roles
4. Check database for user records

## Next Steps
After completing this chapter, you should understand:
- How to implement user authentication
- Session management and security
- Role-based access control
- Password security best practices
- Protected routes and decorators
- User profile management

## Additional Resources

- [Flask-Login Documentation](https://flask-login.readthedocs.io/)
- [Werkzeug Security](https://werkzeug.palletsprojects.com/en/2.3.x/utils/#module-werkzeug.security)
- [OWASP Authentication Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html)
- [Flask Session Management](https://flask.palletsprojects.com/en/2.3.x/quickstart/#sessions)
