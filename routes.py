from flask import Blueprint, render_template, redirect, url_for, flash, send_file, request
from flask_login import login_required, current_user
from dbmodels import db, File, Log, User, Access
from forms import UploadForm
import os

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
@login_required
def index():
    """
    back for homepage
    """
    accessible_files = File.query.join(Access, File.id == Access.file_id).filter(Access.user_id == current_user.id).all()
    uploaded_files = File.query.filter_by(user_id=current_user.id).all()
    files = set(accessible_files).union(set(uploaded_files))

    #count downloads of file
    download_stats = {}
    for file_entry in files:
        download_count = Log.query.filter_by(file_id=file_entry.id).count()
        download_stats[file_entry.filename] = download_count

    return render_template('index.html', user=current_user, files=files, download_stats=download_stats)

@main_bp.route('/admin')
@login_required
def admin():
    """
    statistic and logs
    """
    if not current_user.is_admin:
        return redirect(url_for('main.dashboard'))

    search_query = request.args.get('search', '')
    query = Log.query.filter(Log.action.like('Downloaded%'))

    if search_query:
        query = query.join(User).filter((User.username.like(f'%{search_query}%')))

    logs = query.order_by(Log.timestamp.desc()).all()

    users = User.query.all()

    #count downloads of file
    download_stats = {}
    for user in users:
        download_count = Log.query.filter_by(user_id=user.id).count()
        download_stats[user.username] = download_count

    return render_template('admin.html', logs=logs, users=users, download_stats=download_stats, search_query=search_query)

@main_bp.route('/logs/<int:file_id>')
@login_required
def logs(file_id):
    """
    Logs for specific file
    """
    if not current_user.is_admin:
        return redirect(url_for('main.index'))

    logs = Log.query.filter_by(file_id=file_id).order_by(Log.timestamp.desc()).all()
    file = File.query.get_or_404(file_id)

    #count downloads of file
    files = File.query.all()
    download_stats = {}
    for file_entry in files:
        download_count = Log.query.filter_by(file_id=file_entry.id).count()
        download_stats[file_entry.filename] = download_count

    return render_template('logs.html', logs=logs, file=file, download_stats=download_stats)

@main_bp.route('/upload', methods=['GET', 'POST'])
@login_required
def upload_file():
    """
    Handle file uploads.
    """
    form = UploadForm()
    if form.validate_on_submit():
        file = form.file.data
        if file:
            user_folder = os.path.join('uploads', str(current_user.id))
            if not os.path.exists(user_folder):
                os.makedirs(user_folder)
            filename = file.filename
            filepath = os.path.join(user_folder, filename)
            file.save(filepath)
            new_file = File(filename=filename, filepath=filepath, user_id=current_user.id)
            db.session.add(new_file)
            db.session.commit()
            flash('File uploaded successfully')
            return redirect(url_for('main.index'))
    return render_template('upload.html', form=form)

@main_bp.route('/download/<int:file_id>')
@login_required
def download_file(file_id):
    """
    Handle file downloads.
    """
    file = File.query.get_or_404(file_id)

    if not (current_user.is_admin or Access.query.filter_by(user_id=current_user.id, file_id=file.id).first() or file.user_id == current_user.id):
        flash('You do not have permission to download this file')
        return redirect(url_for('main.index'))
    
    return send_file(file.filepath, as_attachment=True, download_name=file.filename)

@main_bp.route('/delete/<int:file_id>')
@login_required
def delete_file(file_id):
    """
    Handle file deletions.
    """
    file = File.query.get_or_404(file_id)
    if file.user_id != current_user.id and not current_user.is_admin:
        flash('You do not have permission to delete this file')
        return redirect(url_for('main.index'))

    #delete file info from database
    Access.query.filter_by(file_id=file_id).delete()
    db.session.commit()
    Log.query.filter_by(file_id=file_id).delete()
    db.session.commit()
    db.session.delete(file)
    db.session.commit()

    #delete from file system
    file_path = file.filepath
    if os.path.exists(file_path):
        os.remove(file_path)

    flash('File deleted successfully')
    return redirect(url_for('main.index'))

@main_bp.route('/edit_access/<int:file_id>', methods=['GET', 'POST'])
@login_required
def edit_file(file_id):
    """
    Back for edit access of file
    """
    if not current_user.is_admin:
        return redirect(url_for('main.index'))

    file = File.query.get_or_404(file_id)
    users = User.query.filter_by(is_admin=False).all()
    access_list = Access.query.filter_by(file_id=file_id).all()
    granted_users = [access.user_id for access in access_list]

    if request.method == 'POST':
        for user in users:
            if str(user.id) in request.form:
                if user.id not in granted_users:
                    new_access = Access(user_id=user.id, file_id=file.id)
                    db.session.add(new_access)
            else:
                access_to_remove = Access.query.filter_by(user_id=user.id, file_id=file.id).first()
                if access_to_remove:
                    db.session.delete(access_to_remove)
        db.session.commit()
        flash('Access permissions updated successfully')
        return redirect(url_for('main.logs', file_id=file.id))

    return render_template('edit.html', file=file, users=users, granted_users=granted_users)
