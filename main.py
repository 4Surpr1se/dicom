import pydicom as dicom
import matplotlib.pylab as plt
from DicomRTTool.ReaderWriter import DicomReaderWriter

# specify your image path
image_path = 'CT Structuree/CT.1.2.840.113619.2.218.40399348.21087.323404623.41.dcm'
ds = dicom.dcmread(image_path)

plt.imshow(ds.pixel_array)
plt.show()
DicomReaderWriter()
