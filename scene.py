from scenedetect import VideoManager
from scenedetect import SceneManager
from scenedetect import scene_manager

# For content-aware scene detection:
from scenedetect.detectors import ContentDetector

import argparse
import os

def parse_args():
    desc = "Scene Detection CLI"
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('--threshold', type=float, default=15.0, help='Scene Detection Threshold')
    parser.add_argument('--src', type=str, default='sample.mp4', help='What Is Video PATH?')
    parser.add_argument('--save', type=str, default='data/frames', help='Where Should I Save The JSON File?')

    return parser.parse_args()

def find_scenes(args):
    # Create our video & scene managers, then add the detector.
    video_manager = VideoManager([args.src])
    scene_manager_class = SceneManager()
    scene_manager_class.add_detector(ContentDetector(threshold=args.threshold))

    # Improve processing speed by downscaling before processing.
    video_manager.set_downscale_factor()

    # Start the video manager and perform the scene detection.
    video_manager.start()
    scene_manager_class.detect_scenes(frame_source=video_manager)

    # Each returned scene is a tuple of the (start, end) timecode.
    scenes = scene_manager_class.get_scene_list()
    
    # Make Image Directory To Save Frames
    file_name = os.path.basename(args.src).split(".")[0]
    if not os.path.exists(f'{args.save}/{file_name}'):
        os.makedirs(f'{args.save}/{file_name}')
        print('Frames Directory Created Successfully!')

    scene_manager.save_images(
        scenes,
        video_manager,
        num_images=1,
        frame_margin=1,
        image_extension='jpg',
        encoder_param=95,
        image_name_template='$VIDEO_NAME-Scene-$SCENE_NUMBER-$IMAGE_NUMBER',
        output_dir=f'{args.save}/{file_name}',
        downscale_factor=1,
        show_progress=False,
        scale=None,
        height=None,
        width=None
    )
    with open(f'{args.save}/{file_name}.csv', 'w') as stats_file:
        scene_manager.write_scene_list(stats_file, scenes)
    return scenes

def main():
    args = parse_args()
    if args is None:
        exit()

    find_scenes(args)

if __name__ == '__main__':
    main()