#!/usr/bin/env python
"""
This is a small script that does the equivalent of multicrab.
"""
import os
from optparse import OptionParser

from CRABAPI.RawCommand import crabCommand
from CRABClient.ClientExceptions import ClientException
from httplib import HTTPException

def getOptions():
    """
    Parse and return the arguments provided by the user.
    """
    usage = ("Usage: %prog --crabCmd CMD [--workArea WAD --crabCmdOpts OPTS]"
             "\nThe multicrab command executes 'crab CMD OPTS' for each project directory contained in WAD"
             "\nUse multicrab -h for help")

    parser = OptionParser(usage=usage)

    parser.add_option('-c', '--crabCmd',
                      dest = 'crabCmd',
                      default = '',
                      help = "crab command",
                      metavar = 'CMD')

    parser.add_option('-w', '--workArea',
                      dest = 'workArea',
                      default = '',
                      help = "work area directory (only if CMD != 'submit')",
                      metavar = 'WAD')

    parser.add_option('-o', '--crabCmdOpts',
                      dest = 'crabCmdOpts',
                      default = '',
                      help = "options for crab command CMD",
                      metavar = 'OPTS')

    (options, arguments) = parser.parse_args()

    if arguments:
        parser.error("Found positional argument(s): %s." % (arguments))
    if not options.crabCmd:
        parser.error("(-c CMD, --crabCmd=CMD) option not provided.")
    if options.crabCmd != 'submit':
        if not options.workArea:
            parser.error("(-w WAR, --workArea=WAR) option not provided.")
        if not os.path.isdir(options.workArea):
            parser.error("'%s' is not a valid directory." % (options.workArea))

    return options


def main():

    options = getOptions()

    # The submit command needs special treatment.
    if options.crabCmd == 'submit':

        #--------------------------------------------------------
        # This is the base config:
        #--------------------------------------------------------
        from CRABClient.UserUtilities import config, getUsernameFromSiteDB
        config = config()

        #basedir = '/uscms/home/mreid/CRAB/signal_region_analysis/CMSSW_10_2_1/src/Firefighter/washAOD/data/iDM/2018/GenFilter/'

        config.General.workArea = 'crab'
        config.General.transferOutputs = True
        config.General.transferLogs = True

        config.JobType.pluginName = 'Analysis'
        config.JobType.psetName = 'iDMAnalyzer_cfg.py'
        #config.JobType.psetName = 'python/iDMAnalyzer_cfg.py'
        #config.JobType.maxMemoryMB = 4000
        #config.JobType.numCores = 1


        #config.Data.outputPrimaryDataset = 'TrigRecoEffStudies'
        config.Data.splitting = 'Automatic'
        #config.Data.unitsPerJob = 1
        config.Data.outLFNDirBase = '/store/group/lpcmetx/iDM/Ntuples/2018/backgrounds'
        config.Data.publication = False

        #config.Site.ignoreGlobalBlacklist = True
        #config.Site.blac = ['T3_RU_FIAN', 'T3_US_MIT', 'T3_US_UCD',
        #'T3_CO_Uniandes', 'T3_US_NotreDame', 
        #'T3_IN_PUHEP', 'T3_UK_ScotGrid_ECDF', 'T3_BY_NCPHEP',
        #'T2_CH_CERN_HLT', 'T3_CH_CERN_HelixNebula', 'T3_IN_TIFRCloud',
        #'T0_CH_CERN', 'T3_GR_IASA', 'T3_CN_PKU', 'T0_CH_CSCS_HPC',
        #'T3_IR_IPM', 'T2_RU_ITEP', 'T3_US_JHU', 'T3_US_Kansas',
        #'T3_US_FSU', 'T3_KR_UOS', 'T3_CH_PSI']
        #config.Site.whitelist = ["T3_US_FNALLPC"]
        config.Site.storageSite = 'T3_US_FNALLPC'

        #--------------------------------------------------------

        # Will submit one task for each of these input datasets.
#        samples = {
#                'DYJetsToLL_M-50': '/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1/AODSIM',
#                'ZZTo2L2Nu': '/ZZTo2L2Nu_TuneCP5_13TeV_powheg_pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15_ext1-v2/AODSIM'
#        }
	QCD_sample = {
		'QCD_bEnriched_HT100to200':'/QCD_bEnriched_HT100to200_TuneCP5_13TeV-madgraph-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1/AODSIM',
		'QCD_bEnriched_HT200to300':'/QCD_bEnriched_HT200to300_TuneCP5_13TeV-madgraph-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v2/AODSIM',
		'QCD_bEnriched_HT300to500':'/QCD_bEnriched_HT300to500_TuneCP5_13TeV-madgraph-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v2/AODSIM',
		'QCD_bEnriched_HT500to700':'/QCD_bEnriched_HT500to700_TuneCP5_13TeV-madgraph-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v2/AODSIM',
		'QCD_bEnriched_HT700to1000':'/QCD_bEnriched_HT700to1000_TuneCP5_13TeV-madgraph-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v2/AODSIM',
		'QCD_bEnriched_HT1000to1500':'/QCD_bEnriched_HT1000to1500_TuneCP5_13TeV-madgraph-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v2/AODSIM',
		'QCD_bEnriched_HT1500to2000':'/QCD_bEnriched_HT1500to2000_TuneCP5_13TeV-madgraph-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v2/AODSIM',
		'QCD_bEnriched_HT2000toInf':'/QCD_bEnriched_HT2000toInf_TuneCP5_13TeV-madgraph-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v2/AODSIM'
	}
	TT_sample = {
		'TTTo2L2Nu':'/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1/AODSIM',
		'TT_diLept':'/TT_DiLept_TuneCP5_13TeV-amcatnlo-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15_ext1-v2/AODSIM',
		'TTJets':'/TTJets_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1/AODSIM'
	}
	Zjets_sample = {
		'ZJetsToNuNu_HT-100To200':'/ZJetsToNuNu_HT-100To200_13TeV-madgraph/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1/AODSIM',
		'ZJetsToNuNu_HT-200To400':'/ZJetsToNuNu_HT-200To400_13TeV-madgraph/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1/AODSIM'
	}
	Wjets_sample = {
		'WJetsToLNu':'/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v2/AODSIM',
		'WJetsToLNu_HT-70To100':'/WJetsToLNu_HT-70To100_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1/AODSIM',
		'WJetsToLNu_HT-100To200':'/WJetsToLNu_HT-100To200_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1/AODSIM',
		'WJetsToLNu_HT-200To400':'/WJetsToLNu_HT-200To400_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1/AODSIM',
		'WJetsToLNu_HT-400To600':'/WJetsToLNu_HT-400To600_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1/AODSIM'
	}
	DY_sample = {
		#'DYJetsToTauTau':'/DYJetsToTauTau_ForcedMuDecay_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v2/AODSIM',
		'DYJetsToLL':'/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1/AODSIM'
	}
	Di_sample = {
		'WZTo3LNu':'/WZTo3LNu_TuneCP5_13TeV-powheg-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15_ext1-v2/AODSIM',
		'WWJJToLNuLNu':'/WWJJToLNuLNu_QCD_noTop_13TeV-madgraph-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15_ext1-v2/AODSIM',
		'ZZTo2L2Nu':'/ZZTo2L2Nu_TuneCP5_13TeV_powheg_pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15_ext1-v2/AODSIM',
		'WWTo2L2Nu':'/WWTo2L2Nu_NNPDF31_TuneCP5_13TeV-powheg-pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v1/AODSIM'
	}

	#samples = QCD_sample
	#samples = TT_sample
	#samples = Zjets_sample
	#samples = Wjets_sample
	samples = DY_sample
	#samples = Di_sample
        for sample, dataset in samples.items():

            config.Data.inputDataset = dataset
            config.General.requestName = 'iDMAnalysis_' + sample
            #config.Data.outputDatasetTag = sample
            #config.Data.userInputFiles = open(basedir + sample + '.list').readlines()

            # Submit.
            try:
                print "Submitting for input dataset %s with options %s" % (sample, options.crabCmdOpts)
                crabCommand(options.crabCmd, config = config, *options.crabCmdOpts.split())
            except HTTPException as hte:
                print "Submission for input dataset %s failed: %s" % (sample, hte.headers)
            except ClientException as cle:
                print "Submission for input dataset %s failed: %s" % (sample, cle)

    # All other commands can be simply executed.
    elif options.workArea:

        for dir in osdir(options.workArea):
            projDir = os.path.join(options.workArea, dir)
            if not os.path.isdir(projDir):
                continue
            # Execute the crab command.
            msg = "Executing (the equivalent of): crab %s --dir %s %s" % (options.crabCmd, projDir, options.crabCmdOpts)
            print "-"*len(msg)
            print msg
            print "-"*len(msg)
            try:
                crabCommand(options.crabCmd, dir = projDir, *options.crabCmdOpts.split())
            except HTTPException as hte:
                print "Failed executing command %s for task %s: %s" % (options.crabCmd, projDir, hte.headers)
            except ClientException as cle:
                print "Failed executing command %s for task %s: %s" % (options.crabCmd, projDir, cle)


if __name__ == '__main__':
    main()