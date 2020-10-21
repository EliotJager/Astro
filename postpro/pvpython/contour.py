#### import the simple module from the paraview
from paraview.simple import *
import getopt

#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

##
vertical_scale=10

###############################
def greenland_results(PVDfile=None,GridFile=None,BedId=102):

  # get active view
  SurfaceView = GetActiveViewOrCreate('RenderView')
## 
  ###
  # read results
  ### from active source
  if (PVDFile==None):
    run=GetActiveSource()
  ## from the results file
  else:
    run = PVDReader(FileName=PVDfile)
  # hide data in view
  Hide(run)
  RenameSource( proxy=run , newName = "Results")
  run.UpdatePipeline()

## plot Results


## for making some contour
  # we need first calculate magnitude of velocity
    # create a new 'Calculator'
    ## display contour
  CalculatorUmod = Calculator(Input=run)

   # Properties modified on calculator12
  CalculatorUmod.ResultArrayName = 'Umod'
  CalculatorUmod.Function = '(ssavelocity_X^2+ssavelocity_Y^2)^0.5'

  #SetActiveView(SurfaceView)
  ResultTaub(CalculatorUmod, 'h', [10,3000])


##################################################################################
### a common config for the views
############################################################################
def ViewGreenland(View):
  # 2D mode
  View.InteractionMode = '2D'
  # Camera settings
  View.CameraPosition = [110990.3125, -1996074.0, 8015672.0]
  View.CameraFocalPoint = [110990.3125, -1996074.0, 9869.0]
  View.CameraParallelScale = 2106070.0
  View.CameraParallelProjection = 1

  if ("viewsize" in globals()) :
      View.ViewSize = viewsize

#########################################################
## plot the results
#########################################################
def ResultTaub(Source=None, Variable='ssavalocity', interval = [0.001,1.0]):

  if (Source==None):
    Source=FindSource("Results")
    Source.UpdatePipeline()
  
  SurfaceView = GetActiveViewOrCreate('RenderView')
  ViewGreenland(SurfaceView)

  print(Variable)
  print(Source.PointData.keys())  
  # show data in view
  Display = Show(Source, SurfaceView, 'UnstructuredGridRepresentation')
  ColorBy(Display, ('POINTS', Variable))
  VarLUT = GetColorTransferFunction(Variable)
  # get opacity transfer function/opacity map for Variable 
  VarPWF = GetOpacityTransferFunction(Variable)
  ## logscale
  # convert to log space
  VarLUT.MapControlPointsToLogSpace()
  # Properties modified on taub_trueLUT
  VarLUT.UseLogScale = 1
  # Rescale transfer function
  VarLUT.RescaleTransferFunction(interval[0], interval[1])
  # Rescale transfer function
  VarPWF.RescaleTransferFunction(interval[0], interval[1])  
  # show color bar/color legend
  Display.SetScalarBarVisibility(SurfaceView, True)

  ## display + savescreen
  Render(SurfaceView)
  SaveScreenshot('Var.png', SurfaceView)
  #Hide(Source,SurfaceView)

  
  # get color transfer function/color map for 'Umod'

  UmodLUT = GetColorTransferFunction('Umod')
  
  # get opacity transfer function/opacity map for 'Umod'
  UmodPWF = GetOpacityTransferFunction('Umod')

  ## making some contours
  
  # create a new 'Contour'
  ContourVel = Contour(Input=Source)
  ContourVel.ContourBy = ['POINTS', 'Umod']
  ContourVel.PointMergeMethod = 'Uniform Binning'
  ContourVel.Isosurfaces = [1.0, 5.0, 10.0, 20.0, 50.0, 100.0, 500.0]
  
  ## display contour
  ContDisplay = Show(ContourVel,SurfaceView, 'GeometryRepresentation')
  
  # Properties modified on ssavelocity_magnLUT
  UmodLUT.UseLogScale = 1
  UmodLUT.ApplyPreset('Black, Blue and White', True)
  
  # Rescale transfer function
  UmodLUT.RescaleTransferFunction(1.0, 500.0)
  # Rescale transfer function
  UmodPWF.RescaleTransferFunction(1.0, 500.0)

  # show color bar/color legend
  ContDisplay.SetScalarBarVisibility(SurfaceView, True)

  ## display + savescreen
  Render(SurfaceView)
  SaveScreenshot(Variable+'new.png', SurfaceView)
  Hide(Source,SurfaceView)


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
        PVDFile=arg
        found_i=True
    if opt in ("-g"):
        GridFile=arg
    if opt in ("-B"):
        BedId=int(arg)

  ## set view size for batch mode
  viewsize=[800,800]

  greenland_results(PVDFile)
