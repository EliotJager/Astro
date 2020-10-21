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

## Warp by bedrock elevation

  ## add elevation with WarpByScalar
  # create a new 'Warp By Scalar'
  warpByZb = WarpByScalar(Input=run)
  # Properties modified on warpByScalar1
  warpByZb.Scalars = ['POINTS', 'zb']
  warpByZb.ScaleFactor = 10.0

  # show data in view
  warpByZbDisplay = Show(warpByZb, SurfaceView, 'UnstructuredGridRepresentation')
  Hide(warpByZb)

## calcul of real taub
  
  Surface = Threshold(Input=warpByZb)
  Surface.Scalars = ['CELLS', 'GeometryIds']
  RenameSource( proxy=Surface , newName = "Surface")
  Surface.UpdatePipeline()

   # create a new 'Calculator'
  calculatorTaub = Calculator(Input=Surface)

   # Properties modified on calculator12
  calculatorTaub.ResultArrayName = 'Tau_b'
  calculatorTaub.Function = 'taub*(1+groundedmask)/2'


## we make statistics on Taub
  # create a new 'Temporal Statistics'
  StatisticsTaub = TemporalStatistics(Input=calculatorTaub)

## for making some contour
  # we need first calculate magnitude of velocity
    # create a new 'Calculator'
    ## display contour
  calculatorUmod = Calculator(Input=StatisticsTaub)

   # Properties modified on calculator12
  calculatorUmod.ResultArrayName = 'Umod'
  calculatorUmod.Function = '(ssavelocity_average_X^2+ssavelocity_average_Y^2)^0.5'


## we plot the statistics
# average
  ResultTaub(calculatorUmod, 'Tau_b_average')

# minimum 
  ResultTaub(calculatorUmod, 'Tau_b_minimum')

# maximum
  ResultTaub(calculatorUmod, 'Tau_b_maximum')

# standard deviation
  ResultTaub(calculatorUmod, 'Tau_b_stddev', [0.00001,0.1])


## Coefficient of variation
   # create a new 'Calculator'
  calculatorCV_Taub = Calculator(Input=calculatorUmod)

   # Properties modified on calculator12
  calculatorCV_Taub.ResultArrayName = 'CV_Tau_b(%)'
  calculatorCV_Taub.Function = '100*Tau_b_stddev/Tau_b_average'

## other plot (CV)
  ResultTaub(calculatorCV_Taub, 'CV_Tau_b(%)', [1,100])



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


##################################################################################
### a common config for the views
############################################################################
def ViewGreenland(View):
  # 2D mode
  View.InteractionMode = '2D'
  # Camera settings
  View.CameraPosition = [53435.2, -2003849.5, 7062504.8]
  View.CameraFocalPoint = [53435.2, -2003849.5, 0.0]
  View.CameraParallelScale = 1527263.3
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

  SurfDisplay = Show(Source,SurfaceView)
  
  # set scalar coloring
  ColorBy(SurfDisplay, ('POINTS',Variable))
  # get color transfer function/color map for 'RTData'
  VarLUT = GetColorTransferFunction(Variable)
  # get opacity transfer function/opacity map for 'taub_true'
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
  SurfDisplay.SetScalarBarVisibility(SurfaceView, True)
  SurfDisplay.Scale = [1.0, 1.0, vertical_scale]
  ## change colors
  VarLUT.ApplyPreset('Rainbow Desaturated', True)
  ## making some contours
  
  ## display + savescreen
  Render(SurfaceView)
  SaveScreenshot(Variable+'.png', SurfaceView)

  # get color transfer function/color map for 'Umod'

  UmodLUT = GetColorTransferFunction('Umod')

  # get opacity transfer function/opacity map for 'Umod'
  UmodPWF = GetOpacityTransferFunction('Umod')

  ## making some contours

  print(Source.PointData.keys())

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
  SaveScreenshot(Variable+'contour.png', SurfaceView)
  Hide(Source,SurfaceView)
  Hide(ContourVel,SurfaceView)


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
