from rt_utils import RTStructBuilder
import matplotlib.pyplot as plt

# Load existing RT Struct. Requires the series path and existing RT Struct path
rtstruct = RTStructBuilder.create_from(
  dicom_series_path="./testlocation",
  rt_struct_path="./testlocation/rt-struct.dcm"
)

# Add ROI. This is the same as the above example.
rtstruct.add_roi(
  mask=MASK_FROM_ML_MODEL,
  color=[255, 0, 255],
  name="RT-Utils ROI!"
)

rtstruct.save('new-rt-struct')