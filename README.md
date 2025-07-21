# view-waymo-tfrecord

A minimal viewer for Waymo TFRecord files that extracts camera frames and LIDAR data to create video outputs.

The tfrecord data format is described here: https://www.tensorflow.org/datasets/catalog/waymo_open_dataset

## Description

This tool processes Waymo Open Dataset TFRecord files and creates MP4 video outputs. It uses TensorFlow and the Waymo Open Dataset libraries to parse the TFRecord format and OpenCV to handle image processing and video creation.

The repository includes two main scripts:

1. **main.py** - Extracts frames from a specified camera to create a video
2. **lidar_video_gen.py** - Processes LIDAR data from the TOP sensor to create a colorized range image video

## Requirements

- Python 3.10 or higher
- Linux operating system (Mac build currently unavailable due to compatibility issues with the Waymo Open Dataset libraries)
- Dependencies:
  - opencv-python (4.8.1.78 or higher)
  - waymo-open-dataset-tf-2-12-0 (1.6.7)

## Important Note

**This repository requires a sample.tfrecord file which is not included due to size constraints.** You must obtain a Waymo Open Dataset TFRecord file separately and place it in the project directory with the name `sample.tfrecord`, or modify the `filename` variable in main.py to point to your TFRecord file.

Waymo Open Dataset files can be downloaded from the [official Waymo Open Dataset website](https://waymo.com/open/) after registration.

## Usage

1. Place your Waymo TFRecord file in the project directory (named as `sample.tfrecord` or update the filename in the code)
2. Run the desired script:

   For camera video:
   ```
   uv sync
   uv run main.py
   ```
   This will generate a video file named `waymo_front_camera.mp4` by default
   
   For LIDAR video:
   ```
   uv sync
   uv run lidar_video_gen.py
   ```
   This will generate a video file named `waymo_lidar_top_padded.mp4` by default

## Configuration

### Camera Video (main.py)

You can modify the following variables in `main.py` to customize the camera video output:

- `filename`: Path to the TFRecord file
- `output_video`: Name of the output video file
- `camera_name`: Which camera to extract (FRONT, FRONT_LEFT, FRONT_RIGHT, SIDE_LEFT, SIDE_RIGHT)

### LIDAR Video (lidar_video_gen.py)

You can modify the following variables in `lidar_video_gen.py` to customize the LIDAR video output:

- `filename`: Path to the TFRecord file
- `output_video`: Name of the output video file
- `desired_width` and `desired_height`: Output video dimensions (default: 1280x720)
- `max_width`: Maximum width for downscaling wide range images
