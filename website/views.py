"""Books and notes"""
import json
import requests
from flask import Blueprint, jsonify, render_template, request, flash
from flask_login import login_required, current_user
from .models import Book, Note
from . import db


views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    return render_template("home.html")


@views.route('/draft', methods=['GET', 'POST'])
@login_required
def draft():
    if request.method == 'POST':
        about = request.form.get('about')
        note = request.form.get('note')

        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            new_note = Note(about=about, data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')

    return render_template("draft.html", user=current_user)


@views.route('/delete-book', methods=['POST'])
def delete_book():
    book = json.loads(request.data)
    book_id = book['bookId']
    book = Book.query.get(book_id)
    if book:
        if book.user_id == current_user.id:
            db.session.delete(book)
            db.session.commit()
    return jsonify({})


@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    note_id = note['noteId']
    note = Note.query.get(note_id)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
    return jsonify({})


@views.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    if request.method == 'POST':
        # Define a variable with the URL of the API
        name = request.form.get('name')
        author = request.form.get('author')
        api_url = "https://www.googleapis.com/books/v1/volumes?q=" + \
            name + author + "&key=AIzaSyB56VmCX1jXPYWqFj7KDjBSpJRlvOKKjiE"
        # Call the root of the api with GET, store the answer in a response variable
        # This call will return a list of URLs that represent dog pictures
        response = requests.get(api_url)
        # get the result as json
        response_dict = response.json()
        repo_dicts = response_dict['items']
        return render_template("searchResults.html", lenght=len(repo_dicts), repo_dicts=repo_dicts)
    else:
        return render_template("search.html")


@views.route('/searchResults', methods=['GET', 'POST'])
@login_required
def search_results():
    if request.method == 'POST':
        # Then get the data from the form
        google_id = request.form.get('google')
        api_url = "https://www.googleapis.com/books/v1/volumes?q=" + \
            google_id + "&key=AIzaSyB56VmCX1jXPYWqFj7KDjBSpJRlvOKKjiE"
        response = requests.get(api_url)
        response_dict = response.json()
        repo_dicts = response_dict['items']
        repo_dict = repo_dicts[0]
        name = repo_dict['volumeInfo']['title']
        author = repo_dict['volumeInfo']['authors'][0]
        try:
            imageLink = repo_dict['volumeInfo']['imageLinks']['smallThumbnail']
        except:
            imageLink = 'No image'
        book = Book.query.filter_by(name=name).first()
        new_book = Book(name=name, author=author,
                        imageLink=imageLink, user_id=current_user.id)
        db.session.add(new_book)
        db.session.commit()
        flash('Book added!', category='success')
        return render_template("home.html", name=name, author=author, imageLink=imageLink, user=current_user)
    return render_template("search.html")
