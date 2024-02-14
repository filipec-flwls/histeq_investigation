import os
os.environ['OPENCV_IO_ENABLE_OPENEXR']='1'
import cv2
import numpy as np
import skimage
import time
from pathlib import Path

def hist_eq_process_adapt2(image_path: Path, out_path: Path, target_resolution: tuple):
    """____________Reads Images____________"""
    start_time = time.time()
    
    image = cv2.imread(str(image_path), cv2.IMREAD_UNCHANGED )
    
    """____________Converts Image____________"""
    equalized_channels = []
    for i in range(image.shape[2]):
        channel = image[:,:,i]
        normalized_channel = (channel - channel.min()) / (channel.max() - channel.min())
        equalized_channel = skimage.exposure.equalize_adapthist(normalized_channel, kernel_size=256*2, nbins=256*500)
        equalized_channel = np.clip(np.round(equalized_channel * 255), 0, 255).astype(np.uint8)
        equalized_channels.append(equalized_channel)
    image = np.stack(equalized_channels, axis=-1)
    
    """____________Resize Image____________"""
    image = cv2.resize(image, target_resolution, interpolation=cv2.INTER_LINEAR)

    """____________Writes Processed Image____________"""
    cv2.imwrite(str(out_path), image)

    end_time = time.time()
    
    """____________Notification____________"""
    elapsed_time = end_time - start_time
    minutes = int(elapsed_time // 60)
    seconds = int(elapsed_time % 60)
    formatted_minutes = str(minutes).zfill(2)
    formatted_seconds = str(seconds).zfill(2)  
     
    if image is None:
        print(f"Failed to read image: {image_path}")
        return
    print(f"Processing: {image_path}, \n Output: {out_path}")
    print(f"Processing took: [{formatted_minutes}:{formatted_seconds}]")
    
