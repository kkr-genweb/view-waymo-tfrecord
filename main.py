import tensorflow as tf
from waymo_open_dataset import dataset_pb2 as open_dataset
import numpy as np
import cv2

# ------------------------------
# CONFIG
# ------------------------------
filename = "sample.tfrecord"
output_video = "waymo_front_camera.mp4"
camera_name = open_dataset.CameraName.FRONT  # or FRONT_LEFT, etc.

# ------------------------------
# Read dataset
# ------------------------------
dataset = tf.data.TFRecordDataset(filename, compression_type='')

# ------------------------------
# Setup video writer
# ------------------------------
# Initialize these once you have the first frame's shape
video_writer = None

# ------------------------------
# Iterate frames
# ------------------------------
for idx, data in enumerate(dataset):
    frame = open_dataset.Frame()
    frame.ParseFromString(data.numpy()) 
    print(f"Frame {idx} timestamp: {frame.timestamp_micros}")

    # Find the camera image matching our desired camera
    image = next((img for img in frame.images if img.name == camera_name), None)
    if image is None:
        print(f"No camera {camera_name} found in frame {idx}")
        continue

    # Decode JPEG bytes
    img_np = np.frombuffer(image.image, dtype=np.uint8)
    img_decoded = cv2.imdecode(img_np, cv2.IMREAD_COLOR)

    # Initialize writer if first frame
    if video_writer is None:
        height, width, _ = img_decoded.shape
        fps = 10  # Waymo dataset is 10 Hz
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        video_writer = cv2.VideoWriter(output_video, fourcc, fps, (width, height))

    # Write frame
    video_writer.write(img_decoded)

    print(f"Wrote frame {idx} to video")

# ------------------------------
# Finalize
# ------------------------------
if video_writer:
    video_writer.release()
    print(f"Video saved to {output_video}")
else:
    print("No frames were written.")
