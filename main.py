import os
os.environ['OPENCV_IO_ENABLE_OPENEXR']='1'
import pandas as pd
from pathlib import Path
# from histeq_v001 import hist_eq_process_adapt 
# from histeq_v002 import hist_eq_process_adapt2
from histeq_v003 import hist_eq_process_adapt3
# from histeq_gamma_v001 import hist_eq_process_gamma
# from histeq_gamma_v002 import hist_eq_process_gamma_split
# from histeq_gamma_v002 import hist_eq_process_gamma_split_lum

def read_input_create_output_folder(shot_dirs: Path, in_ext: str, out_ext: str, target_resolution: tuple, csv_data: pd.DataFrame, out_folder_name: str):
    out_dir_path = shot_dirs / out_folder_name
    out_dir_path.mkdir(parents=True, exist_ok=True)

    images_dir = shot_dirs
    image_paths = sorted(images_dir.glob(f"**/*.{in_ext}"))
    
    cct_img_dir = shot_dirs / 'cct'
    cct_img_paths = sorted(cct_img_dir.glob(f"*.{out_ext}"))
    # print(cct_img_paths)
    # print(type(cct_img_paths))
    # # print(image_paths)
    # print(type(image_paths))
    for image_path in image_paths:
        cct_img_path = next(path for path in cct_img_paths if path.stem == image_path.stem)
        out_path = out_dir_path / f"{image_path.stem}.{out_ext}"
        # hist_eq_process_adapt(image_path, out_path, target_resolution)
        # hist_eq_process_adapt2(image_path, out_path, target_resolution)
        hist_eq_process_adapt3(image_path, out_path, target_resolution, cct_img_path)
        # hist_eq_process_gamma(image_path, out_path, target_resolution)
        # hist_eq_process_gamma_split(image_path, out_path, target_resolution)
        # hist_eq_process_gamma_split_lum(image_path, out_path, target_resolution)
    return

if __name__ == '__main__':
    
    in_ext = "exr"
    out_ext = "jpg"
    target_resolution = (2578, 1080)
    out_folder_name = 'masked'
    input_dir = sorted(list(Path(r'input/to/your/files').iterdir()))
    csv_file_path = Path(r'shot_context_single.csv')
    csv_data = pd.read_csv(csv_file_path)
    
    for shot_dirs in input_dir:
        try:
            folder_name = shot_dirs.name
            if folder_name in csv_data['ShotName'].values:
                read_input_create_output_folder(shot_dirs, in_ext, out_ext, target_resolution, csv_data, out_folder_name)
                
        except Exception as e:
            print(f"Error processing images: {e}")
