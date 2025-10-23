# Chapter 4: Flask Templates and Jinja2

## Overview
This chapter covers Flask templating with Jinja2, including template inheritance, variables, filters, control structures, macros, and static files.

## What You'll Learn
- **Template Inheritance**: Create base templates and extend them
- **Template Variables**: Pass data from Flask to templates
- **Template Filters**: Transform data in templates
- **Control Structures**: Use loops and conditionals in templates
- **Template Macros**: Create reusable template components
- **Static Files**: Serve CSS, JavaScript, and images
- **Custom Filters**: Create your own template filters
- **Context Processors**: Inject global variables into templates

## Files Structure
```
Chapter-04/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── templates/            # Jinja2 templates
│   ├── base.html         # Base template
│   ├── index.html        # Home page
│   ├── users.html        # Users list page
│   ├── user_detail.html  # User details page
│   ├── posts.html        # Blog posts page
│   ├── contact.html      # Contact form page
│   ├── demo_filters.html # Filters demonstration
│   ├── demo_macros.html  # Macros demonstration
│   ├── macros.html       # Reusable macros
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

### 1. Template Inheritance
```html
<!-- base.html -->
<!DOCTYPE html>
<html>
<head>
    <title>{% block title %}{% endblock %}</title>
</head>
<body>
    {% block content %}{% endblock %}
</body>
</html>

<!-- child.html -->
{% extends "base.html" %}
{% block title %}My Page{% endblock %}
{% block content %}
    <h1>Hello World!</h1>
{% endblock %}
```

### 2. Template Variables
```python
# In Flask route
return render_template('index.html', 
                     title='Home',
                     users=users,
                     current_time=datetime.now())
```

```html
<!-- In template -->
<h1>{{ title }}</h1>
<p>Current time: {{ current_time|datetime }}</p>
```

### 3. Template Filters
```html
<!-- Built-in filters -->
{{ "hello world"|upper }}        <!-- HELLO WORLD -->
{{ "hello world"|title }}        <!-- Hello World -->
{{ users|length }}               <!-- Number of users -->
{{ user.name|truncate(10) }}     <!-- Truncated name -->

<!-- Custom filters -->
{{ current_time|datetime }}      <!-- Custom datetime format -->
{{ price|currency }}             <!-- Custom currency format -->
```

### 4. Control Structures
```html
<!-- Conditionals -->
{% if user.age >= 18 %}
    <p>Adult user</p>
{% elif user.age >= 13 %}
    <p>Teen user</p>
{% else %}
    <p>Child user</p>
{% endif %}

<!-- Loops -->
{% for user in users %}
    <p>{{ loop.index }}. {{ user.name }}</p>
{% endfor %}
```

### 5. Template Macros
```html
<!-- Define macro -->
{% macro user_card(user) %}
    <div class="card">
        <h5>{{ user.name }}</h5>
        <p>{{ user.email }}</p>
    </div>
{% endmacro %}

<!-- Use macro -->
{% from 'macros.html' import user_card %}
{{ user_card(user) }}
```

### 6. Custom Filters
```python
@app.template_filter('datetime')
def datetime_filter(value):
    if value is None:
        return ""
    return value.strftime('%Y-%m-%d %H:%M:%S')
```

### 7. Context Processors
```python
@app.context_processor
def inject_global_vars():
    return {
        'site_name': 'My Flask App',
        'current_year': datetime.now().year
    }
```

## Routes and Features

- **`/`** - Home page with template variables and control structures
- **`/users`** - Users list with template loops and conditionals
- **`/user/<id>`** - User details with template filters
- **`/posts`** - Blog posts demonstrating template inheritance
- **`/contact`** - Contact form with form handling
- **`/demo-filters`** - Comprehensive filters demonstration
- **`/demo-macros`** - Macros usage examples

## Key Features Demonstrated

1. **Template Inheritance**: Base template with navigation and footer
2. **Template Variables**: Passing data from Flask to templates
3. **Template Filters**: Built-in and custom filters
4. **Control Structures**: Loops, conditionals, and loop variables
5. **Template Macros**: Reusable template components
6. **Static Files**: CSS and JavaScript integration
7. **Error Handling**: Custom error pages
8. **Form Processing**: GET/POST form handling
9. **Flash Messages**: User feedback system
10. **Responsive Design**: Bootstrap integration

## Best Practices

1. **Template Organization**: Use inheritance for consistent layout
2. **Macro Usage**: Create reusable components for common elements
3. **Filter Usage**: Use filters for data transformation
4. **Static Files**: Organize CSS and JS in separate files
5. **Error Handling**: Provide custom error pages
6. **Form Validation**: Validate input on both client and server
7. **Security**: Escape user input to prevent XSS attacks

## Common Template Patterns

### Navigation Menu
```html
<nav class="navbar">
    <a href="{{ url_for('index') }}">Home</a>
    <a href="{{ url_for('users_list') }}">Users</a>
</nav>
```

### Flash Messages
```html
{% with messages = get_flashed_messages(with_categories=true) %}
    {% if messages %}
        {% for category, message in messages %}
            <div class="alert alert-{{ category }}">{{ message }}</div>
        {% endfor %}
    {% endif %}
{% endwith %}
```

### Pagination
```html
{% if pagination.has_prev %}
    <a href="{{ url_for('users_list', page=pagination.prev_num) }}">Previous</a>
{% endif %}
```

## Next Steps
After completing this chapter, you should understand:
- How to create and use Jinja2 templates
- Template inheritance and organization
- Passing data between Flask and templates
- Using filters and control structures
- Creating reusable template components
- Handling static files and forms

## Troubleshooting

1. **Template Not Found**: Ensure templates are in the `templates/` directory
2. **Static Files Not Loading**: Check the `static/` directory structure
3. **Template Variables Undefined**: Verify variable names match between Flask and template
4. **Macro Import Errors**: Ensure macro file is in the correct location

## Additional Resources

- [Jinja2 Documentation](https://jinja.palletsprojects.com/)
- [Flask Template Documentation](https://flask.palletsprojects.com/en/2.3.x/templating/)
- [Bootstrap Documentation](https://getbootstrap.com/docs/5.1/)
- [HTML/CSS Basics](https://developer.mozilla.org/en-US/docs/Web/HTML)
