import cv2
import os
import argparse
import uuid

"""parsing and configuration"""

def parse_args():
    desc = "Frame Extractor"
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('--frame', type=int, default=1800, help='We Will Extract Frame Every X Frame')
    parser.add_argument('--src', type=str, default='', help='What Is a Video Path?')
    parser.add_argument('--dir', type=str, default='', help='Save Frames Folder Name')

    return parser.parse_args()

def main():
    args = parse_args()
    if not args.src:
        exit()
    
    # Opens the Video file
    target_directory = 'data/frames'
    cap= cv2.VideoCapture(args.src)
    frame_folder = args.dir or str(uuid.uuid4())
    count = 0
    file_number = 0

    if not os.path.exists(f'{target_directory}/{frame_folder}'):
        os.makedirs(f'{target_directory}/{frame_folder}')
        print('Frames Directory Created Successfully!')

    while(cap.isOpened()):
        ret, frame = cap.read()

        if ret:
            cv2.imwrite(f'{target_directory}/{frame_folder}/frame{file_number}.jpg', frame)
            file_number += 1
            count += args.frame # i.e. at 30 fps, this advances one second
            cap.set(1, count)
        else:
            cap.release()
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()