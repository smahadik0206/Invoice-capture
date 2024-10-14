from flask import Flask, render_template, request, url_for, redirect
from werkzeug.utils import secure_filename
from main import check_filetype
import os
from parse_result import getKeyValue, dataToTable
from create_db import *
import json

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/getresults')
def getresults():
    return render_template('getresults.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/feedback')
def feedback():
    return render_template('feedback.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

# file input
@app.route('/upload', methods=['POST'])
def get_files():
    if request.method=='POST':
        file = request.files['files']
        filename = file.filename
        print(filename)
        file.save(os.path.join(f'static/pdf/{filename}'))
        # file processing
        print(filename)
        res = check_filetype(f'C:/New folder/Project/Project/static/pdf/{filename}')
        #delete old results
        for file_ in os.listdir('static/Result'):
            try:
                file_path = f'C:/New folder/Project/Project/static/Result/{file_}'
                os.remove(file_path)
            except:
                pass
        print(res)
        # save result
        f = f'static/Result/{filename}.json'
        if os.path.exists(f):
            os.remove(f)
        with open(f,'x') as f:
            json.dump(res, f, indent=4)
        file_submit_noti = f"{filename} file Successfully Processed"
    return render_template('index.html', notification = file_submit_noti, file_name=f'{filename}.json')


# saved to database
@app.route('/saveToDataBase', methods=['POST'])
def save_result():
    for path, dirs, files in os.walk('static/Result'):
        for filename in files:
            if filename.endswith('.json'):
                file_path = os.path.join(path, filename)

    with open(file_path, 'r') as json_file:
        result = json.load(json_file)

    result = getKeyValue(result)

    id = save_to_database(result ,filename)
    if id:
        noti = f"Extracted result saved to database! Your result Id is {id}"
    else:
        noti = "Error occured while data save to database"
    return render_template('index.html', savedToDB_notification = noti, file_name=filename)


@app.route('/savefeedback', methods=['POST'])
def savefeedback():
    if request.method=='POST':
        name = request.form.get('name')
        comments = request.form.get('comments')

        if save_feedback(name, comments) is True:
            noti = "Your feedback has been submitted. Thank you!"
            return render_template('feedback.html', feedback_notification = noti)
        else:
            noti = "Error occured while submitting your feedback"
            return render_template('feedback.html', feedback_notification = noti)


@app.route('/savecontact', methods=['POST'])
def savecontact():
    if request.method=='POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')

        if save_contact(name, email, message) is True:
            noti = "Thank you for contacting us!"
            return render_template('contact.html', contact_notification = noti)
        else:
            noti = "An error occurred while sending your message"
            return render_template('contact.html', contact_notification = noti)
    else:
        noti = "An error occurred while sending your message"
        return render_template('contact.html', contact_notification = noti)


@app.route('/get_data', methods=['POST'])
def get_data():
    if request.method=='POST':
        invoiceid = request.form.get('invoiceid')
        print(invoiceid)
        result = retrive_data(invoiceid)

        file_data, line_items = dataToTable(result)

        dataTodownload = {
            'document_details' : {},
            'line_items' : line_items
        }
        for i in file_data:
            dataTodownload['document_details'].update({i[0]:i[1]})

        columns = []
        if line_items is not None:
            for key in line_items[0].keys():
                columns.append(key)

        file_path = f"static/Result/{invoiceid}.json"
        if not os.path.exists(file_path):
            with open(file_path, 'x') as json_file:
                json.dump(dataTodownload, json_file, indent=4)

        if result:
            return render_template('getresults.html', file_data=file_data, columns=sorted(set(columns)), line_items=line_items, file_name = f"{invoiceid}.json")
        else:
            return render_template('getresults.html', data='result')

if __name__=='__main__':
    app.run(port=5000, debug=True)