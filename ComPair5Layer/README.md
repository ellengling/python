# ComPair5Layer
.csv files with angular resolution, energy resolution, and effective area points for Fermi-LAT, COMPTEL, and AMEGO
EventAnalysisPlots and FigureOfMeritPlots contain pdf and png plots output by running EventAnalysis and FigureOfMeritPlotter

# Files of note
FigureOfMeritPlotter.py: updated file of same name in python directory to include data points for Fermi-LAT, COMPTEL, and ComPair (from .csv files)

**EventViewer.py Usage Example**:
import EventViewer
filename = 'FarFieldPointSource_1.000_Cos1.0.inc1.id1.sim'  
EventViewer.plot(filename)

EventAnalysis.py: Analyzes the output from revan and creates performance and log files

**EventAnalysis.py Usage Example**:
EventAnalysis.performCompleteAnalysis(directory="../Simulations/AMEGO4x4PerformancePlotTraFiles/")

FigureOfMeritPlotter.py: Takes output log files from EventAnalysis and creates instrument performance files

please see the ipython notebook for example usage
