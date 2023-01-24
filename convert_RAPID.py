from operator import concat
import pandas as pd
import os
import SimpleITK as sitk
import numpy as np
import glob
import pydicom


def convert_map_to_nii(dcm_path, output_path, file_name, stats_only):

    if not stats_only:

        dicom_paths = glob.glob(dcm_path + '*.dcm')

        output_path_map_image = output_path + file_name + '_image/'
        if not os.path.isdir(output_path_map_image):
            os.system('mkdir -p ' + output_path_map_image)

        output_path_map_mask = output_path + file_name + '_mask/'
        if not os.path.isdir(output_path_map_mask):
            os.system('mkdir -p ' + output_path_map_mask)

        for i in range(len(dicom_paths)):

            dcm_file_name = dicom_paths[i].split('/')[-1]
            #print(i, dcm_file_name)

            ds_image = pydicom.dcmread(dicom_paths[i])
            ds_mask = pydicom.dcmread(dicom_paths[i])
            
            data_image = ds_image.pixel_array
            data_mask = ds_mask.pixel_array
            shape = data_image.shape

            for y in range(shape[0]):
                for x in range(shape[1]):
                    red = data_image[y, x, 0]
                    green = data_image[y, x, 1]
                    blue = data_image[y, x, 2]
                    if x < 50 or y > 540:
                        data_image[y, x] = [0, 0, 0]
                        data_mask[y, x] = [0, 0, 0]
                    elif (red > 128 and green < 128 and blue < 128):
                        data_image[y, x] = [50, 50, 50]
                        data_mask[y, x] = [1, 1, 1]
                    elif (red > 128 and green > 128 and blue < 128):
                        data_image[y, x] = [50, 50, 50]
                        data_mask[y, x] = [2, 2, 2]
                    elif (red < 128 and green > 128 and blue < 128):
                        data_image[y, x] = [50, 50, 50]
                        data_mask[y, x] = [3, 3, 3]
                    elif (red < 128 and green < 128 and blue > 128):
                        data_image[y, x] = [50, 50, 50]
                        data_mask[y, x] = [4, 4, 4]
                    else:
                        data_mask[y, x] = [0, 0, 0]
                    
            ds_image.PixelData = data_image.tobytes()
            ds_mask.PixelData = data_mask.tobytes()

            pydicom.dcmwrite(output_path_map_image + dcm_file_name, ds_image)
            pydicom.dcmwrite(output_path_map_mask + dcm_file_name, ds_mask)

        command = 'dcm2niix -b n -m y -v y -z i -f ' + file_name + '_image' + ' -o \"' + output_path + '\" \"' + output_path_map_image  + '\"'
        print(command)
        os.system(command)

        command = 'dcm2niix -b n -m y -v y -z i -f ' + file_name + '_mask' + ' -o \"' + output_path + '\" \"' + output_path_map_mask  + '\"'
        print(command)
        os.system(command)

    nii_path_image = output_path + file_name + '_image.nii.gz'
    nii_path_mask = output_path + file_name + '_mask.nii.gz'

    assert(os.path.isfile(nii_path_image))
    assert(os.path.isfile(nii_path_mask))

    return nii_path_image, nii_path_mask



