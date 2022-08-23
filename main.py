from keras.models import load_model

import numpy as np
import argparse
import warnings
import os

import script.utils

def parse_args():
    desc = "NSFW Classification"
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('--model', type=str, default='model/model.h5', help='Where Is Model File?')
    parser.add_argument('--dir', type=str, default='data/frames', help='What Is Images Directory?')
    parser.add_argument('--json', type=str, default='data/frames', help='Where Should I Save The JSON File?')

    return parser.parse_args()

def main():
    args = parse_args()
    if args is None:
        exit()

    warnings.filterwarnings("ignore")
    model = load_model(args.model)
    frames_path = args.dir

    response  = {}
    frames = os.listdir(frames_path)
    folder_name = os.path.basename(frames_path)
    for item in frames:
        if os.path.isfile(f'{frames_path}/{item}'):
            image = script.utils.load_image(f'{frames_path}/{item}')
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

    script.utils.write_json_file(response, f'{args.json}/{folder_name}_result.json')

if __name__ == '__main__':
    main()