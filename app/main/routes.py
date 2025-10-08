from flask import (
    Blueprint, render_template,
    flash, redirect, url_for, request, current_app, g
)
from flask_login import current_user, login_required
from flask_babel import get_locale, _
import sqlalchemy as sa
from app.models import db, User, Post, Message, Notification
from .forms import (EditProfileForm, EmptyForm, PostForm,
                    SearchForm, MessageForm)
from datetime import datetime, timezone
from langdetect import detect, LangDetectException
from app.translate import translate

# Define blueprint
routes_bp = Blueprint('routes', __name__)


# We define the routing here
# Index/landing page
@routes_bp.route('/', methods=['GET', 'POST'])
@routes_bp.route('/index', methods=['GET', 'POST'])
@login_required  # We require users to login before viewing this
def index():
    form = PostForm()
    if form.validate_on_submit():
        try:
            language = detect(form.post.data)
        except LangDetectException:
            language = ''
        post = Post(body=form.post.data, author=current_user,
                    language=language)
        db.session.add(post)
        db.session.commit()
        flash('Your post is now live!')
        return redirect(url_for('routes.index'))

    # Pagination
    page = request.args.get('page', 1, type=int)
    posts = db.paginate(current_user.following_posts(),
                        page=page,
                        per_page=current_app.config['POSTS_PER_PAGE'],
                        error_out=False)

    # Add navigation arrows
    next_url = url_for('routes.index', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('routes.index', page=posts.prev_num) \
        if posts.has_prev else None

    return render_template('index.html', title='Home Page',
                           form=form, posts=posts.items,
                           next_url=next_url, prev_url=prev_url)


# User profile page
@routes_bp.route('/user/<username>')
@login_required
def user(username):
    user = db.first_or_404(sa.select(User).where(User.username == username))
    page = request.args.get('page', 1, type=int)
    query = user.posts.select().order_by(Post.timestamp.desc())
    posts = db.paginate(query, page=page,
                        per_page=current_app.config['POSTS_PER_PAGE'],
                        error_out=False)
    # Add navigation arrows
    next_url = url_for('routes.user', username=user.username,
                       page=posts.next_num) if posts.has_next else None
    prev_url = url_for('routes.user', username=user.username,
                       page=posts.prev_num) if posts.has_prev else None
    form = EmptyForm()

    # Add form for follow and unfollow
    form = EmptyForm()
    return render_template('user.html', user=user, posts=posts.items,
                           next_url=next_url, prev_url=prev_url,
                           form=form)


# Record time of last visit
@routes_bp.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.now(timezone.utc)
        db.session.commit()
        g.search_form = SearchForm()
    g.locale = str(get_locale())


# Profile editor page
@routes_bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('routes.edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)


# Add follow route
@routes_bp.route('/follow/<username>', methods=['POST'])
@login_required
def follow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(
                User.username == username
                )
        )
        if user is None:
            flash(f'User {username} not found.')
            return redirect(url_for('routes.index'))
        if user == current_user:
            flash('You cannot follow yourself!')
            return redirect(url_for('routes.user', username=username))
        current_user.follow(user)
        db.session.commit()
        flash(f'You are following {username}!')
        return redirect(url_for('routes.user', username=username))
    else:
        return redirect(url_for('routes.index'))


# Add unfollow route
@routes_bp.route('/unfollow/<username>', methods=['POST'])
@login_required
def unfollow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(
                User.username == username
                )
        )
        if user is None:
            flash(f'User {username} not found.')
            return redirect(url_for('routes.index'))
        if user == current_user:
            flash('You cannot unfollow yourself!')
            return redirect(url_for('routes.user', username=username))
        current_user.unfollow(user)
        db.session.commit()
        flash(f'You are not following {username}')
        return redirect(url_for('routes.user', username=username))
    else:
        return redirect(url_for('routes.index'))


# Explore view function
@routes_bp.route('/explore')
@login_required
def explore():
    page = request.args.get('page', 1, type=int)
    query = sa.select(Post).order_by(Post.timestamp.desc())
    posts = db.paginate(query, page=page,
                        per_page=current_app.config['POSTS_PER_PAGE'],
                        error_out=False)
    # Add navigation arrows
    next_url = url_for('routes.explore', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('routes.explore', page=posts.prev_num) \
        if posts.has_prev else None

    return render_template('index.html', title='Explore', posts=posts.items,
                           next_url=next_url, prev_url=prev_url)


@routes_bp.route("/translate", methods=["POST"])
@login_required
def translate_text():
    data = request.get_json()
    return {'text': translate(
                    data['text'],
                    data['source_language'],
                    data['dest_language']
                    )
            }


# Search
@routes_bp.route('/search')
@login_required
def search():
    if not g.search_form.validate():
        return redirect(url_for('routes.explore'))
    page = request.args.get('page', 1, type=int)
    posts, total = Post.search(g.search_form.q.data, page,
                               current_app.config['POSTS_PER_PAGE'])
    next_url = url_for('routes.search', q=g.search_form.q.data,
                       page=page + 1) if \
        total > page * current_app.config['POSTS_PER_PAGE'] else None
    prev_url = url_for('routes.search', q=g.search_form.q.data,
                       page=page - 1) if \
        page > 1 else None
    return render_template('search.html', title=_('Search'), posts=posts,
                           next_url=next_url, prev_url=prev_url)


# User popup view function
@routes_bp.route('/user/<username>/popup')
@login_required
def user_popup(username):
    user = db.first_or_404(sa.select(User).where(User.username == username))
    form = EmptyForm()
    return render_template('user_popup.html', user=user, form=form)


# Messaging route
@routes_bp.route('/send_message/<recipient>', methods=['GET', 'POST'])
@login_required
def send_message(recipient):
    user = db.first_or_404(sa.select(User).where(User.username == recipient))
    form = MessageForm()
    if form.validate_on_submit():
        msg = Message(author=current_user, recipient=user,
                      body=form.message.data)
        db.session.add(msg)
        user.add_notification('unread_message_count',
                              user.unread_message_count())
        db.session.commit()
        flash(_('Your message has been sent.'))
        return redirect(url_for('routes.user', username=recipient))
    return render_template('send_message.html', title=_('Send Message'),
                           form=form, recipient=recipient)


# View private messages
@routes_bp.route('/messages')
@login_required
def messages():
    current_user.last_message_read_time = datetime.now(timezone.utc)
    current_user.add_notification('unread_message_count', 0)
    db.session.commit()
    page = request.args.get('page', 1, type=int)
    query = current_user.messages_received.select().order_by(
        Message.timestamp.desc())
    messages = db.paginate(query, page=page,
                           per_page=current_app.config['POSTS_PER_PAGE'],
                           error_out=False)
    next_url = url_for('routes.messages', page=messages.next_num) \
        if messages.has_next else None
    prev_url = url_for('routes.messages', page=messages.prev_num) \
        if messages.has_prev else None
    return render_template('messages.html', messages=messages.items,
                           next_url=next_url, prev_url=prev_url)


# Add the notification view function
@routes_bp.route('/notifications')
@login_required
def notifications():
    since = request.args.get('since', 0.0, type=float)
    query = current_user.notifications.select().where(
        Notification.timestamp > since).order_by(
        Notification.timestamp.asc())
    notifications = db.session.scalars(query)
    return [{
            'name': n.name,
            'data': n.get_data(),
            'timestamp': n.timestamp
            } for n in notifications]


# Export post route and view function
@routes_bp.route('/export_posts')
@login_required
def export_posts():
    if current_user.get_task_in_progress('export_posts'):
        flash(_('An export task is currently in progress'))
    else:
        current_user.launch_task('export_posts', _('Exporting posts...'))
        db.session.commit()
    return redirect(url_for('routes.user', username=current_user.username))
