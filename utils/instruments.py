from PIL import Image
from skimage import transform
import urllib.request as req

import numpy as np
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import json
import urllib
import sys

def write_json_file(dic, target_file):
    json_object = json.dumps(dic, indent = 4)
    with open(target_file, "w") as outfile:
        outfile.write(json_object)

def save_file(filename, data):
    with open(filename, 'wb') as f:
        f.write(data)

def read_file_line_by_line(file_path):
    file = open(file_path, 'r')
    return file.readlines()

def load_image(filename):
    np_image = Image.open(filename)
    np_image = np.array(np_image).astype('float32')/255
    np_image = transform.resize(np_image, (224, 224, 3))
    np_image = np.expand_dims(np_image, axis=0)
    img=mpimg.imread(filename)
    plt.imshow(img)
    return np_image

def download_file_from_url(url, target):
    try:
        req.urlretrieve(url, target)
    except urllib.error.HTTPError as err:
        # print('========================')
        # print(f'Error Code: {err.getcode()}')
        # print(f'Target URL: {url}' )
        # print('========================')
        # print('\n')
        pass
    except urllib.error.URLError as err:
        # print('========================')
        # print(f'Error Code: WinError 10060 - Connection Problem')
        # print(f'Target URL: {url}' )
        # print('========================')
        # print('\n')
        pass
    except Exception as e:
        # print('========================')
        # print(f'Error Code: Unknown Error')
        # print(f'Target URL: {url}' )
        # print('========================')
        # print('\n')
        pass
    except KeyboardInterrupt:
        sys.exit()
        pass
    return True
