# import logging
from glob import glob
import pandas as pd
class Quiz: 
    def embed_quiz_func(self,df):
        try:
            final_list = []
            for i in range(len(df)):
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
                topic_dict['title'] = df['title'][i]
                topic_dict['explanation'] = df['explanation'][i]

                topic_dict['options'][0]['name'] = df['option1'][i]
                topic_dict['options'][1]['name'] = df['option2'][i]
                topic_dict['options'][2]['name'] = df['option3'][i]
                topic_dict['options'][3]['name'] = df['option4'][i]

                topic_dict['options'][0]['isCorrect'] = df['isCorrect1'][i]
                topic_dict['options'][1]['isCorrect'] = df['isCorrect2'][i]
                topic_dict['options'][2]['isCorrect'] = df['isCorrect3'][i]
                topic_dict['options'][3]['isCorrect'] = df['isCorrect4'][i]

                final_list.append(topic_dict)
            return final_list

        except Exception as e:
            # logging.info(e)
            raise e