# Copyright (C) 2002-2017 CERN for the benefit of the ATLAS collaboration

import CaloD3PDMaker
import D3PDMakerCoreComps
import EventCommonD3PDMaker
from D3PDMakerCoreComps.D3PDObject import make_SGDataVector_D3PDObject
from D3PDMakerConfig.D3PDMakerFlags import D3PDMakerFlags, _string_prop
from CaloD3PDMaker import CaloD3PDMakerConf
from D3PDMakerCoreComps.ContainedVectorMultiAssociation import ContainedVectorMultiAssociation


from AthenaCommon.JobProperties import JobProperty, JobPropertyContainer
from AthenaCommon.JobProperties import jobproperties

_string_prop ('Cluster422SGKey','Calo422TopoClusters')


Cluster422D3PDObject = \
           make_SGDataVector_D3PDObject ('xAOD::CaloClusterContainer',
                                         D3PDMakerFlags.Cluster422SGKey(),
                                         'cl422_', 'Cluster422D3PDObject',
                                         default_allowMissing = True)


Cluster422D3PDObject.defineBlock (0, 'Kinematics',
                               EventCommonD3PDMaker.FourMomFillerTool,
                               WriteE = False,
                               WriteM = False)

Cluster422D3PDObject.defineBlock (0, 'SamplingBasics',
                                   CaloD3PDMaker.ClusterSamplingFillerTool)

Cluster422D3PDObject.defineBlock (
    1, 'Moments',
    D3PDMakerCoreComps.AuxDataFillerTool,
    Vars = ['firstEdens = FIRST_ENG_DENS<float:0',
            'cellmaxfrac = ENG_FRAC_MAX<float:0',
            'longitudinal = LONGITUDINAL<float:0',
            'secondlambda = SECOND_LAMBDA<float:0',
            'lateral = LATERAL<float:0',
            'secondR = SECOND_R<float:0',
            'centerlambda = CENTER_LAMBDA<float:0',
            'eng_bad_cells = ENG_BAD_CELLS<float:0',
            'n_bad_cells = N_BAD_CELLS<float:0',
            'isolation = ISOLATION<float:0',
            ])
Cluster422D3PDObject.defineBlock (
    1, 'CenterMagMoment',
    D3PDMakerCoreComps.AuxDataFillerTool,
    Vars = ['centermag = CENTER_MAG<float:0',
            ])
Cluster422D3PDObject.defineBlock (
    1, 'Time',
    D3PDMakerCoreComps.AuxDataFillerTool,
    Vars = ['time'])

Cluster422D3PDObject.defineBlock (2, 'SamplingEnergies',
                                   CaloD3PDMaker.ClusterSamplingFillerTool,
                                   EmHadEnergies = False, # don't duplicate this one!
                                   SamplingEnergies = True,
                                   SamplingEtaPhi = False,
                                   WriteRecoStatus = False)

Cluster422D3PDObject.defineBlock (3, 'SamplingEtaPhi',
                                   CaloD3PDMaker.ClusterSamplingFillerTool,
                                   EmHadEnergies = False, # don't duplicate this one!
                                   SamplingEnergies = False, # don't duplicate this one!
                                   SamplingEtaPhi = False,
                                   WriteRecoStatus = False) # don't duplicate this one!


CaloCellInCluster422 = ContainedVectorMultiAssociation (
    Cluster422D3PDObject,
    CaloD3PDMaker.CaloClusterCellAssociationTool,
    "cell_",
    4)

CaloCellInCluster422.defineBlock (4, 'CellKinematics',
                                EventCommonD3PDMaker.FourMomFillerTool,
                                WriteE  = True,  WriteM = False)
