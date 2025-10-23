"""
API blueprint for REST API endpoints
"""
from flask import Blueprint, request, jsonify, current_app
from flask_login import login_required, current_user
from functools import wraps
from app.models import User, Post, Category, Comment
from app import db
from sqlalchemy import desc
import json

api_bp = Blueprint('api', __name__)

def admin_required(f):
    """Decorator to require admin role for API endpoints"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            return jsonify({'error': 'Admin access required'}), 403
        return f(*args, **kwargs)
    return decorated_function

@api_bp.route('/users')
@login_required
def get_users():
    """Get all users (API)"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    users = User.query.paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'users': [{
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'full_name': user.full_name,
            'is_active': user.is_active,
            'is_admin': user.is_admin,
            'created_at': user.created_at.isoformat(),
            'last_login': user.last_login.isoformat() if user.last_login else None
        } for user in users.items],
        'pagination': {
            'page': users.page,
            'pages': users.pages,
            'per_page': users.per_page,
            'total': users.total,
            'has_next': users.has_next,
            'has_prev': users.has_prev
        }
    })

@api_bp.route('/users/<int:user_id>')
@login_required
def get_user(user_id):
    """Get specific user (API)"""
    user = User.query.get_or_404(user_id)
    
    return jsonify({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'bio': user.bio,
        'avatar_url': user.avatar_url,
        'is_active': user.is_active,
        'is_admin': user.is_admin,
        'is_verified': user.is_verified,
        'created_at': user.created_at.isoformat(),
        'updated_at': user.updated_at.isoformat(),
        'last_login': user.last_login.isoformat() if user.last_login else None,
        'login_count': user.login_count
    })

@api_bp.route('/posts')
@login_required
def get_posts():
    """Get all posts (API)"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    category_id = request.args.get('category', type=int)
    published_only = request.args.get('published_only', 'true').lower() == 'true'
    
    query = Post.query
    if published_only:
        query = query.filter_by(is_published=True)
    if category_id:
        query = query.filter_by(category_id=category_id)
    
    posts = query.order_by(desc(Post.created_at))\
                .paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'posts': [{
            'id': post.id,
            'title': post.title,
            'slug': post.slug,
            'excerpt': post.excerpt,
            'content': post.content,
            'featured_image': post.featured_image,
            'is_published': post.is_published,
            'is_featured': post.is_featured,
            'view_count': post.view_count,
            'like_count': post.like_count,
            'reading_time': post.reading_time,
            'created_at': post.created_at.isoformat(),
            'updated_at': post.updated_at.isoformat(),
            'published_at': post.published_at.isoformat() if post.published_at else None,
            'author': {
                'id': post.author.id,
                'username': post.author.username,
                'full_name': post.author.full_name
            },
            'category': {
                'id': post.category.id,
                'name': post.category.name,
                'slug': post.category.slug
            }
        } for post in posts.items],
        'pagination': {
            'page': posts.page,
            'pages': posts.pages,
            'per_page': posts.per_page,
            'total': posts.total,
            'has_next': posts.has_next,
            'has_prev': posts.has_prev
        }
    })

@api_bp.route('/posts/<int:post_id>')
@login_required
def get_post(post_id):
    """Get specific post (API)"""
    post = Post.query.get_or_404(post_id)
    
    return jsonify({
        'id': post.id,
        'title': post.title,
        'slug': post.slug,
        'content': post.content,
        'excerpt': post.excerpt,
        'featured_image': post.featured_image,
        'is_published': post.is_published,
        'is_featured': post.is_featured,
        'view_count': post.view_count,
        'like_count': post.like_count,
        'reading_time': post.reading_time,
        'created_at': post.created_at.isoformat(),
        'updated_at': post.updated_at.isoformat(),
        'published_at': post.published_at.isoformat() if post.published_at else None,
        'author': {
            'id': post.author.id,
            'username': post.author.username,
            'full_name': post.author.full_name,
            'avatar_url': post.author.avatar_url
        },
        'category': {
            'id': post.category.id,
            'name': post.category.name,
            'slug': post.category.slug,
            'color': post.category.color
        },
        'comments': [{
            'id': comment.id,
            'content': comment.content,
            'is_approved': comment.is_approved,
            'created_at': comment.created_at.isoformat(),
            'author': {
                'id': comment.author.id,
                'username': comment.author.username,
                'full_name': comment.author.full_name
            }
        } for comment in post.comments.filter_by(is_approved=True).all()]
    })

@api_bp.route('/categories')
def get_categories():
    """Get all categories (API)"""
    categories = Category.query.filter_by(is_active=True).all()
    
    return jsonify({
        'categories': [{
            'id': category.id,
            'name': category.name,
            'slug': category.slug,
            'description': category.description,
            'color': category.color,
            'post_count': category.posts.count(),
            'created_at': category.created_at.isoformat()
        } for category in categories]
    })

@api_bp.route('/comments')
@login_required
def get_comments():
    """Get all comments (API)"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    post_id = request.args.get('post_id', type=int)
    approved_only = request.args.get('approved_only', 'true').lower() == 'true'
    
    query = Comment.query
    if post_id:
        query = query.filter_by(post_id=post_id)
    if approved_only:
        query = query.filter_by(is_approved=True)
    
    comments = query.order_by(desc(Comment.created_at))\
                  .paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'comments': [{
            'id': comment.id,
            'content': comment.content,
            'is_approved': comment.is_approved,
            'is_spam': comment.is_spam,
            'created_at': comment.created_at.isoformat(),
            'updated_at': comment.updated_at.isoformat(),
            'author': {
                'id': comment.author.id,
                'username': comment.author.username,
                'full_name': comment.author.full_name
            },
            'post': {
                'id': comment.post.id,
                'title': comment.post.title,
                'slug': comment.post.slug
            }
        } for comment in comments.items],
        'pagination': {
            'page': comments.page,
            'pages': comments.pages,
            'per_page': comments.per_page,
            'total': comments.total,
            'has_next': comments.has_next,
            'has_prev': comments.has_prev
        }
    })

@api_bp.route('/stats')
@login_required
def get_stats():
    """Get application statistics (API)"""
    stats = {
        'users': {
            'total': User.query.count(),
            'active': User.query.filter_by(is_active=True).count(),
            'admins': User.query.filter_by(is_admin=True).count()
        },
        'posts': {
            'total': Post.query.count(),
            'published': Post.query.filter_by(is_published=True).count(),
            'featured': Post.query.filter_by(is_featured=True).count()
        },
        'comments': {
            'total': Comment.query.count(),
            'approved': Comment.query.filter_by(is_approved=True).count(),
            'pending': Comment.query.filter_by(is_approved=False).count()
        },
        'categories': {
            'total': Category.query.count(),
            'active': Category.query.filter_by(is_active=True).count()
        }
    }
    
    return jsonify(stats)

@api_bp.route('/user-info')
@login_required
def get_user_info():
    """Get current user information (API)"""
    return jsonify({
        'id': current_user.id,
        'username': current_user.username,
        'email': current_user.email,
        'full_name': current_user.full_name,
        'bio': current_user.bio,
        'avatar_url': current_user.avatar_url,
        'is_admin': current_user.is_admin,
        'is_active': current_user.is_active,
        'is_verified': current_user.is_verified,
        'created_at': current_user.created_at.isoformat(),
        'last_login': current_user.last_login.isoformat() if current_user.last_login else None,
        'login_count': current_user.login_count
    })

@api_bp.errorhandler(404)
def api_not_found(error):
    """API 404 error handler"""
    return jsonify({'error': 'Resource not found'}), 404

@api_bp.errorhandler(500)
def api_internal_error(error):
    """API 500 error handler"""
    return jsonify({'error': 'Internal server error'}), 500
