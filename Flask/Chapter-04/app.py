"""
Chapter 4: Flask Templates and Jinja2
=====================================

This chapter covers:
1. Introduction to Jinja2 templating engine
2. Template inheritance and blocks
3. Template variables and filters
4. Template control structures (loops, conditions)
5. Template macros and includes
6. Static files handling

Prerequisites:
- Basic understanding of Flask routes
- HTML knowledge
- Python basics

Let's start with a simple Flask app that demonstrates template usage.
"""

from flask import Flask, render_template, request, url_for, redirect, flash
from datetime import datetime
import os

# Create Flask application instance
app = Flask(__name__)

# Secret key for flash messages (in production, use environment variables)
app.secret_key = 'your-secret-key-here'

# Sample data for demonstration
users = [
    {'id': 1, 'name': 'John Doe', 'email': 'john@example.com', 'age': 25, 'city': 'New York'},
    {'id': 2, 'name': 'Jane Smith', 'email': 'jane@example.com', 'age': 30, 'city': 'Los Angeles'},
    {'id': 3, 'name': 'Bob Johnson', 'email': 'bob@example.com', 'age': 35, 'city': 'Chicago'},
    {'id': 4, 'name': 'Alice Brown', 'email': 'alice@example.com', 'age': 28, 'city': 'Houston'},
]

# Sample posts data
posts = [
    {'id': 1, 'title': 'Getting Started with Flask', 'content': 'Flask is a micro web framework...', 'author': 'John Doe', 'date': '2024-01-15'},
    {'id': 2, 'title': 'Understanding Jinja2 Templates', 'content': 'Jinja2 is a powerful templating engine...', 'author': 'Jane Smith', 'date': '2024-01-16'},
    {'id': 3, 'title': 'Flask Forms and Validation', 'content': 'Forms are essential for user interaction...', 'author': 'Bob Johnson', 'date': '2024-01-17'},
]

@app.route('/')
def index():
    """
    Home page route that demonstrates basic template usage
    """
    # Pass data to template
    current_time = datetime.now()
    return render_template('index.html', 
                         title='Flask Templates Demo',
                         current_time=current_time,
                         user_count=len(users))

@app.route('/users')
def users_list():
    """
    Route to display list of users with template loops
    """
    return render_template('users.html', 
                         users=users,
                         title='Users List')

@app.route('/user/<int:user_id>')
def user_detail(user_id):
    """
    Route to display individual user details
    Demonstrates template conditionals and filters
    """
    # Find user by ID
    user = next((u for u in users if u['id'] == user_id), None)
    
    if not user:
        flash('User not found!', 'error')
        return redirect(url_for('users_list'))
    
    return render_template('user_detail.html', 
                         user=user,
                         title=f"User: {user['name']}")

@app.route('/posts')
def posts_list():
    """
    Route to display blog posts with template inheritance
    """
    return render_template('posts.html', 
                         posts=posts,
                         title='Blog Posts')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    """
    Contact form route demonstrating form handling
    """
    if request.method == 'POST':
        # Get form data
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        
        # Simple validation
        if not name or not email or not message:
            flash('All fields are required!', 'error')
        else:
            flash('Thank you for your message! We will get back to you soon.', 'success')
            # In a real application, you would save this to a database
            print(f"Contact form submitted: {name} ({email}): {message}")
        
        return redirect(url_for('contact'))
    
    return render_template('contact.html', title='Contact Us')

@app.route('/demo-filters')
def demo_filters():
    """
    Route to demonstrate Jinja2 filters
    """
    sample_text = "hello world"
    sample_list = [1, 2, 3, 4, 5]
    sample_dict = {'name': 'John', 'age': 25, 'city': 'New York'}
    
    return render_template('demo_filters.html',
                         sample_text=sample_text,
                         sample_list=sample_list,
                         sample_dict=sample_dict,
                         title='Jinja2 Filters Demo')

@app.route('/demo-macros')
def demo_macros():
    """
    Route to demonstrate Jinja2 macros
    """
    return render_template('demo_macros.html',
                         users=users,
                         title='Jinja2 Macros Demo')

# Custom template filters
@app.template_filter('datetime')
def datetime_filter(value):
    """
    Custom filter to format datetime objects
    Usage in template: {{ date|datetime }}
    """
    if value is None:
        return ""
    return value.strftime('%Y-%m-%d %H:%M:%S')

@app.template_filter('currency')
def currency_filter(value):
    """
    Custom filter to format currency
    Usage in template: {{ price|currency }}
    """
    if value is None:
        return "$0.00"
    return f"${value:.2f}"

# Template context processor
@app.context_processor
def inject_global_vars():
    """
    Inject global variables into all templates
    These variables will be available in every template
    """
    return {
        'site_name': 'Flask Learning Hub',
        'current_year': datetime.now().year,
        'app_version': '1.0.0'
    }

# Error handlers
@app.errorhandler(404)
def not_found(error):
    """
    Custom 404 error page
    """
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    """
    Custom 500 error page
    """
    return render_template('errors/500.html'), 500

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    os.makedirs('templates', exist_ok=True)
    os.makedirs('templates/errors', exist_ok=True)
    os.makedirs('static/css', exist_ok=True)
    os.makedirs('static/js', exist_ok=True)
    
    # Run the application
    app.run(debug=True, host='0.0.0.0', port=5000)
