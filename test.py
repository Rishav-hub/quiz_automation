from src.embed_quiz import Quiz
import pandas as pd
import json
import os
import glob
import numpy as np
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


if __name__ == "__main__":
    FOLDER_DIR = "uploads/"
    for i in os.listdir(FOLDER_DIR):
        df = pd.read_excel(os.path.join(FOLDER_DIR, i))
        
        # print(i)
        file_name = i.split(".")[0]
        # print(f"Started {file_name}")
        # print('shape:', df.shape)
        quiz = Quiz()
        new_df = quiz.return_import_data(df)

        # testing the convert to dataframe function
        # print(new_df[new_df.isnull().any(axis=1)])
        # validate column
        validate_df = quiz.validate_columns(new_df)
        print('Validated shape:', validate_df.shape)

        # Function to pass the dataframe to the convert to dataframe function
        converted_df = quiz.convert_to_dataframe(validate_df)
        converted_df.to_excel(f"excel_artifacts/{file_name}.xlsx")

        # Function to pass the dataframe and convert to json
        final_list = quiz.embed_quiz_func(converted_df)
        print(f"completed {file_name}")
        out_file = open(f"artifacts/{file_name}.json", "w", encoding="utf-8")
        json.dump(final_list, out_file, indent = 4, cls=NpEncoder, ensure_ascii=False)
        out_file.close()
