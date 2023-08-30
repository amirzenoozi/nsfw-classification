from distutils import extension
from itertools import count
from dotenv import load_dotenv
from tqdm import tqdm

import urllib.request as req

import script.utils
import os
import argparse

config = load_dotenv(".localenv")

"""parsing and configuration"""
def parse_args():
    desc = "Dataset Downloader"
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('--file', type=str, default='', help='We Will Download All URL Inside The .txt File')

    return parser.parse_args()

def file_size_cleaner(directory):
    files = os.listdir(directory)
    for file in tqdm(files, desc='Cleaning Directory ProgressBar'):
        file_size = os.path.getsize(f'{directory}/{file}')

        # Remove Files that are larger than 5MB or less than 3KB 
        if file_size < (3 * 1024) or file_size > (5 * 1024 * 1024):
            os.remove(f'{directory}/{file}')

def main():
    args = parse_args()
    if args is None:
        exit()
    
    count = 1
    file_path = args.file
    lines = script.utils.read_file_line_by_line(file_path)
    folder_name = os.path.basename(file_path).split('.')[0]
    
    if not os.path.exists(f'{os.getenv("DATASET_DIR")}/all/{folder_name}'):
            os.makedirs(f'{os.getenv("DATASET_DIR")}/all/{folder_name}')

    for line in tqdm(lines, desc='Downloading ProgressBar'):
        parse_url = line.strip().split('/')
        file_extension = parse_url[-1].split('.')[-1]
        target_file = f'{os.getenv("DATASET_DIR")}/all/{folder_name}/{count}.{file_extension}'
        if not os.path.isfile(target_file):
            script.utils.download_file_from_url(line.strip(), f'{target_file}')
        count += 1
    
    # Remove All Very Large And Very Small Files From Directory
    file_size_cleaner(f'{os.getenv("DATASET_DIR")}/all/{folder_name}')

if __name__ == '__main__':
    main()