# view-waymo-tfrecord

A minimal viewer for Waymo TFRecord files that extracts camera frames and creates a video output.

## Description

This tool processes Waymo Open Dataset TFRecord files and extracts frames from a specified camera to create an MP4 video output. It uses TensorFlow and the Waymo Open Dataset libraries to parse the TFRecord format and OpenCV to handle image processing and video creation.

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
2. Run the script:
   ```
   uv sync
   uv run main.py
   ```
3. The script will generate a video file named `waymo_front_camera.mp4` by default

## Configuration

You can modify the following variables in `main.py` to customize the output:

- `filename`: Path to the TFRecord file
- `output_video`: Name of the output video file
- `camera_name`: Which camera to extract (FRONT, FRONT_LEFT, FRONT_RIGHT, SIDE_LEFT, SIDE_RIGHT)