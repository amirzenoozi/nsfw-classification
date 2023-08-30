import cv2
import os
import argparse

"""parsing and configuration"""

def parse_args():
    desc = "Frame Extractor"
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('--frame', type=int, default=1800, help='We Will Extract Frame Every X Frame')
    parser.add_argument('--src', type=str, default='sample.mp4', help='What Is a Video Path?')

    return parser.parse_args()

def main():
    args = parse_args()
    if args is None:
        exit()
    
    # Opens the Video file
    target_directory = 'data/frames'
    file_name = os.path.basename(args.src).split(".")[0]
    cap= cv2.VideoCapture(args.src)
    count = 0
    file_number = 0

    if not os.path.exists(f'{target_directory}/{file_name}'):
        os.makedirs(f'{target_directory}/{file_name}')
        print('Frames Directory Created Successfully!')

    while(cap.isOpened()):
        ret, frame = cap.read()

        if ret:
            cv2.imwrite(f'{target_directory}/{file_name}/frame{file_number}.jpg', frame)
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