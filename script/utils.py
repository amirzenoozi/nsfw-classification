from PIL import Image
from skimage import transform

import numpy as np
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import json

def write_json_file(dic, target_file):
    json_object = json.dumps(dic, indent = 4)
    with open("result.json", "w") as outfile:
        outfile.write(json_object)


def load_image(filename):
    np_image = Image.open(filename)
    np_image = np.array(np_image).astype('float32')/255
    np_image = transform.resize(np_image, (224, 224, 3))
    np_image = np.expand_dims(np_image, axis=0)
    img=mpimg.imread(filename)
    plt.imshow(img)
    return np_image