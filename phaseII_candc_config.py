import glob

debug = False
Sample="PhaseII"
isESD=True
doTruth=True
doTTVAIso=False
phaseII=True

     
     
     
#Input file
from PyUtils import AthFile
import AthenaPoolCnvSvc.ReadAthenaPool                 #sets up reading of POOL files (e.g. xAODs)
from AthenaCommon.AthenaCommonFlags import athenaCommonFlags
#svcMgr.EventSelector.InputCollections=files
#athenaCommonFlags.FilesInput = svcMgr.EventSelector.InputCollections

jps.AthenaCommonFlags.FilesInput = FilesInput

from RecExConfig.InputFilePeeker import inputFileSummary
print ("Input type: %s" % inputFileSummary['stream_names'])

af = AthFile.fopen(svcMgr.EventSelector.InputCollections[0])
isMC = 'IS_SIMULATION' in af.fileinfos['evt_type']
run_number = af.run_number[0]


if(isMC==False):
    print ("Only for Phase II MC")
    exit(1)

print (af.fileinfos['conditions_tag'])

# Create output ROOT file for histograms
#svcMgr += CfgMgr.THistSvc()
#svcMgr.THistSvc.Output += ["RATESTREAM DATAFILE='RatesHistograms.root' OPT='RECREATE'"] #add an output root file stream

#jps.AthenaCommonFlags.HistOutputs = ["OUTPUT:cells.root"]

#Input file
from PyUtils import AthFile
import AthenaPoolCnvSvc.ReadAthenaPool                 #sets up reading of POOL files (e.g. xAODs)
from AthenaCommon.AthenaCommonFlags import athenaCommonFlags
#svcMgr.EventSelector.InputCollections=files
#athenaCommonFlags.FilesInput = svcMgr.EventSelector.InputCollections

from AthenaCommon.GlobalFlags import globalflags;
globalflags.DataSource.set_Value_and_Lock("geant4");
DetDescrVersion="ATLAS-P2-ITK-23-00-03";
ConditionsTag="OFLCOND-MC15c-SDR-14-03";
globalflags.DetDescrVersion.set_Value_and_Lock(DetDescrVersion);
include("InDetSLHC_Example/preInclude.NoTRT_NoBCM_NoDBM.py")
include("InDetSLHC_Example/preInclude.SLHC_Setup.py")
include("InDetSLHC_Example/preInclude.SLHC_Setup_Strip_GMX.py")
include("InDetSLHC_Example/preInclude.SLHC_Calorimeter_mu200.py")


# Access the algorithm sequece:
from AthenaCommon.AlgSequence import AlgSequence
topSequence=AlgSequence()

if(isESD):
    #Some database settings, needed for ESD
    from RecExConfig import AutoConfiguration
    AutoConfiguration.ConfigureSimulationOrRealData()
    AutoConfiguration.ConfigureGeo()
    
    from AthenaCommon.DetFlags import DetFlags
    DetFlags.detdescr.all_setOff()
    DetFlags.detdescr.Calo_setOn()
    include("RecExCond/AllDet_detDescr.py")

#What does this do
if(isMC and isESD ):
    include( "LArConditionsCommon/LArIdMap_MC_jobOptions.py" )


#What does this do
from RegistrationServices.RegistrationServicesConf import IOVRegistrationSvc
svcMgr += IOVRegistrationSvc()
if debug:
    svcMgr.IOVRegistrationSvc.OutputLevel = DEBUG
else:
    svcMgr.IOVRegistrationSvc.OutputLevel = INFO
svcMgr.IOVRegistrationSvc.RecreateFolders = True
svcMgr.IOVRegistrationSvc.SVFolder = False
svcMgr.IOVRegistrationSvc.userTags = False


#These lines are for configuring the bunch crossing tool, useful for some cases
from TrigBunchCrossingTool.BunchCrossingTool import BunchCrossingTool
if isMC: ToolSvc += BunchCrossingTool( "MC" )
else: ToolSvc += BunchCrossingTool( "LHC" )


###TrigL0Gep simulation
#422 cluster name Calo422TopoClusters
from TrigL0GepPerf.L0GepSimulationSequence import setupL0GepSimulationSequence
setupL0GepSimulationSequence(
    topoclAlgs = ['Calo422'],
    puSupprAlgs = [''],
    jetAlgs = ['AntiKt4']
    )



#Default setup
from TrigT1CaloFexSim.L1SimulationControlFlags import L1Phase1SimFlags as simflags

simflags.CTP.RunCTPEmulation=False
from TrigT1CaloFexPerf.L1PerfControlFlags import L1Phase1PerfFlags as pflags
pflags.CTP.RunCTPEmulation=False
if(phaseII):
    simflags.Calo.UseAllCalo=True
    simflags.Calo.RunEFexAlgorithms=False
    pflags.Calo.UseAllCalo=True



################
from RecExConfig.RecFlags import rec
rec.readAOD=True
rec.readESD=False
rec.readRDO=False
rec.doESD=False
rec.doWriteAOD=False

rec.doHist.set_Value_and_Lock(False)
rec.doCBNT.set_Value_and_Lock(False)
rec.doWriteTAGCOM.set_Value_and_Lock(False)
rec.doWriteTAG.set_Value_and_Lock(False)
rec.doWriteAOD.set_Value_and_Lock(False)
rec.doAOD.set_Value_and_Lock(False)
rec.doMonitoring.set_Value_and_Lock(False)

#include ("RecExCommon/RecExCommon_topOptions.py")


#add cell information to output.
from D3PDMakerRoot.D3PDMakerRootConf import D3PD__RootD3PDSvc
rootsvc=D3PD__RootD3PDSvc()
rootsvc.IndexMajor = ''
rootsvc.IndexMinor = ''
from D3PDMakerCoreComps.MakerAlg import MakerAlg
from D3PDMakerCoreComps.resolveSGKey import testSGKey
from EventCommonD3PDMaker.EventInfoD3PDObject import EventInfoD3PDObject
from CaloD3PDMaker.makeCaloCellFilterAlg import makeCaloCellFilterAlg
from CaloCellD3PDObject_slim import AllCaloCellD3PDObject


from AthenaCommon.AlgSequence import AthSequencer
alg = MakerAlg ('caloCells', topSequence, file = tuple_name ,
                D3PDSvc = 'D3PD::RootD3PDSvc')
alg += EventInfoD3PDObject (0)
alg += AllCaloCellD3PDObject (3, sgkey = 'AllCalo', prefix='cell_')

calocluster_sgkey = 'CaloCalTopoClusters'
from D3PDMakerCoreComps.ContainedVectorMultiAssociation import ContainedVectorMultiAssociation
from CaloD3PDMaker import CaloClusterCellAssociationTool

if testSGKey ('CaloClusterContainer', calocluster_sgkey):
    from CaloD3PDMaker.ClusterD3PDObject import ClusterD3PDObject
    from Cluster422D3PDObject import Cluster422D3PDObject
    alg += ClusterD3PDObject (5)
    
    #422 clusters
    alg += Cluster422D3PDObject (4)
    
elif testSGKey ('xAOD::CaloClusterContainer', calocluster_sgkey):
    from xAODClusterD3PDObject import xAODClusterD3PDObject
    from Cluster422D3PDObject import Cluster422D3PDObject
    alg += xAODClusterD3PDObject (5)
    
    #422 clusters
    alg += Cluster422D3PDObject (4)


#################
#### MET PART ###

from MissingETD3PDMaker.MissingETD3PDMakerFlags import MissingETD3PDMakerFlags

if 'IS_SIMULATION' in inputFileSummary['evt_type']:
    rec.doTruth = True

MissingETD3PDMakerFlags.doMissingETRegions = False
MissingETD3PDMakerFlags.doCellOutEflow = False
MissingETD3PDMakerFlags.doCells = False ## what is this?

METD3PDDetailLevel = 10
#from MissingETD3PDMaker.MissingETD3PD import MissingETD3PD
from MissingETD3PDMaker.MissingETD3PDObject  import MissingETD3PDObject
#from MissingETD3PDObject_custom import MissingETD3PDObject

alg += MissingETD3PDObject (level=METD3PDDetailLevel,
        allowMissing = True,
        exclude=['MET_Base', 'MET_RefTau', 'MET_SoftClus',
         'MET_RefFinal_Phi', 'MET_MuonBoy_Et',
         'MET_RefJet_SumEt', 'MET_RefJet', 'MET_RefEle', 'MET_RefGamma',
         ])

from MissingETD3PDObject_custom import MissingETD3PDObject_Truth, MissingETD3PDObject_Calo

alg += MissingETD3PDObject_Truth (level=METD3PDDetailLevel,
        allowMissing = True)
#alg += MissingETD3PDObject_Calo (level=METD3PDDetailLevel,
#        allowMissing = True)
        
# Reduce logging - but don't suppress messages
include("AthAnalysisBaseComps/SuppressLogging.py")
MessageSvc.defaultLimit = 9999999
MessageSvc.useColors = True
MessageSvc.Format = "% F%35W%S%7W%R%T %0W%M"

# Execution statistics
from AthenaCommon.AppMgr import theAuditorSvc
from GaudiAud.GaudiAudConf import ChronoAuditor
theAuditorSvc += ChronoAuditor()
theApp.AuditAlgorithms = True
