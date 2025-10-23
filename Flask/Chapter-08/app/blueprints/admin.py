"""
Admin blueprint for administrative functions
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from functools import wraps
from app.models import User, Post, Category, Comment
from app import db
from sqlalchemy import desc, func

admin_bp = Blueprint('admin', __name__)

def admin_required(f):
    """Decorator to require admin role"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('Admin access required.', 'error')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/')
@admin_required
def dashboard():
    """Admin dashboard"""
    stats = {
        'total_users': User.query.count(),
        'active_users': User.query.filter_by(is_active=True).count(),
        'admin_users': User.query.filter_by(is_admin=True).count(),
        'total_posts': Post.query.count(),
        'published_posts': Post.query.filter_by(is_published=True).count(),
        'total_comments': Comment.query.count(),
        'approved_comments': Comment.query.filter_by(is_approved=True).count(),
        'total_categories': Category.query.count()
    }
    
    recent_users = User.query.order_by(desc(User.created_at)).limit(5).all()
    recent_posts = Post.query.order_by(desc(Post.created_at)).limit(5).all()
    recent_comments = Comment.query.order_by(desc(Comment.created_at)).limit(5).all()
    
    return render_template('admin/dashboard.html',
                         stats=stats,
                         recent_users=recent_users,
                         recent_posts=recent_posts,
                         recent_comments=recent_comments,
                         title='Admin Dashboard')

@admin_bp.route('/users')
@admin_required
def users():
    """Admin user management"""
    page = request.args.get('page', 1, type=int)
    users = User.query.paginate(page=page, per_page=20, error_out=False)
    
    return render_template('admin/users.html',
                         users=users,
                         title='User Management')

@admin_bp.route('/user/<int:user_id>/toggle-status')
@admin_required
def toggle_user_status(user_id):
    """Toggle user active status"""
    user = User.query.get_or_404(user_id)
    user.is_active = not user.is_active
    db.session.commit()
    
    status = 'activated' if user.is_active else 'deactivated'
    flash(f'User {user.username} has been {status}.', 'success')
    
    return redirect(url_for('admin.users'))

@admin_bp.route('/user/<int:user_id>/toggle-admin')
@admin_required
def toggle_user_admin(user_id):
    """Toggle user admin status"""
    user = User.query.get_or_404(user_id)
    if user.id == current_user.id:
        flash('You cannot change your own admin status.', 'error')
        return redirect(url_for('admin.users'))
    
    user.is_admin = not user.is_admin
    db.session.commit()
    
    status = 'granted admin privileges' if user.is_admin else 'removed admin privileges'
    flash(f'User {user.username} has been {status}.', 'success')
    
    return redirect(url_for('admin.users'))

@admin_bp.route('/posts')
@admin_required
def posts():
    """Admin post management"""
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(desc(Post.created_at))\
                    .paginate(page=page, per_page=20, error_out=False)
    
    return render_template('admin/posts.html',
                         posts=posts,
                         title='Post Management')

@admin_bp.route('/post/<int:post_id>/toggle-published')
@admin_required
def toggle_post_published(post_id):
    """Toggle post published status"""
    post = Post.query.get_or_404(post_id)
    post.is_published = not post.is_published
    if post.is_published and not post.published_at:
        post.published_at = datetime.utcnow()
    db.session.commit()
    
    status = 'published' if post.is_published else 'unpublished'
    flash(f'Post "{post.title}" has been {status}.', 'success')
    
    return redirect(url_for('admin.posts'))

@admin_bp.route('/comments')
@admin_required
def comments():
    """Admin comment management"""
    page = request.args.get('page', 1, type=int)
    comments = Comment.query.order_by(desc(Comment.created_at))\
                          .paginate(page=page, per_page=20, error_out=False)
    
    return render_template('admin/comments.html',
                         comments=comments,
                         title='Comment Management')

@admin_bp.route('/comment/<int:comment_id>/toggle-approved')
@admin_required
def toggle_comment_approved(comment_id):
    """Toggle comment approved status"""
    comment = Comment.query.get_or_404(comment_id)
    comment.is_approved = not comment.is_approved
    db.session.commit()
    
    status = 'approved' if comment.is_approved else 'unapproved'
    flash(f'Comment has been {status}.', 'success')
    
    return redirect(url_for('admin.comments'))

@admin_bp.route('/categories')
@admin_required
def categories():
    """Admin category management"""
    categories = Category.query.order_by(Category.name).all()
    
    return render_template('admin/categories.html',
                         categories=categories,
                         title='Category Management')

@admin_bp.route('/category/<int:category_id>/toggle-active')
@admin_required
def toggle_category_active(category_id):
    """Toggle category active status"""
    category = Category.query.get_or_404(category_id)
    category.is_active = not category.is_active
    db.session.commit()
    
    status = 'activated' if category.is_active else 'deactivated'
    flash(f'Category "{category.name}" has been {status}.', 'success')
    
    return redirect(url_for('admin.categories'))

@admin_bp.route('/statistics')
@admin_required
def statistics():
    """Admin statistics page"""
    # User statistics
    user_stats = {
        'total': User.query.count(),
        'active': User.query.filter_by(is_active=True).count(),
        'admins': User.query.filter_by(is_admin=True).count(),
        'verified': User.query.filter_by(is_verified=True).count(),
        'new_this_month': User.query.filter(User.created_at >= datetime.utcnow().replace(day=1)).count()
    }
    
    # Post statistics
    post_stats = {
        'total': Post.query.count(),
        'published': Post.query.filter_by(is_published=True).count(),
        'drafts': Post.query.filter_by(is_published=False).count(),
        'featured': Post.query.filter_by(is_featured=True).count(),
        'new_this_month': Post.query.filter(Post.created_at >= datetime.utcnow().replace(day=1)).count()
    }
    
    # Comment statistics
    comment_stats = {
        'total': Comment.query.count(),
        'approved': Comment.query.filter_by(is_approved=True).count(),
        'pending': Comment.query.filter_by(is_approved=False).count(),
        'spam': Comment.query.filter_by(is_spam=True).count(),
        'new_this_month': Comment.query.filter(Comment.created_at >= datetime.utcnow().replace(day=1)).count()
    }
    
    return render_template('admin/statistics.html',
                         user_stats=user_stats,
                         post_stats=post_stats,
                         comment_stats=comment_stats,
                         title='Statistics')
