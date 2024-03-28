
import FWCore.ParameterSet.Config as cms
from Configuration.Generator.Pythia8CommonSettings_cfi import *
from Configuration.Generator.MCTunes2017.PythiaCP5Settings_cfi import *
from GeneratorInterface.EvtGenInterface.EvtGenSetting_cff import *

generator = cms.EDFilter("Pythia8GeneratorFilter",
                         pythiaPylistVerbosity = cms.untracked.int32(0), # If 0: particle has no open decay channels
                         pythiaHepMCVerbosity = cms.untracked.bool(False),
                         comEnergy = cms.double(13000.0),
                         maxEventsToPrint = cms.untracked.int32(0),
                         ExternalDecays = cms.PSet(
                         EvtGen130 = cms.untracked.PSet(
                         #uses latest evt and decay tables from evtgen 1.6
                         decay_table = cms.string('GeneratorInterface/EvtGenInterface/data/DECAY_2014_NOLONGLIFE.DEC'),
                         particle_property_file = cms.FileInPath('GeneratorInterface/EvtGenInterface/data/evt_2014.pdl'),
                         convertPythiaCodes = cms.untracked.bool(False),
                         list_forced_decays = cms.vstring('MyD0', 'Myanti-D0'), 
                         operates_on_particles = cms.vint32( 413, -413, 421, -421),
                         user_decay_embedded= cms.vstring(
"""

Alias      MyD0        D0
Alias      Myanti-D0   anti-D0
ChargeConj MyD0 Myanti-D0

Decay MyD0
  1.000        K-      pi+              PHSP;
Enddecay
CDecay Myanti-D0


End
"""
                          ),
                ),
                parameterSets = cms.vstring('EvtGen130')
        ),
        PythiaParameters = cms.PSet(
        pythia8CommonSettingsBlock,
        pythia8CP5SettingsBlock,
        processParameters = cms.vstring(
            'Main:timesAllowErrors = 10000',  
            'HardQCD:hardccbar = on', # Sum of gg -> ccbar with qqbar ->ccbar
            'HardQCD:gg2gg = on',
            'HardQCD:qg2qg = on',
            'PartonLevel:MPI = on', #MPI: multiple parton interaction
            'SecondHard:Charmonium = on',
            'SecondHard:generate = on',
            'PhaseSpace:pTHatMin = 50.0',
            'PhaseSpace:pTHatMinSecond = 4.0',
            'PhaseSpace:pTHatMinDiverge = 0.5',
            ),
        parameterSets = cms.vstring('pythia8CommonSettings',
                                    'pythia8CP5Settings',
                                    'processParameters',
                                    )
        )
                         )

generator.PythiaParameters.processParameters.extend(EvtGenExtraParticles)
###########
# Filters #
###########
# Filter only pp events which produce Psi
psifilter = cms.EDFilter("PythiaFilter", 
    ParticleID = cms.untracked.int32(100443),
    MinPt           = cms.untracked.double(50.0),
    MaxPt           = cms.untracked.double(100.0),
    MinEta          = cms.untracked.double(-2.4),
    MaxEta          = cms.untracked.double(2.4)
)

# Dimuon filter
mumufilter = cms.EDFilter("MCParticlePairFilter",
    Status = cms.untracked.vint32(1, 1),
    MinP = cms.untracked.vdouble(2.7, 2.7),
    MinPt = cms.untracked.vdouble(2.0, 2.0),
    MaxPt = cms.untracked.vdouble(100, 100),
    MaxEta = cms.untracked.vdouble(2.4, 2.4),
    MinEta = cms.untracked.vdouble(-2.4, -2.4),
    ParticleCharge = cms.untracked.int32(-1),
    ParticleID1 = cms.untracked.vint32(13),
    ParticleID2 = cms.untracked.vint32(13),
    MinInvMass = cms.untracked.double(3.586),
    MaxInvMass = cms.untracked.double(3.786),

)

# Filter for D* -> D0(kaonPion) pionslow 


# Test with the official filter


DstarFilter = cms.EDFilter("PythiaMomDauFilter",
    ChargeConjugation = cms.untracked.bool(True),
    MomMinPt = cms.untracked.double(1.5),
    MomMaxPt = cms.untracked.double(100.0),
    MomMinEta = cms.untracked.double(-2.5), # Dstar eta
    MomMaxEta = cms.untracked.double(2.5),
    DaughterID = cms.untracked.int32(421),
    DaughterIDs = cms.untracked.vint32(421, 211), # D* daughters
    DescendantsIDs = cms.untracked.vint32(-321, 211),
    MaxEta = cms.untracked.double(2.5),
    MinEta = cms.untracked.double(-2.5),
    MinPt = cms.untracked.double(0.2),
    NumberDaughters = cms.untracked.int32(2),
    NumberDescendants = cms.untracked.int32(2),
    ParticleID = cms.untracked.int32(413)
)



ProductionFilterSequence = cms.Sequence(generator*psifilter*mumufilter*DstarFilter)
