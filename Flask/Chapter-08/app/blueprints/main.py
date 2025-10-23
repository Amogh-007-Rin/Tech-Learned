"""
Main blueprint for general application routes
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app.models import User, Post, Category, Comment
from app import db
from sqlalchemy import desc, func

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Home page"""
    stats = {
        'total_users': User.query.count(),
        'total_posts': Post.query.count(),
        'published_posts': Post.query.filter_by(is_published=True).count(),
        'total_comments': Comment.query.count(),
        'total_categories': Category.query.count()
    }
    
    # Get recent posts
    recent_posts = Post.query.filter_by(is_published=True)\
                           .order_by(desc(Post.created_at))\
                           .limit(5).all()
    
    # Get popular posts
    popular_posts = Post.query.filter_by(is_published=True)\
                            .order_by(desc(Post.view_count))\
                            .limit(5).all()
    
    # Get categories with post counts
    categories = db.session.query(Category, func.count(Post.id).label('post_count'))\
                          .outerjoin(Post)\
                          .group_by(Category.id)\
                          .order_by(desc('post_count')).limit(6).all()
    
    return render_template('index.html',
                         title='Flask Blueprints Demo',
                         stats=stats,
                         recent_posts=recent_posts,
                         popular_posts=popular_posts,
                         categories=categories)

@main_bp.route('/about')
def about():
    """About page"""
    return render_template('about.html', title='About')

@main_bp.route('/contact')
def contact():
    """Contact page"""
    return render_template('contact.html', title='Contact')

@main_bp.route('/posts')
@login_required
def posts_list():
    """List all posts with pagination"""
    page = request.args.get('page', 1, type=int)
    category_id = request.args.get('category', type=int)
    search = request.args.get('search', '')
    
    query = Post.query.filter_by(is_published=True)
    
    # Apply filters
    if category_id:
        query = query.filter_by(category_id=category_id)
    
    if search:
        query = query.filter(Post.title.contains(search) | Post.content.contains(search))
    
    posts = query.order_by(desc(Post.created_at))\
                .paginate(page=page, per_page=10, error_out=False)
    
    # Get categories for filter
    categories = Category.query.filter_by(is_active=True).all()
    
    return render_template('posts.html',
                         posts=posts,
                         categories=categories,
                         title='Posts')

@main_bp.route('/post/<int:post_id>')
@login_required
def post_detail(post_id):
    """Post detail page"""
    post = Post.query.get_or_404(post_id)
    
    # Increment view count
    post.increment_view_count()
    
    # Get comments
    comments = Comment.query.filter_by(post_id=post_id, is_approved=True)\
                          .order_by(Comment.created_at.asc()).all()
    
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

@main_bp.route('/categories')
def categories_list():
    """List all categories"""
    categories = db.session.query(Category, func.count(Post.id).label('post_count'))\
                          .outerjoin(Post)\
                          .group_by(Category.id)\
                          .order_by(desc('post_count')).all()
    
    return render_template('categories.html',
                         categories=categories,
                         title='Categories')

@main_bp.route('/category/<int:category_id>')
def category_detail(category_id):
    """Category detail page"""
    category = Category.query.get_or_404(category_id)
    
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter_by(category_id=category_id, is_published=True)\
                    .order_by(desc(Post.created_at))\
                    .paginate(page=page, per_page=10, error_out=False)
    
    return render_template('category_detail.html',
                         category=category,
                         posts=posts,
                         title=f'Category: {category.name}')

@main_bp.route('/search')
def search():
    """Search functionality"""
    query = request.args.get('q', '')
    page = request.args.get('page', 1, type=int)
    
    results = {}
    if query:
        # Search posts
        posts = Post.query.filter_by(is_published=True)\
                        .filter(Post.title.contains(query) | Post.content.contains(query))\
                        .order_by(desc(Post.created_at))\
                        .paginate(page=page, per_page=10, error_out=False)
        
        # Search users
        users = User.query.filter(User.username.contains(query) | User.first_name.contains(query))\
                        .limit(5).all()
        
        results = {
            'posts': posts,
            'users': users,
            'query': query
        }
    
    return render_template('search.html',
                         results=results,
                         title='Search Results')

@main_bp.route('/profile')
@login_required
def profile():
    """User profile page"""
    user_posts = Post.query.filter_by(author_id=current_user.id)\
                         .order_by(desc(Post.created_at))\
                         .limit(5).all()
    
    user_comments = Comment.query.filter_by(author_id=current_user.id)\
                               .order_by(desc(Comment.created_at))\
                               .limit(5).all()
    
    return render_template('profile.html',
                         user_posts=user_posts,
                         user_comments=user_comments,
                         title='My Profile')

@main_bp.route('/users')
@login_required
def users_list():
    """List all users"""
    page = request.args.get('page', 1, type=int)
    users = User.query.paginate(page=page, per_page=20, error_out=False)
    
    return render_template('users.html',
                         users=users,
                         title='Users')

@main_bp.route('/user/<int:user_id>')
@login_required
def user_detail(user_id):
    """User detail page"""
    user = User.query.get_or_404(user_id)
    
    # Get user's posts
    posts = Post.query.filter_by(author_id=user_id)\
                    .order_by(desc(Post.created_at))\
                    .limit(10).all()
    
    return render_template('user_detail.html',
                         user=user,
                         posts=posts,
                         title=f'User: {user.username}')
