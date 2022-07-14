import os
from flask import Flask, render_template, request, send_file, redirect,flash
from werkzeug.utils import secure_filename
from flask_cors import CORS, cross_origin
import numpy as np
import json
import datetime
import glob
import pandas as pd

from src.embed_quiz import Quiz

# initialising the flask app
app = Flask(__name__)
CORS(app)
# Creating the upload folder
XLSX_FILE_DIR = "uploads/"
download_folder = "artifacts/"
if not os.path.exists(download_folder):
    os.mkdir(download_folder)

class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.bool_):
            return bool(obj)
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)

@app.route('/')
@cross_origin()
def index():
    return render_template('embed.html')

@app.route('/embed_engine', methods=['POST', 'GET'])
@cross_origin()
def embedfile():
    if request.method == 'POST':
        try:
            f = request.files['fileupload']
            os.makedirs(XLSX_FILE_DIR, exist_ok=True)
            for i in glob.glob(XLSX_FILE_DIR + '*.xlsx'): 
                os.remove(i)
            file_path = os.path.join(XLSX_FILE_DIR, f.filename)
            f.save(file_path)
            file_name = f.filename.split(".")[0].replace(" ", "_")
            print(file_name)
            cleandir = 'artifacts/'
            for i in glob.glob(cleandir + '*.json'): 
                os.remove(i)
            df = pd.read_excel(file_path)
            quiz = Quiz()
            final_list = quiz.embed_quiz_func(df)
            out_file = open(f"artifacts/{file_name}.json", "w")
            json.dump(final_list, out_file, indent = 4, cls=NpEncoder)
            out_file.close()
            return render_template('embed.html')
        except Exception as e:
            raise(e)
    else:
        render_template('embed.html')

# Sending the file to the user
@app.route('/download')
def download():
    file_name = os.listdir('artifacts')[0]
    download_folder_1 = f'artifacts/{file_name}'
    return send_file(download_folder_1, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)  # running the flask app
