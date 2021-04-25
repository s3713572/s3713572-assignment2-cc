from flask import render_template, request, url_for, redirect, flash, session
from music import app
from music.models import Login, Music, Subscription
from music.forms import LoginForm, RegistrationForm
from music.helpers.login_manager import is_login_match, is_login_exist
from music.helpers.register_manager import create_item
from music.helpers.home_manager import filt_music, fetch_musics, MusicsHelper, onlick_subscription_button
from music.helpers.subscription_manger import remove_music
from flask_paginate import Pagination, get_page_args
from boto3.dynamodb.conditions import Key, Attr


@app.route('/', methods=['GET','POST'])
def login():
    session.pop('user_name',None)
    session.pop('email', None)
    form = LoginForm()
    if request.method == 'POST':
        if is_login_exist(form.email.data) and is_login_match(form.email.data, form.password.data) and form.validate_on_submit():
            current_user = Login.find(form.email.data)
            session['user_name'] = current_user.user_name
            session['email'] = current_user.email
            flash(f'Login successfully!!','success')
            return redirect(url_for('main'))
        else:
            flash(f'Login failed, Please check your input', 'danger')
            return render_template('login.html',form=form, title="login")
    return render_template('login.html',form=form, title="login")

@app.route('/register', methods=['GET','POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        create_item(form.email.data, form.user_name.data, form.password.data)
        flash(f'Register successfully!','success')
        return redirect(url_for('login'))
    return render_template('register.html',form=form, title="register")


@app.route('/main', methods=['POST', 'GET'])
def main(page_num=1):
    if session['user_name'] == None:
        flash(f'Please login first', 'success')
        return redirect(url_for('login'))
    musics = function_to_run_only_once(session['email'])

    page, per_page, offset = get_page_args(page_parameter='page',per_page_parameter='per_page')
    total = len(musics)
    pagination_users = get_user_index(offset=offset, per_page=per_page, email=session['email'])
    pagination = Pagination(page=page, per_page=per_page, total=total,css_framework='bootstrap4')


    return render_template('main.html', title="main", musics=pagination_users,page=page,per_page=per_page,pagination=pagination)

@app.before_first_request
def function_to_run_only_once(email=None):
    musics = fetch_musics(email)
    return musics


def get_user_index(offset=0, per_page=10, email=None):
    musics = fetch_musics(email)
    return musics[offset: offset + per_page]

@app.route('/button_status_change/<string:music_id>/<string:button_status>', methods=['GET','POST'])
def subscript(music_id,button_status):
    if onlick_subscription_button(button_status, music_id, session['email']) == "Subscript":
        flash(f"Subscripted successfully1","success")
        return redirect(url_for('main'))
    if onlick_subscription_button(button_status, music_id, session['email']) == "de-Subscript":
        flash(f"Cancel Subscription successfully1","success")
        return redirect(url_for('main'))
    return redirect(url_for('main'))


@app.route('/search')
def search(page_num=1):
    if session['user_name'] == None:
        flash(f'Please login first', 'success')
        return redirect(url_for('login'))
    notification = ""
    musics = filt_music(request.args.get('title'), request.args.get('artist'), request.args.get('year'), session['email'])

    if len(musics) == 0:
        notification = "No result is  retrieved. Please query again"
    page, per_page, offset = get_page_args(page_parameter='page',per_page_parameter='per_page')
    total = len(list(musics))
    pagination_users = musics[offset: 0 + 10]
    pagination = Pagination(page=page, per_page=per_page, total=total,css_framework='bootstrap4')
    
    return render_template('main.html',musics=pagination_users,page=page,per_page=per_page,pagination=pagination,notification=notification)


@app.route('/subscription', methods=['GET','POST'])
def subscription():
    if session['user_name'] == None:
        flash(f'Please login first', 'success')
        return redirect(url_for('login'))
    
    subscriptions = Subscription.where(Attr('email').eq(session['email']))
    musics = []

    for subscription in subscriptions:
        music = Music.find(subscription.music_id)
        musics.append(music)

    return render_template('subscription.html', title="subscription", musics=musics)

@app.route('/remove/<string:music_id>')
def remove(music_id):
    if session['user_name'] == None:
        flash(f'Please login first', 'success')
        return redirect(url_for('login'))
    remove_music(music_id,session['email'])
    flash('removed successfully!','success')
    return redirect(url_for('subscription'))


@app.route('/logout')
def logout():
    session.pop('user_name', None)
    session.pop('email', None)
    flash('Logout successfully!', 'success')
    return redirect(url_for('login'))