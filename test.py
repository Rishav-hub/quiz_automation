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
        print(f"Started {file_name}")
        # print('shape:', df.shape)
        quiz = Quiz()
        new_df = quiz.return_import_data(df)

        # testing the convert to dataframe function
        # print(new_df[new_df.isnull().any(axis=1)])
        # validate column
        validate_df = quiz.validate_columns(new_df)
        print('Validated shape:', validate_df.shape)
        # How to divide excel into multiple sheets

        list_of_df = quiz.divide_excel_into_chunks(validate_df ,10)
        # print('List of df shape:', print(list_of_df))
        counter = 0      
        for df_in_chunks in list_of_df:
            # Function to pass the dataframe to the convert to dataframe function
            converted_df = quiz.convert_to_dataframe(df_in_chunks)
            if not os.path.exists(f"master_folder/{file_name}"):
                os.mkdir(f"master_folder/{file_name}")
            if not os.path.exists(f"master_folder/{file_name}/excel_artifacts"):
                os.mkdir(f"master_folder/{file_name}/excel_artifacts")
            converted_df.to_excel(f"master_folder/{file_name}/excel_artifacts/{file_name}_{counter}.xlsx")

            # Function to pass the dataframe and convert to json
            final_list = quiz.embed_quiz_func(converted_df)
            print(f"completed {file_name}")
            if not os.path.exists(f"master_folder/{file_name}/json_artifacts"):
                os.mkdir(f"master_folder/{file_name}/json_artifacts")
            out_file = open(f"master_folder/{file_name}/json_artifacts/{file_name}_{counter}.json", "w", encoding="utf-8")
            json.dump(final_list, out_file, indent = 4, cls=NpEncoder, ensure_ascii=False)
            counter += 1
            out_file.close()
