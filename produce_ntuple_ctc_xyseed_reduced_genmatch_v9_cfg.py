import FWCore.ParameterSet.Config as cms 
from Configuration.StandardSequences.Eras import eras

# For old samples use the digi converter
process = cms.Process('DIGI',eras.Phase2C4)

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('SimGeneral.MixingModule.mixNoPU_cfi')
process.load('Configuration.Geometry.GeometryExtended2023D35Reco_cff')
process.load('Configuration.Geometry.GeometryExtended2023D35_cff')
process.load('Configuration.StandardSequences.MagneticField_cff')
process.load('Configuration.StandardSequences.Generator_cff')
process.load('IOMC.EventVertexGenerators.VtxSmearedHLLHC14TeV_cfi')
process.load('GeneratorInterface.Core.genFilterSummary_cff')
process.load('Configuration.StandardSequences.SimIdeal_cff')
process.load('Configuration.StandardSequences.Digi_cff')
process.load('Configuration.StandardSequences.SimL1Emulator_cff')
process.load('Configuration.StandardSequences.DigiToRaw_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')


process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(10)
)

# Input source
process.source = cms.Source("PoolSource",
       fileNames = cms.untracked.vstring('/store/mc/PhaseIIMTDTDRAutumn18DR/SingleE_FlatPt-2to100/FEVT/PU200_103X_upgrade2023_realistic_v2-v1/70000/008A0FE7-A01F-CB4B-B101-903A2A27BE2E.root'),
       inputCommands=cms.untracked.vstring(
           'keep *',
           'drop l1tEMTFHit2016Extras_simEmtfDigis_CSC_HLT',
           'drop l1tEMTFHit2016Extras_simEmtfDigis_RPC_HLT',
           'drop l1tEMTFHit2016s_simEmtfDigis__HLT',
           'drop l1tEMTFTrack2016Extras_simEmtfDigis__HLT',
           'drop l1tEMTFTrack2016s_simEmtfDigis__HLT',
           )
       )

process.options = cms.untracked.PSet(

)

# Output definition
process.TFileService = cms.Service(
    "TFileService",
    fileName = cms.string("ntuple.root")
    )

# Other statements
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:phase2_realistic', '')

# load HGCAL TPG simulation
process.load('L1Trigger.L1THGCal.hgcalTriggerPrimitives_cff')
process.load('L1Trigger.L1THGCalUtilities.HGC3DClusterGenMatchSelector_cff')
process.load('L1Trigger.L1THGCalUtilities.hgcalTriggerNtuples_cff')
from L1Trigger.L1THGCalUtilities.hgcalTriggerChains import HGCalTriggerChains
import L1Trigger.L1THGCalUtilities.vfe as vfe
import L1Trigger.L1THGCalUtilities.concentrator as concentrator
import L1Trigger.L1THGCalUtilities.clustering2d as clustering2d
import L1Trigger.L1THGCalUtilities.clustering3d as clustering3d
import L1Trigger.L1THGCalUtilities.selectors as selectors
import L1Trigger.L1THGCalUtilities.customNtuples as ntuple

# Change seed position to energy weigted barycenter
process.histoMax_C3d_params.seed_position = cms.string('TCWeighted')

chains = HGCalTriggerChains()
# Register algorithms
## VFE
chains.register_vfe("Floatingpoint8",
        lambda p : vfe.create_compression(p, 4, 4, True))
## ECON
chains.register_concentrator("Supertriggercell",
        concentrator.create_supertriggercell)
chains.register_concentrator("Supertriggercell4444fixed",
        lambda p,i : concentrator.create_supertriggercell(p,i,
            stcSize=cms.vuint32(4,8,8,8),fixedDataSizePerHGCROC=True ))
chains.register_concentrator("Equalshare",
        lambda p,i : concentrator.create_supertriggercell(p,i,
            stcSize=cms.vuint32(4,8,8,8),fixedDataSizePerHGCROC=True,type_energy_division='equalShare'))
chains.register_concentrator("Onebit",
        concentrator.create_onebitfraction)
## BE1
chains.register_backend1("Dummy",
        clustering2d.create_dummy)
## BE2
chains.register_backend2("Histomax",
        clustering3d.create_histoMax_variableDr)
chains.register_backend2("Histomaxbin4",
        lambda p,i : clustering3d.create_histoMaxXY_variableDr(p,i,
        nBins_X1=96,
        nBins_X2=96))
chains.register_backend2("Histomaxbin4shape15",
        lambda p,i : clustering3d.create_histoMaxXY_variableDr(p,i,
        nBins_X1=96,
        nBins_X2=96,
        shape_threshold=1.5))
### Varies clustering distance
from L1Trigger.L1THGCal.customClustering import dr_layerbylayer
dr_layerbylayer_50 = [dr*0.5 for dr in dr_layerbylayer]
dr_layerbylayer_200 = [dr*2. for dr in dr_layerbylayer]
chains.register_backend2("Histomaxbin4dr50",
        lambda p,i : clustering3d.create_histoMaxXY_variableDr(p,i,
        nBins_X1=96,
        nBins_X2=96,
    distances=dr_layerbylayer_50))
chains.register_backend2("Histomaxbin4dr50shape15",
        lambda p,i : clustering3d.create_histoMaxXY_variableDr(p,i,
        nBins_X1=96,
        nBins_X2=96,
    distances=dr_layerbylayer_50,
    shape_threshold=1.5))
chains.register_backend2("Histomaxbin4dr200",
        lambda p,i : clustering3d.create_histoMaxXY_variableDr(p,i,
        nBins_X1=96,
        nBins_X2=96,
    distances=dr_layerbylayer_200))
chains.register_backend2("Histomaxbin4dr200shape15",
        lambda p,i : clustering3d.create_histoMaxXY_variableDr(p,i,
        nBins_X1=96,
        nBins_X2=96,
    distances=dr_layerbylayer_200,
    shape_threshold=1.5))
# Register selector
chains.register_selector("Genmatch",
        selectors.create_genmatch)
# Register ntuples
# Store gen info only in the reference ntuple
ntuple_list = ['event', 'gen', 'multiclusters']
chains.register_ntuple("Genclustersntuple", lambda p,i : ntuple.create_ntuple(p,i, ntuple_list))

# Register trigger chains
concentrator_algos = ['Supertriggercell', 'Supertriggercell4444fixed', 'Equalshare', 'Onebit']
backend_algos = ['Histomaxbin4', 'Histomaxbin4dr50', 'Histomaxbin4dr200']
## Make cross product fo ECON and BE algos
import itertools
for cc,be in itertools.product(concentrator_algos,backend_algos):
    if 'Supertriggercell' in cc:
        # Use a shape threshold of 1.5 mipT for STC
        chains.register_chain('Floatingpoint8', cc, 'Dummy', be+'shape15', 'Genmatch', 'Genclustersntuple')
    else:
        chains.register_chain('Floatingpoint8', cc, 'Dummy', be, 'Genmatch', 'Genclustersntuple')


process = chains.create_sequences(process)

# Remove towers from sequence
process.hgcalTriggerPrimitives.remove(process.hgcalTowerMap)
process.hgcalTriggerPrimitives.remove(process.hgcalTower)

process.hgcl1tpg_step = cms.Path(process.hgcalTriggerPrimitives)
process.selector_step = cms.Path(process.hgcalTriggerSelector)
process.ntuple_step = cms.Path(process.hgcalTriggerNtuples)

# Schedule definition
process.schedule = cms.Schedule(process.hgcl1tpg_step, process.selector_step, process.ntuple_step)

# Add early deletion of temporary data products to reduce peak memory need
from Configuration.StandardSequences.earlyDeleteSettings_cff import customiseEarlyDelete
process = customiseEarlyDelete(process)
# End adding early deletion

