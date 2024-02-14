import os
os.environ['OPENCV_IO_ENABLE_OPENEXR']='1'
import cv2
import numpy as np
import matplotlib.pyplot as plt
import skimage
import time
from pathlib import Path

def hist_eq_process_adapt3(image_path: Path, out_path: Path, target_resolution: tuple, cct_img_path: Path):
    """____________Reads Images____________"""
    start_time = time.time()

    img_exr = cv2.imread(str(image_path), cv2.IMREAD_UNCHANGED)
    img_cct = cv2.imread(str(cct_img_path), cv2.IMREAD_UNCHANGED)
    
    """____________Converts Image____________"""
    img_exr = ((img_exr - img_exr.min()) / (img_exr.max() - img_exr.min()))
    img_exr_eq = skimage.exposure.equalize_adapthist(img_exr, kernel_size=256*2, nbins=256*500)
    img_exr_uint = np.clip(np.round(img_exr_eq * 255), 0, 255).astype(np.uint8)
    
    """____________Resize Image____________"""
    img_converted = cv2.resize(img_exr_uint, target_resolution, interpolation=cv2.INTER_LINEAR)
    gray_image = cv2.cvtColor(img_cct, cv2.COLOR_BGR2GRAY)
    
    """____________Calculate Maximum and Mid Levels____________"""
    max_pixel_value = np.max(gray_image)
    mid_pixel_value = (np.max(gray_image) + np.min(gray_image)) // 2
    
    """____________Create Masks____________"""
    max_mask = cv2.compare(gray_image, max_pixel_value-20, cv2.CMP_GE)
    mid_mask = cv2.compare(gray_image, mid_pixel_value, cv2.CMP_GE)
    
    """____________Apply Masks to Isolate Levels____________"""
    max_level_isolated = cv2.bitwise_and(gray_image, gray_image, mask=max_mask)
    mid_level_isolated = cv2.bitwise_and(gray_image, gray_image, mask=mid_mask)
    
    """____________Merge Images of Max and Mid Levels____________"""
    max_and_mid_merged = cv2.add(max_level_isolated, mid_level_isolated)
    
    """____________Writes Processed Image____________"""
    cv2.imshow('Image', max_and_mid_merged)
    cv2.waitKey(1)
    cv2.destroyAllWindows()
    # cv2.imwrite(str(out_path / "max_and_mid_merged.png"), max_and_mid_merged)

    end_time = time.time()
    
    """____________Notification____________"""
    elapsed_time = end_time - start_time
    minutes = int(elapsed_time // 60)
    seconds = int(elapsed_time % 60)
    formatted_minutes = str(minutes).zfill(2)
    formatted_seconds = str(seconds).zfill(2)  
     
    if img_exr is None:
        print(f"Failed to read image: {image_path}")
        return
    print(f"Processing: {image_path}, \n Output: {out_path}")
    print(f"Processing took: [{formatted_minutes}:{formatted_seconds}]")
