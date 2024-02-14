import os
os.environ['OPENCV_IO_ENABLE_OPENEXR']='1'
import cv2
import numpy as np
import skimage
import time
from pathlib import Path

def hist_eq_process_gamma_split(image_path: Path, out_path: Path, target_resolution: tuple):
    """____________Reads Image____________"""
    start_time = time.time()
    
    image = cv2.imread(str(image_path), -1)
    
    """____________Converts Image____________"""
    image = image[:,:,:3]
    image = ((image - image.min()) / (image.max() - image.min()))
    b, g, r = cv2.split(image)
    b_eq = skimage.exposure.equalize_adapthist(b, kernel_size=256*2, nbins=256*500)
    g_eq = skimage.exposure.equalize_adapthist(g, kernel_size=256*2, nbins=256*500)
    r_eq = skimage.exposure.equalize_adapthist(r, kernel_size=256*2, nbins=256*500)
    image = cv2.merge((b_eq, g_eq, r_eq))

    
    """____________Resize Image____________"""
    image = cv2.resize(image, target_resolution, interpolation=cv2.INTER_LINEAR)
    
    """____________Writes Processed Image____________"""
    image = image ** (1/ 2.2)
    cv2.imwrite(str(out_path), image * 255)
    
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
