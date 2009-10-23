"""Tests the core of the cactus atomiser/reconstruction pipeline.
"""

import unittest

import os
import sys
import random

from sonLib.bioio import parseSuiteTestOptions
from sonLib.bioio import TestStatus
from sonLib.bioio import getTempDirectory
from sonLib.bioio import getTempFile
from sonLib.bioio import logger
from sonLib.bioio import system

from cactus.cactus_common import runCactusSetup
from cactus.cactus_common import runCactusAligner
from cactus.cactus_common import runCactusCore
from cactus.cactus_common import getRandomCactusInputs
from cactus.cactus_common import runCactusCheckReconstructionTree

class TestCase(unittest.TestCase):
    
    def setUp(self):
        self.testNo = TestStatus.getTestSetup(1, 100, 0, 0)
        self.tempDir = getTempDirectory(os.getcwd())
        unittest.TestCase.setUp(self)
    
    def tearDown(self):
        unittest.TestCase.tearDown(self)
        system("rm -rf %s" % self.tempDir)
        system("rm -rf pinchGraph1.dot pinchGraph2.dot pinchGraph3.dot pinchGraph4.dot cactusGraph1.dot cactusGraph2.dot cactusGraph3.dot net1.dot net2.dot net3.dot pinchGraph5.dot pinchGraph6.dot")
        system("rm -rf pinchGraph1.pdf pinchGraph2.pdf pinchGraph3.pdf pinchGraph4.pdf cactusGraph1.pdf cactusGraph2.pdf cactusGraph3.pdf net1.pdf net2.pdf net3.pdf pinchGraph5.pdf pinchGraph6.pdf")
    
    def testChromosomes(self):
        """Tests cactus_core on the alignment of 4 whole chromosome X's, human, chimp, mouse, dog.
        """
        if TestStatus.getTestStatus() in (TestStatus.TEST_VERY_LONG,):
            chrXPath = os.path.join(TestStatus.getPathToDataSets(), "chr_x")
            sequences = [ os.path.join(chrXPath, seqFile) for seqFile in ("hg18.fa", "panTro2.fa", "mouse_chrX.fa", "dog_chrX.fa") ]
            newickTreeString = '(((h:0.006969, c:0.009727):0.13, m:0.36):0.02, d:0.15);'
            runPipe(sequences, newickTreeString, self.tempDir)
    
    def testCactusWorkflow_Encode(self): 
        """Run the workflow on the encode pilot regions.
        """
        if TestStatus.getTestStatus() in (TestStatus.TEST_LONG,):
            encodeDatasetPath = os.path.join(TestStatus.getPathToDataSets(), "MAY-2005")
            newickTreeString = "(((((((((HUMAN:0.006969, CHIMP:0.009727):0.025291, BABOON:0.044568):0.11,((MOUSE:0.072818, RAT:0.081244):0.260342, RABBIT):0.26):0.023260,(DOG:0.094381,COW:0.164728):0.04),ELEPHANT:0.5),MONODELPHIS:0.7),PLATYPUS:0.9),CHICKEN:1.1),ZEBRAFISH:1.5);"
            for encodeRegion in [ "ENm00" + str(i) for i in xrange(1, 2) ]:
                sequences = [ os.path.join(encodeDatasetPath, encodeRegion, ("%s.%s.fa" % (species, encodeRegion))) for\
                             species in ("human", "chimp", "baboon", "mouse", "rat", "rabbit", "dog", "cow", "elephant", "monodelphis", "platypus", "chicken", "zebrafish") ]
                runPipe(sequences, newickTreeString, self.tempDir)
    
    def testCactusCore(self):
        for test in xrange(self.testNo):
            sequenceDirs, newickTreeString = getRandomCactusInputs(tempDir=getTempDirectory(self.tempDir))
            runPipe(sequenceDirs, newickTreeString, self.tempDir, useDummy=True, writeDebugFiles=True,
                    randomAtomParameters=True)
            
            ##########################################
            #Make neatos
            ##########################################
            """
            system("neato pinchGraph1.dot -Tpdf > pinchGraph1.pdf") 
            system("neato pinchGraph2.dot -Tpdf > pinchGraph2.pdf")
            system("neato pinchGraph3.dot -Tpdf > pinchGraph3.pdf")
            system("neato pinchGraph4.dot -Tpdf > pinchGraph4.pdf")
            system("neato pinchGraph5.dot -Tpdf > pinchGraph5.pdf")
            system("neato pinchGraph6.dot -Tpdf > pinchGraph6.pdf")
            system("neato cactusGraph1.dot -Tpdf > cactusGraph1.pdf")
            system("neato cactusGraph2.dot -Tpdf > cactusGraph2.pdf")
            system("neato cactusGraph3.dot -Tpdf > cactusGraph3.pdf")
            """
            
            
def runPipe(sequenceDirs, newickTreeString, tempDir, useDummy=False, writeDebugFiles=False, randomAtomParameters=False):
    tempAlignmentFile = getTempFile(rootDir=tempDir)
    tempReconstructionDirectory = os.path.join(getTempDirectory(tempDir), "tempReconstruction")
    
    runCactusSetup(tempReconstructionDirectory, sequenceDirs, 
                   newickTreeString, getTempDirectory(tempDir))
    runCactusAligner(tempReconstructionDirectory, tempAlignmentFile,
                     tempDir=getTempDirectory(tempDir), useDummy=useDummy)
    
    system("cat %s" % tempAlignmentFile)
    
    logger.info("Constructed the alignments")
    if randomAtomParameters:
        runCactusCore(tempReconstructionDirectory, tempAlignmentFile, 
                      tempDir=getTempDirectory(tempDir), 
                      writeDebugFiles=writeDebugFiles,
                      maximumEdgeDegree=1+random.random()*100,
                      proportionOfAtomsToKeep=random.random(),
                      discardRatio=random.random()*2,
                      minimumTreeCoverage=random.random(),
                      minimumChainLength=random.random()*5)
    else:
        runCactusCore(tempReconstructionDirectory, tempAlignmentFile, 
                      tempDir=getTempDirectory(tempDir), writeDebugFiles=writeDebugFiles)
    
    #runCactusCheckReconstructionTree(tempReconstructionDirectory, checkAdjacencies=False)
    
    system("rm -rf %s %s" % (tempReconstructionDirectory, tempAlignmentFile))
    
    logger.info("Ran the test of the reconstruction program okay")
        
def main():
    parseSuiteTestOptions()
    sys.argv = sys.argv[:1]
    unittest.main()
        
if __name__ == '__main__':
    main()