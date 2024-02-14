import os
os.environ['OPENCV_IO_ENABLE_OPENEXR']='1'
import cv2
import numpy as np
import skimage
import pandas as pd
import time
from pathlib import Path

def clahe_equalization(image_path: Path, out_path: Path, target_resolution: tuple):
    
    """____________Read Image____________"""
    start_time = time.time()
    
    read_imgs = cv2.imread(str(image_path))
    
    """____________Convert Image____________"""
    convert_rgb_to_lab_imgs = cv2.cvtColor(read_imgs, cv2.COLOR_BGR2LAB) # Converts image to LAB colour so CLAHE can be applied to the luminance channel
    l, a, b = cv2.split(convert_rgb_to_lab_imgs) # Splitting the LAB image to L, A and B channels, respectivel

    """____________CLAHE____________"""
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
    clahe_l_img = clahe.apply(l) # Apply CLAHE to L channel
    m_clahe_channels_imgs = cv2.merge((clahe_l_img,a,b)) # Combine the CLAHE enhanced L-channel back with A and B channels
    CLAHE_img = cv2.cvtColor(m_clahe_channels_imgs, cv2.COLOR_LAB2BGR)# Convert LAB image back to color (RGB)

    """____________Resize Image____________"""
    CLAHE_rsz = cv2.resize(CLAHE_img, target_resolution, interpolation=cv2.INTER_LINEAR)
    
    """____________Writes Processed Image____________"""
    cv2.imwrite(str(out_path), CLAHE_rsz)
    
    end_time = time.time()
    
    """____________Notification____________"""
    elapsed_time = end_time - start_time
    minutes = int(elapsed_time // 60)
    seconds = int(elapsed_time % 60)
    formatted_minutes = str(minutes).zfill(2)
    formatted_seconds = str(seconds).zfill(2)  
     
    if CLAHE_rsz is None:
        print(f"Failed to read image: {image_path}")
        return
    print(f"Processing: {image_path}, \n Output: {out_path}")
    print(f"Processing took: [{formatted_minutes}:{formatted_seconds}]")

def read_input_create_output_folder(shot_dirs: Path, in_ext: str, out_ext: str, target_resolution: tuple, csv_data: pd.DataFrame):
    out_dir_path = shot_dirs / "clahe"
    out_dir_path.mkdir(parents=True, exist_ok=True)
    # print(f"Output Directory: {out_dir_path}")

    images_dir = shot_dirs / 'PROXYJPG' / 'proxy'
    image_paths = sorted(images_dir.glob(f"**/*.{in_ext}"))

    for image_path in image_paths:
        out_path = out_dir_path / f"{image_path.stem}.{out_ext}"
        print(f'This is shot dir:{shot_dirs}\n This is images dir:{images_dir}\n This is image_paths:{image_paths}\n this is image_path:{image_path}')
        # clahe_equalization(image_path, out_path, target_resolution)
    return

if __name__ == '__main__':
    
    in_ext = "jpg"
    out_ext = "jpg"
    target_resolution = (2578, 1080)
    input_dir = sorted(list(Path('/Volumes/shared/vfx/filipe.correia/Elements/hist_eq_tests/input').iterdir()))
    csv_file_path = Path('/Volumes/shared/vfx/filipe.correia/pulls/Hist_EQ/csv/shot_context.csv')
    csv_data = pd.read_csv(csv_file_path)
    
    for shot_dirs in input_dir:
        try:
            folder_name = shot_dirs.name
            if folder_name in csv_data['ShotName'].values:
                read_input_create_output_folder(shot_dirs, in_ext, out_ext, target_resolution, csv_data)
        except Exception as e:
            print(f"Error processing images: {e}")
