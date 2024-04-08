import numpy as np
from PyQt5 import QtWidgets

from PyQt5.QtWidgets import QDialog, QApplication, QPushButton, QVBoxLayout

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.backends.backend_qt5agg import FigureCanvas

import time

import numpy as np
from DicomRTTool.ReaderWriter import DicomReaderWriter, ROIAssociationClass
from matplotlib import pyplot as plt

from matplotlib.backend_bases import RendererBase
plt.ion() # Похоже юзелесс
ch = 0

# display_slices(image_numpy, mask_numpy, skip=n_slices_skip)


class MainWindow(QtWidgets.QDialog):
    def __init__(self, path, parent=None):
        super().__init__(parent)
        Dicom_path = r'./Step-2-333'
        Dicom_path = path
        Dicom_reader = DicomReaderWriter(description='Examples', arg_max=True)
        Dicom_reader.walk_through_folders(
            Dicom_path)  # This will parse through all DICOM present in the folder and subfolders
        all_rois = Dicom_reader.return_rois(print_rois=True)  # Return a list of all rois present
        print(all_rois)

        Contour_names = ['BODY']  # Define what rois you want
        associations = [ROIAssociationClass('tumor', ['tumor_mr', 'tumor_ct'])]  # Any list of roi associations
        Dicom_reader.set_contour_names_and_associations(contour_names=Contour_names, associations=associations)

        Dicom_reader.get_images_and_mask()

        image_numpy = Dicom_reader.ArrayDicom
        mask_numpy = Dicom_reader.mask
        image_sitk_handle = Dicom_reader.dicom_handle
        mask_sitk_handle = Dicom_reader.annotation_handle
        n_slices_skip = 1

        image = image_numpy
        mask = mask_numpy
        slice_locations = np.unique(np.where(mask != 0)[0])  # get indexes for where there is a contour present
        slice_start = slice_locations[0]  # first slice of contour
        slice_end = slice_locations[len(slice_locations) - 1]  # last slice of contour
        ses = list(zip(image[slice_start:slice_end + 1],
                       mask[slice_start:slice_end + 1]))

        self.figure = plt.figure()

        # this is the Canvas Widget that
        # displays the 'figure'it takes the
        # 'figure' instance as a parameter to __init__
        self.canvas = FigureCanvas(self.figure)

        # this is the Navigation widget
        # it takes the Canvas widget and a parent
        self.toolbar = NavigationToolbar(self.canvas, self)

        # Just some button connected to 'plot' method
        # self.button = QPushButton('Plot')

        # adding action to the button
        # self.button.clicked.connect(self.plot)

        # creating a Vertical Box layout
        layout = QVBoxLayout()

        # adding tool bar to the layout
        layout.addWidget(self.toolbar)

        # adding canvas to the layout
        layout.addWidget(self.canvas)

        # adding push button to the layout
        # layout.addWidget(self.button)

        # setting layout to the main window
        self.setLayout(layout)

        def on_scroll(event):
            global ch
            plt.clf()
            if event != 13:
                if event.button == 'down':
                    ch -= 1
                else:
                    ch += 1
                if ch == -1:
                    ch = len(ses) - 1
                if ch == len(ses):
                    ch = 0
                print(event.button)
            counter = 1

            img_arr, contour_arr = ses[ch]  # plot the slices with contours overlayed ontop
            # ch += 1
            print(ch)
            masked_contour_arr = np.ma.masked_where(contour_arr == 0, contour_arr)
            plt.imshow(img_arr, cmap='gray', interpolation='none')
            plt.imshow(masked_contour_arr, cmap='cool', interpolation='none', alpha=0.5, vmin=1, vmax=np.amax(
                mask))  # vmax is set as total number of contours so same colors can be displayed for each slice
            plt.draw()

            counter += 1

        on_scroll(13)
        plt.connect('scroll_event', on_scroll)
        self.show()
        # self.ax.imshow(Z)
        # self.ax.set_axis_off()

        # self.setCentralWidget(self.layout)
if __name__ == '__main__':
    import sys
    apps = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(apps.exec_())