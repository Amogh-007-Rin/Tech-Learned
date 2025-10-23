"""
Chapter 6: Flask Database Integration (SQLAlchemy)
==================================================

This chapter covers:
1. Introduction to SQLAlchemy ORM
2. Database models and relationships
3. Database migrations with Flask-Migrate
4. CRUD operations
5. Database queries and filtering
6. Advanced database features

Prerequisites:
- Basic understanding of Flask
- SQL knowledge
- Python basics

Let's start with a comprehensive Flask app that demonstrates database integration.
"""

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime, date
import os
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import func, desc, asc, and_, or_, not_
from sqlalchemy.orm import joinedload, selectinload

# Create Flask application instance
app = Flask(__name__)

# Database configuration
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "instance", "app.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your-secret-key-here'

# Initialize extensions
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Database Models
class User(db.Model):
    """User model representing users in the system"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(128), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    bio = db.Column(db.Text)
    website = db.Column(db.String(200))
    phone = db.Column(db.String(20))
    birth_date = db.Column(db.Date)
    is_active = db.Column(db.Boolean, default=True)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    posts = db.relationship('Post', backref='author', lazy='dynamic', cascade='all, delete-orphan')
    comments = db.relationship('Comment', backref='author', lazy='dynamic', cascade='all, delete-orphan')
    profile = db.relationship('UserProfile', backref='user', uselist=False, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<User {self.username}>'
    
    def set_password(self, password):
        """Set password hash"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check password hash"""
        return check_password_hash(self.password_hash, password)
    
    @property
    def full_name(self):
        """Get user's full name"""
        return f"{self.first_name} {self.last_name}"
    
    @property
    def age(self):
        """Calculate user's age"""
        if self.birth_date:
            today = date.today()
            return today.year - self.birth_date.year - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))
        return None

class UserProfile(db.Model):
    """User profile model for additional user information"""
    __tablename__ = 'user_profiles'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    avatar_url = db.Column(db.String(200))
    location = db.Column(db.String(100))
    occupation = db.Column(db.String(100))
    interests = db.Column(db.Text)  # JSON string
    social_links = db.Column(db.Text)  # JSON string
    privacy_settings = db.Column(db.Text)  # JSON string
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<UserProfile {self.user_id}>'

class Category(db.Model):
    """Category model for organizing posts"""
    __tablename__ = 'categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    slug = db.Column(db.String(50), unique=True, nullable=False, index=True)
    description = db.Column(db.Text)
    color = db.Column(db.String(7), default='#007bff')  # Hex color
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    posts = db.relationship('Post', backref='category', lazy='dynamic')
    
    def __repr__(self):
        return f'<Category {self.name}>'

class Post(db.Model):
    """Post model for blog posts"""
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False, index=True)
    slug = db.Column(db.String(200), unique=True, nullable=False, index=True)
    content = db.Column(db.Text, nullable=False)
    excerpt = db.Column(db.Text)
    featured_image = db.Column(db.String(200))
    is_published = db.Column(db.Boolean, default=False)
    is_featured = db.Column(db.Boolean, default=False)
    view_count = db.Column(db.Integer, default=0)
    like_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    published_at = db.Column(db.DateTime)
    
    # Foreign Keys
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    
    # Relationships
    comments = db.relationship('Comment', backref='post', lazy='dynamic', cascade='all, delete-orphan')
    tags = db.relationship('Tag', secondary='post_tags', backref='posts', lazy='dynamic')
    
    def __repr__(self):
        return f'<Post {self.title}>'
    
    @property
    def reading_time(self):
        """Estimate reading time in minutes"""
        word_count = len(self.content.split())
        return max(1, word_count // 200)  # Assume 200 words per minute
    
    def increment_view_count(self):
        """Increment view count"""
        self.view_count += 1
        db.session.commit()

class Tag(db.Model):
    """Tag model for post tags"""
    __tablename__ = 'tags'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False, index=True)
    slug = db.Column(db.String(50), unique=True, nullable=False, index=True)
    color = db.Column(db.String(7), default='#6c757d')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Tag {self.name}>'

# Association table for many-to-many relationship between posts and tags
post_tags = db.Table('post_tags',
    db.Column('post_id', db.Integer, db.ForeignKey('posts.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'), primary_key=True)
)

class Comment(db.Model):
    """Comment model for post comments"""
    __tablename__ = 'comments'
    
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    is_approved = db.Column(db.Boolean, default=False)
    is_spam = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Foreign Keys
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('comments.id'))  # For nested comments
    
    # Relationships
    replies = db.relationship('Comment', backref=db.backref('parent', remote_side=[id]), lazy='dynamic')
    
    def __repr__(self):
        return f'<Comment {self.id}>'

# Routes
@app.route('/')
def index():
    """Home page with database statistics"""
    stats = {
        'total_users': User.query.count(),
        'total_posts': Post.query.count(),
        'published_posts': Post.query.filter_by(is_published=True).count(),
        'total_comments': Comment.query.count(),
        'total_categories': Category.query.count(),
        'total_tags': Tag.query.count()
    }
    
    # Get recent posts
    recent_posts = Post.query.filter_by(is_published=True)\
                           .order_by(desc(Post.created_at))\
                           .limit(5).all()
    
    # Get popular posts
    popular_posts = Post.query.filter_by(is_published=True)\
                            .order_by(desc(Post.view_count))\
                            .limit(5).all()
    
    return render_template('index.html',
                         title='Database Demo',
                         stats=stats,
                         recent_posts=recent_posts,
                         popular_posts=popular_posts)

@app.route('/users')
def users_list():
    """Display all users with pagination"""
    page = request.args.get('page', 1, type=int)
    per_page = 10
    
    users = User.query.paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return render_template('users.html',
                         users=users,
                         title='Users')

@app.route('/user/<int:user_id>')
def user_detail(user_id):
    """Display user details with posts and comments"""
    user = User.query.get_or_404(user_id)
    
    # Get user's posts with pagination
    posts_page = request.args.get('posts_page', 1, type=int)
    posts = Post.query.filter_by(author_id=user_id)\
                     .order_by(desc(Post.created_at))\
                     .paginate(page=posts_page, per_page=5, error_out=False)
    
    # Get user's comments
    comments = Comment.query.filter_by(author_id=user_id)\
                          .order_by(desc(Comment.created_at))\
                          .limit(10).all()
    
    return render_template('user_detail.html',
                         user=user,
                         posts=posts,
                         comments=comments,
                         title=f'User: {user.username}')

@app.route('/posts')
def posts_list():
    """Display all posts with filtering and pagination"""
    page = request.args.get('page', 1, type=int)
    category_id = request.args.get('category', type=int)
    tag_id = request.args.get('tag', type=int)
    search = request.args.get('search', '')
    
    query = Post.query.filter_by(is_published=True)
    
    # Apply filters
    if category_id:
        query = query.filter_by(category_id=category_id)
    
    if tag_id:
        query = query.join(post_tags).filter(post_tags.c.tag_id == tag_id)
    
    if search:
        query = query.filter(or_(
            Post.title.contains(search),
            Post.content.contains(search),
            Post.excerpt.contains(search)
        ))
    
    posts = query.order_by(desc(Post.created_at))\
                .paginate(page=page, per_page=10, error_out=False)
    
    # Get categories and tags for filters
    categories = Category.query.filter_by(is_active=True).all()
    tags = Tag.query.all()
    
    return render_template('posts.html',
                         posts=posts,
                         categories=categories,
                         tags=tags,
                         title='Posts')

@app.route('/post/<int:post_id>')
def post_detail(post_id):
    """Display post details with comments"""
    post = Post.query.get_or_404(post_id)
    
    # Increment view count
    post.increment_view_count()
    
    # Get comments with pagination
    comments_page = request.args.get('comments_page', 1, type=int)
    comments = Comment.query.filter_by(post_id=post_id, is_approved=True)\
                          .order_by(asc(Comment.created_at))\
                          .paginate(page=comments_page, per_page=10, error_out=False)
    
    # Get related posts
    related_posts = Post.query.filter_by(category_id=post.category_id)\
                            .filter(Post.id != post_id)\
                            .filter_by(is_published=True)\
                            .limit(3).all()
    
    return render_template('post_detail.html',
                         post=post,
                         comments=comments,
                         related_posts=related_posts,
                         title=post.title)

@app.route('/categories')
def categories_list():
    """Display all categories with post counts"""
    categories = db.session.query(Category, func.count(Post.id).label('post_count'))\
                          .outerjoin(Post)\
                          .group_by(Category.id)\
                          .order_by(desc('post_count')).all()
    
    return render_template('categories.html',
                         categories=categories,
                         title='Categories')

@app.route('/category/<int:category_id>')
def category_detail(category_id):
    """Display category details with posts"""
    category = Category.query.get_or_404(category_id)
    
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter_by(category_id=category_id, is_published=True)\
                    .order_by(desc(Post.created_at))\
                    .paginate(page=page, per_page=10, error_out=False)
    
    return render_template('category_detail.html',
                         category=category,
                         posts=posts,
                         title=f'Category: {category.name}')

@app.route('/tags')
def tags_list():
    """Display all tags with post counts"""
    tags = db.session.query(Tag, func.count(post_tags.c.post_id).label('post_count'))\
                    .outerjoin(post_tags)\
                    .group_by(Tag.id)\
                    .order_by(desc('post_count')).all()
    
    return render_template('tags.html',
                         tags=tags,
                         title='Tags')

@app.route('/tag/<int:tag_id>')
def tag_detail(tag_id):
    """Display tag details with posts"""
    tag = Tag.query.get_or_404(tag_id)
    
    page = request.args.get('page', 1, type=int)
    posts = Post.query.join(post_tags)\
                    .filter(post_tags.c.tag_id == tag_id)\
                    .filter_by(is_published=True)\
                    .order_by(desc(Post.created_at))\
                    .paginate(page=page, per_page=10, error_out=False)
    
    return render_template('tag_detail.html',
                         tag=tag,
                         posts=posts,
                         title=f'Tag: {tag.name}')

@app.route('/search')
def search():
    """Search functionality across posts and users"""
    query = request.args.get('q', '')
    page = request.args.get('page', 1, type=int)
    
    results = []
    if query:
        # Search posts
        posts = Post.query.filter_by(is_published=True)\
                        .filter(or_(
                            Post.title.contains(query),
                            Post.content.contains(query),
                            Post.excerpt.contains(query)
                        ))\
                        .order_by(desc(Post.created_at))\
                        .paginate(page=page, per_page=10, error_out=False)
        
        # Search users
        users = User.query.filter(or_(
            User.username.contains(query),
            User.first_name.contains(query),
            User.last_name.contains(query),
            User.email.contains(query)
        )).limit(5).all()
        
        results = {
            'posts': posts,
            'users': users,
            'query': query
        }
    
    return render_template('search.html',
                         results=results,
                         title='Search Results')

# Database utility routes
@app.route('/create-sample-data')
def create_sample_data():
    """Create sample data for demonstration"""
    try:
        # Create categories
        categories_data = [
            {'name': 'Technology', 'slug': 'technology', 'description': 'Tech news and tutorials', 'color': '#007bff'},
            {'name': 'Lifestyle', 'slug': 'lifestyle', 'description': 'Life tips and advice', 'color': '#28a745'},
            {'name': 'Travel', 'slug': 'travel', 'description': 'Travel guides and experiences', 'color': '#ffc107'},
            {'name': 'Food', 'slug': 'food', 'description': 'Recipes and food reviews', 'color': '#dc3545'},
            {'name': 'Sports', 'slug': 'sports', 'description': 'Sports news and analysis', 'color': '#6f42c1'}
        ]
        
        for cat_data in categories_data:
            if not Category.query.filter_by(slug=cat_data['slug']).first():
                category = Category(**cat_data)
                db.session.add(category)
        
        # Create tags
        tags_data = [
            {'name': 'Python', 'slug': 'python', 'color': '#3776ab'},
            {'name': 'Flask', 'slug': 'flask', 'color': '#000000'},
            {'name': 'Web Development', 'slug': 'web-development', 'color': '#61dafb'},
            {'name': 'Database', 'slug': 'database', 'color': '#336791'},
            {'name': 'Tutorial', 'slug': 'tutorial', 'color': '#28a745'},
            {'name': 'Beginner', 'slug': 'beginner', 'color': '#ffc107'},
            {'name': 'Advanced', 'slug': 'advanced', 'color': '#dc3545'}
        ]
        
        for tag_data in tags_data:
            if not Tag.query.filter_by(slug=tag_data['slug']).first():
                tag = Tag(**tag_data)
                db.session.add(tag)
        
        # Create users
        users_data = [
            {
                'username': 'john_doe',
                'email': 'john@example.com',
                'first_name': 'John',
                'last_name': 'Doe',
                'bio': 'Software developer passionate about Python and Flask',
                'website': 'https://johndoe.dev',
                'birth_date': date(1990, 5, 15)
            },
            {
                'username': 'jane_smith',
                'email': 'jane@example.com',
                'first_name': 'Jane',
                'last_name': 'Smith',
                'bio': 'Web designer and developer',
                'website': 'https://janesmith.design',
                'birth_date': date(1988, 8, 22)
            },
            {
                'username': 'bob_wilson',
                'email': 'bob@example.com',
                'first_name': 'Bob',
                'last_name': 'Wilson',
                'bio': 'Database administrator and Python enthusiast',
                'birth_date': date(1985, 12, 10)
            }
        ]
        
        for user_data in users_data:
            if not User.query.filter_by(username=user_data['username']).first():
                user = User(**user_data)
                user.set_password('password123')
                db.session.add(user)
        
        db.session.commit()
        
        # Create posts
        tech_category = Category.query.filter_by(slug='technology').first()
        lifestyle_category = Category.query.filter_by(slug='lifestyle').first()
        john_user = User.query.filter_by(username='john_doe').first()
        jane_user = User.query.filter_by(username='jane_smith').first()
        
        posts_data = [
            {
                'title': 'Getting Started with Flask',
                'slug': 'getting-started-with-flask',
                'content': 'Flask is a micro web framework written in Python. It is classified as a microframework because it does not require particular tools or libraries...',
                'excerpt': 'Learn the basics of Flask web framework',
                'author_id': john_user.id,
                'category_id': tech_category.id,
                'is_published': True,
                'published_at': datetime.utcnow()
            },
            {
                'title': 'Database Design Best Practices',
                'slug': 'database-design-best-practices',
                'content': 'Good database design is crucial for application performance and maintainability. Here are some best practices...',
                'excerpt': 'Essential tips for designing efficient databases',
                'author_id': bob_user.id if 'bob_user' in locals() else john_user.id,
                'category_id': tech_category.id,
                'is_published': True,
                'published_at': datetime.utcnow()
            },
            {
                'title': 'Healthy Lifestyle Tips',
                'slug': 'healthy-lifestyle-tips',
                'content': 'Maintaining a healthy lifestyle is important for overall well-being. Here are some practical tips...',
                'excerpt': 'Simple ways to improve your daily habits',
                'author_id': jane_user.id,
                'category_id': lifestyle_category.id,
                'is_published': True,
                'published_at': datetime.utcnow()
            }
        ]
        
        for post_data in posts_data:
            if not Post.query.filter_by(slug=post_data['slug']).first():
                post = Post(**post_data)
                db.session.add(post)
        
        db.session.commit()
        
        flash('Sample data created successfully!', 'success')
        
    except Exception as e:
        db.session.rollback()
        flash(f'Error creating sample data: {str(e)}', 'error')
    
    return redirect(url_for('index'))

@app.route('/reset-database')
def reset_database():
    """Reset database (for development only)"""
    try:
        db.drop_all()
        db.create_all()
        flash('Database reset successfully!', 'success')
    except Exception as e:
        flash(f'Error resetting database: {str(e)}', 'error')
    
    return redirect(url_for('index'))

# Error handlers
@app.errorhandler(404)
def not_found(error):
    """Custom 404 error page"""
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    """Custom 500 error page"""
    db.session.rollback()
    return render_template('errors/500.html'), 500

# Database context processors
@app.context_processor
def inject_global_vars():
    """Inject global variables into all templates"""
    return {
        'site_name': 'Flask Database Demo',
        'current_year': datetime.now().year
    }

if __name__ == '__main__':
    # Create necessary directories
    os.makedirs('instance', exist_ok=True)
    os.makedirs('templates', exist_ok=True)
    os.makedirs('templates/models', exist_ok=True)
    os.makedirs('templates/errors', exist_ok=True)
    os.makedirs('static/css', exist_ok=True)
    os.makedirs('static/js', exist_ok=True)
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    # Run the application
    app.run(debug=True, host='0.0.0.0', port=5000)
