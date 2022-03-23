from keras.models import load_model

import numpy as np
import warnings
import os

import script.utils

warnings.filterwarnings("ignore")
model = load_model("model/model.h5")
frames_path = 'data/frames/' 

response  = {}
frames = os.listdir(frames_path)
for item in frames:
        if os.path.isfile(frames_path+item):
            image = script.utils.load_image(frames_path+item)
            ans = model.predict(image)
            maping = {0 : "Neutral", 1 : "Porn", 2 : "Sexy"}
            new_ans = np.argmax(ans[0])

            item_key_name = item.split('.')
            response[item_key_name[0]] = {
                "neutral": round((ans[0][0] * 100), 2),
                "porn": round((ans[0][1] * 100), 2),
                "sexy": round((ans[0][2] * 100), 2),
            }

            # print(maping[new_ans], np.round(ans,2))
            # print(f'{item}: With {ans[0][new_ans]} probability')

script.utils.write_json_file(response, "result.json")