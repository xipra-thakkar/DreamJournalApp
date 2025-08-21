from datetime import date
from flask import Blueprint, flash, jsonify, render_template, request
from flask_login import login_required, current_user
from .models import Note
from . import db
import json

views=Blueprint('views', __name__)

@views.route('/')
def index():
    return render_template('index.html')

@views.route('/notes', methods=['GET', 'POST'])
@login_required
def notes():
    if request.method=='POST':
        note = request.form.get('note')
        if len(note)<1:
            flash('Note is too short or empty.')
        else:
            new_note = Note(note=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            print(new_note)
            flash('Note added successfully.', category='success')
    return render_template('notes.html', user=current_user)

@views.route('/delete-note', methods=['POST'])
@login_required
def delete_note():
    data = request.get_json()
    note_id = data.get('noteId')
    
    print(f"Received noteId: {note_id}")  # Debug log

    note = Note.query.get(note_id)
    if note and note.user_id == current_user.id:
        db.session.delete(note)
        db.session.commit()
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'error': 'Note not found or unauthorized'}), 403

    
@views.route('/edit-note', methods=['POST'])
@login_required
def edit_note():
    data = json.loads(request.data)
    note_id = data['noteId']
    new_note_text = data['note']

    note = Note.query.get(note_id)

    # Ensure the note exists and the user has permission to edit it
    if note and note.user_id == current_user.id:
        note.note = new_note_text  # Update the note text
        db.session.commit()
        return jsonify({}), 200  # Success
    return jsonify({"error": "Note not found or unauthorized"}), 403
