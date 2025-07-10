import tensorflow as tf
from waymo_open_dataset import dataset_pb2 as open_dataset
from waymo_open_dataset.utils import range_image_utils, transform_utils
import numpy as np
import cv2
import zlib

# ------------------------------
# CONFIG
# ------------------------------
filename = "sample.tfrecord"
output_video = "waymo_lidar_top_padded.mp4"

# Desired output dimensions (standard HD)
desired_width = 1280
desired_height = 720

# ------------------------------
# Read dataset
# ------------------------------
dataset = tf.data.TFRecordDataset(filename, compression_type='')

# ------------------------------
# Setup video writer
# ------------------------------
video_writer = None

# ------------------------------
# Iterate frames
# ------------------------------
for idx, data in enumerate(dataset):
    frame = open_dataset.Frame()
    frame.ParseFromString(data.numpy())
    print(f"Frame {idx} timestamp: {frame.timestamp_micros}")

    # Get TOP LiDAR range image
    laser = [l for l in frame.lasers if l.name == open_dataset.LaserName.TOP][0]
    ri = laser.ri_return1

    # Parse compressed range image
    ri_matrix = open_dataset.MatrixFloat()
    decompressed = zlib.decompress(ri.range_image_compressed)
    ri_matrix.ParseFromString(decompressed)

    # Reshape to H x W x 2 (range + intensity)
    ri_np = np.array(ri_matrix.data).reshape(ri_matrix.shape.dims)

    # Use range channel (0)
    range_image = ri_np[:, :, 0]
    range_image = np.clip(range_image, 0, np.percentile(range_image, 99))
    range_image = range_image / np.max(range_image)  # Normalize 0-1
    range_image = (range_image * 255).astype(np.uint8)  # Scale 0-255

    # Apply colormap for visibility
    colored = cv2.applyColorMap(range_image, cv2.COLORMAP_JET)

    # ------------------------------
    # Aspect ratio fix: pad to desired_width x desired_height
    # ------------------------------
    h, w, _ = colored.shape

    # Optionally downscale crazy wide images
    max_width = 1000
    if w > max_width:
        scale = max_width / w
        new_w = max_width
        new_h = int(h * scale)
        colored = cv2.resize(colored, (new_w, new_h))
        h, w = colored.shape[:2]

    # Compute padding to center in 1280x720
    top = (desired_height - h) // 2
    bottom = desired_height - h - top
    left = (desired_width - w) // 2
    right = desired_width - w - left

    padded = cv2.copyMakeBorder(
        colored, top, bottom, left, right,
        cv2.BORDER_CONSTANT, value=[0, 0, 0]
    )

    # ------------------------------
    # Initialize writer if first frame
    # ------------------------------
    if video_writer is None:
        height, width, _ = padded.shape
        fps = 10  # Waymo LiDAR is 10 Hz
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        video_writer = cv2.VideoWriter(output_video, fourcc, fps, (width, height))
        print(f"Initialized video writer: {width}x{height}")

    video_writer.write(padded)
    print(f"Wrote padded LiDAR frame {idx}")

# ------------------------------
# Finalize
# ------------------------------
if video_writer:
    video_writer.release()
    print(f"LiDAR padded video saved to {output_video}")
else:
    print("No frames were written.")