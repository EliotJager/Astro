# trace generated using paraview version 5.8.1
#
# To ensure correct image size when batch processing, please search 
# for and uncomment the line `# renderView*.ViewSize = [*,*]`

#### import the simple module from the paraview
from paraview.simple import *


# create a new 'PVD Reader'
PVDs = PVDReader(FileName='/mnt/data/ejager/Greenland/OPTIM3.pvd')
PVDs.CellArrays = []
PVDs.PointArrays = ['zs', 'zb', 'slipcoef', 'h', 'slc', 'ssavelocity', 'uinit']


# create a new 'Slice'
slice1 = Slice(Input=PVDs, SliceType = 'Plane', SliceOffsetValues = [0.0])

# init the 'Plane' selected for 'SliceType'
slice1.SliceType.Origin = [110000.0, -1455000.0, 0.0]

# Properties modified on slice1.SliceType
slice1.SliceType.Normal = [1.0, -1.06, 0.0]

#### interpolate vtu values at point coordinates
# create a new 'Resample With Dataset'
## For paraview 5.7 (and >?)
resampleWithDataset1 = ResampleWithDataset(SourceDataArrays=PVDs,DestinationMesh=slice1)
## For paraview 5.6 (ciment)
#resampleWithDataset1 = ResampleWithDataset(Input=PVDs,Source=slice1)

#print(resampleWithDataset1.ListProperties())

# save data
SaveData('output/results.csv', proxy=resampleWithDataset1, Precision=8, WriteTimeSteps=1) # WriteAllTimeSteps=1 sur les versions paraview moins recentes
