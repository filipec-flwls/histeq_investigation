# Setup Guide

## Main Script

Enter your required inputs into the main.py

```
    in_ext = "exr"
    out_ext = "jpg"
    target_resolution = (2578, 1080)
    out_folder_name = 'masked'
    input_dir = sorted(list(Path(r'input/to/your/files').iterdir()))
    csv_file_path = Path(r'shot_context_single.csv')
```
## Uncomment histeq process

Only one method at the time so having only one option is important to start each histeq

```
    from histeq_v001 import hist_eq_process_adapt 
    # from histeq_v002 import hist_eq_process_adapt2
    # from histeq_v003 import hist_eq_process_adapt3
    # from histeq_gamma_v001 import hist_eq_process_gamma
    # from histeq_gamma_v002 import hist_eq_process_gamma_split
    # from histeq_gamma_v002 import hist_eq_process_gamma_split_lum

        # hist_eq_process_adapt(image_path, out_path, target_resolution)
        # hist_eq_process_adapt2(image_path, out_path, target_resolution)
        # hist_eq_process_adapt3(image_path, out_path, target_resolution, cct_img_path)
        # hist_eq_process_gamma(image_path, out_path, target_resolution)
        # hist_eq_process_gamma_split(image_path, out_path, target_resolution)
        # hist_eq_process_gamma_split_lum(image_path, out_path, target_resolution)
```
