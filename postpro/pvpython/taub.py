# trace generated using paraview version 5.8.1
#
# To ensure correct image size when batch processing, please search 
# for and uncomment the line `# renderView*.ViewSize = [*,*]`

#### import the simple module from the paraview
from paraview.simple import *
#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

# create a new 'XML Partitioned Unstructured Grid Reader'
PVTU = XMLPartitionedUnstructuredGridReader(FileName=['<INPUT>/OPTIM<NUM>_t0003.pvtu'])
PVTU.CellArrayStatus = ['GeometryIds']
PVTU.PointArrayStatus = ['slc', 'h', 'bedrock', 'mu', 'slc0', 'smb', 'dsmb_fc', 'dhdt_obs', 'slipcoef', 'groundedmask', 'zs', 'zb', 'ssavelocity', 'uobs']

# create a new 'Calculator'
calcul_taub = Calculator(Input=PVTU)
calcul_taub.Function = ''

# Properties modified on calculator1
calcul_taub.ResultArrayName = 'taub'
calcul_taub.Function = 'slc*((ssavelocity_X^2+ssavelocity_Y^2)^0.5)^(1/<m>)'

# save data
SaveData('<OUTPUT>/PARAM<NUM>.vtu', proxy=calcul_taub, PointDataArrays=['bedrock', 'dhdt_obs', 'dsmb_fc', 'groundedmask', 'h', 'mu', 'slc', 'slc0', 'slipcoef', 'smb', 'ssavelocity', 'taub', 'uobs', 'zb', 'zs'], CellDataArrays=['GeometryIds'])
