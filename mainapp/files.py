import os
from datetime import datetime
from mainapp import app, db

def save_birth_cert(form_data, prim_key):
    _, extn = os.path.splitext(form_data.filename)
    file_name = str(prim_key) + '-birth-cert' + extn
    year = datetime.now().year
    
    current_dir = os.path.join(app.root_path + '/static/birth_certs/' + str(year))
    if not os.path.exists(current_dir):
        os.mkdir(current_dir)

    file_path = os.path.join(current_dir, file_name)
    form_data.save(file_path)

    return file_path

def update_file_name(student, form_data):
    # This enables us to use primary key of Student in the file name.
    # This also saves the file

    db.session.add(student)
    db.session.flush()
    student.birth_cert = save_birth_cert(form_data, student.id)

