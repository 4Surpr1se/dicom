import matplotlib.pyplot as plt
import numpy as np

import time

import numpy as np
from DicomRTTool.ReaderWriter import DicomReaderWriter, ROIAssociationClass
from matplotlib import pyplot as plt
print(type(plt))

res = []


def display_slices(image, mask, skip=1):
    """
    Displays a series of slices in z-direction that contains the segmented regions of interest.
    Ensures all contours are displayed in consistent and different colors.
        Parameters:
            image (array-like): Numpy array of image.
            mask (array-like): Numpy array of mask.
            skip (int): Only print every nth slice, i.e. if 3 only print every 3rd slice, default 1.
        Returns:
            None (series of in-line plots).
    """
    # fig, ax = plt.subplots()
    # ax.plot(np.random.rand(10))
    slice_locations = np.unique(np.where(mask != 0)[0])  # get indexes for where there is a contour present
    slice_start = slice_locations[0]  # first slice of contour
    slice_end = slice_locations[len(slice_locations) - 1]  # last slice of contour
    # plt.ion()
    def onclick(event):
        counter = 1
        global cla
        cla += 1
        img_arr, contour_arr = list(zip(image[slice_start:slice_end + 1],
                                        mask[slice_start:slice_end + 1]))[cla]
        print(img_arr, contour_arr)# plot the slices with contours overlayed ontop
        print(cla)
        if counter % skip == 0:  # if current slice is divisible by desired skip amount
            masked_contour_arr = np.ma.masked_where(contour_arr == 0, contour_arr)
            # res.append([img_arr, masked_contour_arr])
            plt.imshow(img_arr, cmap='gray', interpolation='none')
            plt.imshow(masked_contour_arr, cmap='cool', interpolation='none', alpha=0.5, vmin=1, vmax=np.amax(
                mask))  # vmax is set as total number of contours so same colors can be displayed for each slice
            # plt.draw()
            plt.show()
            # plt.clf()

        counter += 1

    plt.connect('button_press_event', onclick)
    onclick(32)
    # plt.show()

cla = 0
Dicom_path = r'./Step-2-333'
Dicom_reader = DicomReaderWriter(description='Examples', arg_max=True)
Dicom_reader.walk_through_folders(Dicom_path) # This will parse through all DICOM present in the folder and subfolders
all_rois = Dicom_reader.return_rois(print_rois=True) # Return a list of all rois present
print(all_rois)

Contour_names = ['BODY'] # Define what rois you want
associations = [ROIAssociationClass('tumor', ['tumor_mr', 'tumor_ct'])] # Any list of roi associations
Dicom_reader.set_contour_names_and_associations(contour_names=Contour_names, associations=associations)

Dicom_reader.get_images_and_mask()

image_numpy = Dicom_reader.ArrayDicom
mask_numpy = Dicom_reader.mask
image_sitk_handle = Dicom_reader.dicom_handle
mask_sitk_handle = Dicom_reader.annotation_handle
n_slices_skip = 4

display_slices(image_numpy, mask_numpy, skip=n_slices_skip)

