# NSFW Classification
We Use Pretrained Keras Model to Classify `NSFW` Content


## Requierments
```bash
pip install -r requirements.txt
```

## Classifier CLI Options
```bash
--model     Model File Path                 #default: 'model/model.h5'
--dir       Directory Path To Classify      #default: 'data/frames'
--json      Json File Path                  #default: 'data/frames'
```

Then You Just Need To Run This

```bash
python main.py --dir PATH_TO_YOUR_DIR --model MODEL_FILE --jsob FOLDER_NAME
```

## Frame Extractor CLI Options
```bash
--frame     Frame Threshold     #default: 1800 (Every Minutes)
--src       Video File PATH     #default: 'sample.mp4'
```

Then You Just Need To Run This

```bash
python frame.py --frame FRAME_TH --src VIDEO_FILE
```

## How To Serve Telegram Bot
Firstly, You Need To Get `API_TOKEN` from `Bot_Fother` and put it in `.localenv` File Then You Just Need To Run: 
```bash
python bot.py
```

## Features
- [x] Detect `Neutral` , `Porn` and `Sexy`
- [x] CLI
- [x] Telegram Bot
- [x] Video Files
- [x] Auto Scene Detect 
- [ ] Rest API