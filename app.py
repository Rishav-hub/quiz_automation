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
download_folder_json = "artifacts/"
download_folder_excel = "excel_artifacts/"
if not os.path.exists(download_folder_json):
    os.mkdir(download_folder_json)
if not os.path.exists(download_folder_excel):
    os.mkdir(download_folder_excel)

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
            for i in glob.glob(download_folder_json + '*.json'): 
                os.remove(i)
            for i in glob.glob(download_folder_excel + '*.xlsx'): 
                os.remove(i)
            df = pd.read_excel(file_path)
            quiz = Quiz()
            new_df = quiz.return_import_data(df)
            validate_df = quiz.validate_columns(new_df)

            # Function to pass the dataframe to the convert to dataframe function
            converted_df = quiz.convert_to_dataframe(validate_df)
            converted_df.to_excel(f"excel_artifacts/{file_name}.xlsx", index=False)
            # Function to pass the dataframe and convert to json
            final_list = quiz.embed_quiz_func(converted_df)
            out_file = open(f"artifacts/{file_name}.json", "w", encoding="utf-8")
            json.dump(final_list, out_file, indent = 4, cls=NpEncoder, ensure_ascii=False)
            out_file.close()
            return render_template('embed.html')
        except Exception as e:
            raise(e)
    else:
        render_template('embed.html')

# Sending the file to the user
@app.route('/download_json')
def download_json():
    file_name = os.listdir('artifacts')[0]
    download_folder_1 = f'artifacts/{file_name}'
    return send_file(download_folder_1, as_attachment=True)

@app.route('/download_excel')
def download_excel():
    file_name = os.listdir('excel_artifacts')[0]
    download_folder_1 = f'excel_artifacts/{file_name}'
    return send_file(download_folder_1, as_attachment=True)
if __name__ == '__main__':
    app.run()  # running the flask app
