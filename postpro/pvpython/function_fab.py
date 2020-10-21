#### import the simple module from the paraview
from paraview.simple import *
import getopt

#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

##
vertical_scale=10

###############################
def monthly_results(ResultFile=None,GridFile=None,BedId=102):

  # get active view
  SurfaceView = GetActiveViewOrCreate('RenderView')
## 
  ###
  # read results
  ### from active source
  if (ResultFile==None):
    run=GetActiveSource()
  ## from the results file
  else:
    run = XMLPartitionedUnstructuredGridReader(FileName=[ResultFile])
  # hide data in view
  Hide(run)
  RenameSource( proxy=run , newName = "Results")
  run.UpdatePipeline()

## plot 3D velocity
  SetActiveView(SurfaceView)
  ResultPlot(run)

## plot results at the bed
  layout2 = CreateLayout('Bed layout')
  BedView = CreateRenderView()
  AssignViewToLayout(view=BedView, layout=layout2, hint=0)
  BedPlots(run,BedId)

## project surface results on the observation grid
  if (GridFile != None):
     layout3 = CreateLayout('Proj. layout')
     ProjView = CreateRenderView()
     # assign view to a particular cell in the layout
     AssignViewToLayout(view=ProjView, layout=layout3, hint=0)
     SetActiveView(ProjView)
     ProjectToGrid(run,GridFile,BedId)

##################################################################################
### a common config for the views
############################################################################
def ViewConfiguration(View):
  # Hide orientation axes
  View.OrientationAxesVisibility = 0
  # Camera settings
  View.CameraPosition = [-348809.8295870024, -2482875.367089488, 159219.1116856395]
  View.CameraFocalPoint = [-180341.3787715006, -2493046.4280049987, 187.19160262968063]
  View.CameraViewUp = [0.6868612372011434, 0.015574106174458867, 0.7266216952771101]
  View.CameraParallelScale = 72623.42734187006

  if ("viewsize" in globals()) :
      View.ViewSize = viewsize
##################################################################
## project the surface results to the observation grid
#################################################################
def BedPlots(Source=None,BedId=102):

  if (Source==None):
    Source=FindSource("Results")
  if (Source==None):
    run=GetActiveSource()

  Source.UpdatePipeline()

  ## get handle on the render view
  renderView = GetActiveViewOrCreate('RenderView')
  ViewConfiguration(renderView)
  
  # Get Bed results
  Bed = Threshold(Input=Source)
  Bed.Scalars = ['CELLS', 'GeometryIds']
  Bed.ThresholdRange = [BedId,BedId]
  RenameSource( proxy=Bed , newName = "Bed")
  Bed.UpdatePipeline()

  Drag = Calculator(Input=Bed)
  Drag.ResultArrayName = 'Taub'
  Drag.Function = '10^(alpha)*mag(velocity)'
  Drag.UpdatePipeline()

  Display = Show(Bed,renderView)
  # set scalar coloring
  ColorBy(Display, ('POINTS','velocity','Magnitude'))
  Display.RescaleTransferFunctionToDataRange(True)
  # get color transfer function/color map for 'RTData'
  VelocityLUT = GetColorTransferFunction('velocity')
  # show color bar/color legend
  Display.SetScalarBarVisibility(renderView, True)
  Display.Scale = [1.0, 1.0, vertical_scale]

  Render(renderView)
  SaveScreenshot('BasalVelocity.png',renderView)

  Hide(Bed)
  Display = Show(Drag,renderView)
  # set scalar coloring
  ColorBy(Display, ('POINTS','Taub','Magnitude'))
  Display.RescaleTransferFunctionToDataRange(True)
  # get color transfer function/color map for 'RTData'
  TaubLUT = GetColorTransferFunction('Taub')
  TaubLUT.RescaleTransferFunction(0.0, 0.250)
  # show color bar/color legend
  Display.SetScalarBarVisibility(renderView, True)
  Display.Scale = [1.0, 1.0, vertical_scale]
 
  Render(renderView)
  SaveScreenshot('BasalDrag.png', renderView)

##################################################################
## project the surface results to the observation grid
#################################################################
def ProjectToGrid(run,GridFile,BedId):
 ## get handle on the render view
  renderView = GetActiveViewOrCreate('RenderView')
  ViewConfiguration(renderView)

  # Get surface results
  SurfId=BedId+1
  Surface = Threshold(Input=run)
  Surface.Scalars = ['CELLS', 'GeometryIds']
  Surface.ThresholdRange = [SurfId,SurfId]
  RenameSource( proxy=Surface , newName = "Surface")
  Surface.UpdatePipeline()
 
  # Horizontal projection
  calculator0 = Calculator(Input=Surface)
  calculator0.ResultArrayName = 'Ztop'
  calculator0.Function = 'coordsZ'
  calculator0.UpdatePipeline()

  # Horizontal projection
  calculator1 = Calculator(Input=calculator0)
  calculator1.CoordinateResults = 1
  calculator1.Function = 'coordsX*iHat+coordsY*jHat'
  calculator1.UpdatePipeline()

  # cells with all data <1 are passive
  thresholdH = Threshold(Input=calculator1)
  thresholdH.Scalars = ['Points', 'thickness']
  thresholdH.ThresholdRange = [0.0, 0.999999999]
  thresholdH.AllScalars=1
  thresholdH.Invert = 1
  thresholdH.UpdatePipeline()

  ################################
  # Read GRID
  grid = NetCDFReader(FileName=[GridFile])
  grid.Dimensions = '(y, x)'
  grid.SphericalCoordinates = 0
  grid.UpdatePipeline()

  # Project on grid
  resampleWithDataset1 = ResampleWithDataset(SourceDataArrays=thresholdH,DestinationMesh=grid)
  resampleWithDataset1.CellLocator = 'Cell Locator'
  resampleWithDataset1.PassPointArrays = 1
  RenameSource( proxy=resampleWithDataset1 , newName = "SurfToNetcdf")
  resampleWithDataset1.UpdatePipeline()

  # Get only valid results
  valid = Threshold(Input=resampleWithDataset1)
  valid.Scalars = ['Points', 'vtkValidPointMask']
  valid.ThresholdRange = [1.0, 1.0]
  valid.UpdatePipeline()

  calculator2 = Calculator(Input=valid)
  calculator2.CoordinateResults = 1
  calculator2.Function = 'coordsX*iHat+coordsY*jHat+Ztop*kHat'
  calculator2.UpdatePipeline()

  Misfit = Calculator(Input=calculator2)
  Misfit.ResultArrayName = 'Vdif'
  Misfit.Function = '(velocity_X-vx)*iHat+(velocity_Y-vy)*jHat'
  Misfit.UpdatePipeline()

  Vangle = Calculator(Input=calculator2)
  Vangle.ResultArrayName = 'Angle'
  Vangle.Function = 'acos((velocity_X*vx+velocity_Y*vy)/(mag(velocity_X*iHat+velocity_Y*jHat)*mag(vx*iHat+vy*jHat)))*180/3.14159'
  Vangle.UpdatePipeline()

  ADisplay = Show(Vangle,renderView)
  # set scalar coloring
  ColorBy(ADisplay,('POINTS','Angle','Magnitude'))
  ADisplay.RescaleTransferFunctionToDataRange(True)
  # get color transfer function/color map for 'RTData'
  AngleLUT = GetColorTransferFunction('Angle')
  AngleLUT.RescaleTransferFunction(0.0, 20.0)
  # show color bar/color legend
  ADisplay.SetScalarBarVisibility(renderView, True)
  ADisplay.Scale = [1.0, 1.0, vertical_scale]

  Render(renderView)
  SaveScreenshot('OrientationError.png', renderView)

  Hide(Vangle)

  MDisplay = Show(Misfit,renderView)
  # set scalar coloring
  ColorBy(MDisplay, ('POINTS','Vdif','Magnitude'))
  MDisplay.RescaleTransferFunctionToDataRange(True)
  # get color transfer function/color map for 'RTData'
  VdifLUT = GetColorTransferFunction('Vdif')
  VdifLUT.RescaleTransferFunction(0.0, 20.0)
  # show color bar/color legend
  MDisplay.SetScalarBarVisibility(renderView, True)
  MDisplay.Scale = [1.0, 1.0, vertical_scale]
  
  Render(renderView)
  SaveScreenshot('SurfaceError.png', renderView)

  
#########################################################
## plot the results
#########################################################
def ResultPlot(Source=None):

  if (Source==None):
    Source=FindSource("Results")
    Source.UpdatePipeline()

  SurfaceView = GetActiveViewOrCreate('RenderView')
  ViewConfiguration(SurfaceView)

  SurfDisplay = Show(Source,SurfaceView)
  # set scalar coloring
  ColorBy(SurfDisplay, ('POINTS','velocity','Magnitude'))
  SurfDisplay.RescaleTransferFunctionToDataRange(True)
  # get color transfer function/color map for 'RTData'
  VelocityLUT = GetColorTransferFunction('velocity')
  # show color bar/color legend
  SurfDisplay.SetScalarBarVisibility(SurfaceView, True)
  SurfDisplay.Scale = [1.0, 1.0, vertical_scale]

  Render(SurfaceView)
  SaveScreenshot('SurfaceVelocity.png', SurfaceView)

############################################################
### a function to save the projected values as numpy arrays
###########################################################
def savegrid() :
  from paraview.vtk.util import numpy_support
  import numpy as np
  # get data
  source=FindSource("SurfToNetcdf")
  source.UpdatePipeline()

  data=servermanager.Fetch(source)

  grid_dim=data.GetDimensions()
  grid_origin=data.GetOrigin()
  grid_spacing=data.GetSpacing()


  fillv=-1.0e6
  Ones=np.ones((grid_dim[0],grid_dim[1]))
  FillArray=Ones*fillv
  Zeros=np.zeros((grid_dim[0],grid_dim[1]))


  x=np.arange(grid_dim[0])*grid_spacing[0]+grid_origin[0]
  y=np.arange(grid_dim[1])*grid_spacing[1]+grid_origin[1]
  print
  print('grid x size:%i ; spacing: %f ; range: %f %f'%(grid_dim[0],grid_spacing[0],x[0],x[-1]))
  print('grid y size:%i ; spacing: %f ; range: %f %f'%(grid_dim[1],grid_spacing[1],y[0],y[-1]))
  print

  ## get valid mask
  valid=numpy_support.vtk_to_numpy(data.GetPointData().GetArray('vtkValidPointMask')).reshape((grid_dim[0],grid_dim[1]))
  print('valid data points:%i'%((valid == 1).sum()))

  ## get uvelmean and vvelmean (ssavelocity)
  vel=numpy_support.vtk_to_numpy(data.GetPointData().GetArray('velocity'))
  tmp=vel[:,0].reshape((grid_dim[0],grid_dim[1]))
  ux=np.where(valid==1,tmp,FillArray)

  tmp=vel[:,1].reshape((grid_dim[0],grid_dim[1]))
  uy=np.where(valid==1,tmp,FillArray)

  tmp=vel[:,2].reshape((grid_dim[0],grid_dim[1]))
  uz=np.where(valid==1,tmp,FillArray)

  np.savez('ElmerResults.npz', x=x,y=y,ux=ux, uy=uy, uz=uz)
   

#### Main function for batch mode
if __name__ == "__main__":
  ###############################
  # get args
  try:
      opts, args = getopt.getopt(sys.argv[1:], "i:g:B:")
  except getopt.GetoptError:
    sys.exit(2)
  for opt, arg in opts:                
    if opt in ("-i"): 
        ResultFile=arg
        found_i=True
    if opt in ("-g"):
        GridFile=arg
    if opt in ("-B"):
        BedId=int(arg)

  ## set view size for batch mode
  viewsize=[800,800]

  monthly_results(ResultFile,GridFile,BedId)
  savegrid()
