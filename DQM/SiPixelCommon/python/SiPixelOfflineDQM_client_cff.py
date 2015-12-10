import FWCore.ParameterSet.Config as cms

#
# This object is used to make changes for different running scenarios
#
from Configuration.StandardSequences.Eras import eras

#Client:
sipixelEDAClient = cms.EDAnalyzer("SiPixelEDAClient",
    EventOffsetForInit = cms.untracked.int32(10),
    ActionOnLumiSection = cms.untracked.bool(False),
    ActionOnRunEnd = cms.untracked.bool(True),
    HighResolutionOccupancy = cms.untracked.bool(False),
    NoiseRateCutValue = cms.untracked.double(-1.),
    NEventsForNoiseCalculation = cms.untracked.int32(100000),
    UseOfflineXMLFile = cms.untracked.bool(True),
    Tier0Flag = cms.untracked.bool(True),
    DoHitEfficiency = cms.untracked.bool(True),
    isUpgrade = cms.untracked.bool(False)	
)
# Modify for running with the Phase 1 pixel detector.
# Note that with this change the sipixelPhase1Client block below is not
# necessary, but I'll leave it for pixel upgrade experts to decide whether
# to take it out or not.
eras.phase1Pixel.toModify( sipixelEDAClient, isUpgrade=True )

sipixelPhase1Client = cms.EDAnalyzer("SiPixelEDAClient",
    EventOffsetForInit = cms.untracked.int32(10),
    ActionOnLumiSection = cms.untracked.bool(False),
    ActionOnRunEnd = cms.untracked.bool(True),
    HighResolutionOccupancy = cms.untracked.bool(False),
    NoiseRateCutValue = cms.untracked.double(-1.),
    NEventsForNoiseCalculation = cms.untracked.int32(100000),
    UseOfflineXMLFile = cms.untracked.bool(True),
    Tier0Flag = cms.untracked.bool(True),
    DoHitEfficiency = cms.untracked.bool(True),
    isUpgrade = cms.untracked.bool(True)
)

#QualityTester
sipixelQTester = cms.EDAnalyzer("QualityTester",
    qtList = cms.untracked.FileInPath('DQM/SiPixelMonitorClient/test/sipixel_tier0_qualitytest.xml'),
    prescaleFactor = cms.untracked.int32(1),
    getQualityTestsFromFile = cms.untracked.bool(True),
    label = cms.untracked.string("SiPixelDQMQTests"),
    verboseQT = cms.untracked.bool(False)
)

#Heavy Ion QualityTester
sipixelQTesterHI = sipixelQTester.clone(
    qtList = cms.untracked.FileInPath('DQM/SiPixelMonitorClient/test/sipixel_tier0_qualitytest_heavyions.xml')
)

#DataCertification:
sipixelDaqInfo = cms.EDAnalyzer("SiPixelDaqInfo")
sipixelDcsInfo = cms.EDAnalyzer("SiPixelDcsInfo")
sipixelCertification = cms.EDAnalyzer("SiPixelCertification")

#Predefined Sequences:
PixelOfflineDQMClient = cms.Sequence(sipixelEDAClient)
PixelOfflineDQMClientWithDataCertification = cms.Sequence(sipixelQTester+
                                                          sipixelEDAClient+
                                                          sipixelDaqInfo+
							  sipixelDcsInfo+
							  sipixelCertification)
PixelOfflineDQMClientNoDataCertification = cms.Sequence(sipixelQTester+
                                                          sipixelEDAClient)

PixelOfflineDQMClientWithDataCertificationHI = cms.Sequence(PixelOfflineDQMClientNoDataCertification)
PixelOfflineDQMClientWithDataCertificationHI.replace(sipixelQTester,sipixelQTesterHI)
PixelOfflinePhase1DQMClient = cms.Sequence(sipixelPhase1Client)
