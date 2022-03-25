from datetime import datetime
from fastapi import FastAPI, UploadFile
from keras.models import load_model

import numpy as np
import script.utils
import os

app = FastAPI()
model = load_model('model/model.h5')


@app.get("/")
def read_root():
    return 'Hello World!'


@app.post("/image/")
def create_upload_file(image: UploadFile):
    if not image:
        return {"message": "No upload file sent"}
    else:
        if not os.path.exists("upload"):
            os.mkdir("upload")
        
        file_parts = image.filename.split(".")
        date = str(datetime.timestamp(datetime.now())).replace(".", "-")
        file_name = f'{os.getcwd()}\\upload\\{file_parts[0].replace(" ", "-")}_{date}.{file_parts[1]}'
        script.utils.save_file(file_name, image.file.read())

        image = script.utils.load_image(file_name)
        ans = model.predict(image)
        maping = {0 : "Neutral", 1 : "Porn", 2 : "Sexy"}
        new_ans = np.argmax(ans[0])

        return {
            "result": {
                "class": maping[new_ans],
                "percentage": round((ans[0][new_ans] * 100), 2),
            }
        }