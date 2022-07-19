# import logging
from glob import glob
from numpy import NaN
import pandas as pd

from bs4 import BeautifulSoup
class Quiz: 
    def embed_quiz_func(self,converted_df):
        try:
            final_list = []
            for i in range(len(converted_df)):
                topic_dict = {
                    "title": "",
                    "explanation": "",
                    "options": [
                    {
                        "name": "",
                        "isCorrect": "false"
                    },
                    {
                        "name": "",
                        "isCorrect": "False"
                    },
                    {
                        "name": "",
                        "isCorrect": "False"
                    },
                    {
                        "name": "",
                        "isCorrect": "False"
                    }
                    ]
                }
                topic_dict['title'] = converted_df['title'][i]
                topic_dict['explanation'] = converted_df['explanation'][i]

                topic_dict['options'][0]['name'] = converted_df['option1'][i]
                topic_dict['options'][1]['name'] = converted_df['option2'][i]
                topic_dict['options'][2]['name'] = converted_df['option3'][i]
                topic_dict['options'][3]['name'] = converted_df['option4'][i]

                topic_dict['options'][0]['isCorrect'] = converted_df['isCorrect1'][i]
                topic_dict['options'][1]['isCorrect'] = converted_df['isCorrect2'][i]
                topic_dict['options'][2]['isCorrect'] = converted_df['isCorrect3'][i]
                topic_dict['options'][3]['isCorrect'] = converted_df['isCorrect4'][i]

                final_list.append(topic_dict)
            return final_list

        except Exception as e:
            # logging.info(e)
            raise e
    
    def convert_to_dataframe(self,new_df):
        try:
            answer_explanation = []
            questions_list = []
            option_1 = []
            option_2 = []
            option_3 = []
            option_4 = []
            is_correct1 = []
            is_correct2 = []
            is_correct3 = []
            is_correct4 = []

            print("Started converting to dataframe")
            
            for i in new_df['AnswerExplanation']:
                explanation = BeautifulSoup(str(i), "lxml").text
                if explanation == NaN:
                    answer_explanation.append("NaN")
                else:
                    answer_explanation.append(explanation)

            for i in new_df['Question']:
                questions = BeautifulSoup(str(i), "lxml").text
                if questions == "NaN":
                    print(">>>>>>>option3 is NaN>>>>>>>>>")
                    questions_list.append("NaN")
                else:
                    questions_list.append(questions)

            for i in new_df['Option1']:
                option1 = BeautifulSoup(str(i), "lxml").text
                if option1 == "NaN":
                    option_1.append("NaN")
                else:
                    option_1.append(option1)

            for i in new_df['Option2']:
                option2 = BeautifulSoup(str(i), "lxml").text
                if option2 == "NaN":
                    option_2.append("NaN")
                else:
                    option_2.append(option2)
                    
            for j in new_df['Option3']:
                option3 = BeautifulSoup(str(j), "lxml").text
                if option3 == "NaN":
                    print(">>>>>>>option3 is NaN>>>>>>>>>")
                    option_3.append("NaN")
                else:
                    option_3.append(option3)
            
            for j in new_df['Option4']:
                option4 = BeautifulSoup(str(j), "lxml").text
                if option4 == "NaN":
                    option_4.append("NaN")
                else:
                    option_4.append(option4)

            for index1, k in enumerate(new_df['CorrectOption']):
                # if len(str(k)) == 1:
                    if str(k) == '1':
                        is_correct1.append(True)
                        is_correct2.append(False)
                        is_correct3.append(False)
                        is_correct4.append(False)
                    if str(k) == '2':
                        is_correct1.append(False)
                        is_correct2.append(True)
                        is_correct3.append(False)
                        is_correct4.append(False)
                    if str(k) == '3':
                        is_correct1.append(False)
                        is_correct2.append(False)
                        is_correct3.append(True)
                        is_correct4.append(False)
                    if str(k) == '4':
                        is_correct1.append(False)
                        is_correct2.append(False)
                        is_correct3.append(False)
                        is_correct4.append(True)

            data = {'title': questions_list, 'explanation': answer_explanation, 'option1': option_1,'option2': option_2, \
                            'option3' : option_3, 'option4': option_4, 'isCorrect1': is_correct1, 'isCorrect2': is_correct2, \
                                    'isCorrect3': is_correct3, 'isCorrect4': is_correct4}
            print("Finished converting to dataframe")
            converted_df = pd.DataFrame(data)
            return converted_df
        # handle settingwith copy warning
        except Exception as e:
            # logging.info(e)
            
            raise(e)
    def return_import_data(self, df):
        columns_needed = ['AnswerExplanation', 'Question', 'CorrectOption', 'Option1', 'Option2', 'Option3', 'Option4']
        new_df = df[columns_needed]

        return new_df
    def validate_columns(self, df):
        try:
            for index1, k in enumerate(df['CorrectOption']):
                if len(str(k)) != 1 or str(k) not in ['1', '2', '3', '4']:
                    # remove that row from the data frame
                    print(f"removing row for index {index1} and value {k}")
                    df.drop(index1, inplace=True)
                else:
                    pass
            return df
        except Exception as e:
            if "SettingWithCopyWarning" in str(e):
                pass
            raise(e)
