import csv
from Bio import SeqIO
from Bio.Blast import NCBIWWW

__author__ = "Ben Santos"
__email__ = "santosb@carleton.edu"

class gene:
    '''
    gene.py allows the user to create objects out of genes
    The gene objects will carry information regarding the genes themselves
    When running, change the filenames accordingly = all information
    is parsed from text files.
    '''
    def __init__(self):
        #id's of the gene, start as None, can be reassigned later
        self.MSTRG = None
        self.DPMN = None

        #the fc, pval, and qval of a gene. start as 0, can be reassigned
        self.fc = 0
        self.pval = 0
        self.qval = 0

        #chromosomeNumber and start and end of sequences
        self.chromosomeNumber = 0
        self.chromosomeStartIndex = 0
        self.chromosomeEndIndex = 0

    '''
    Creates an object of a single gene from the provided csv file

    PARAMETERS:
        filename - the name of the csv file (code was written based on the column names feautre,
        id, fc, psval, qval)
        index - the row of the csv file containing the desired gene (e.g. row 22 of the csv file -> index = 22)
    '''

    def initializeSingleGene(self, filename, index):
        #this line opens the file and closes it after the program runs
        with open(filename) as csv_file:

            #setting up the csv reader
            csv_reader = csv.reader(csv_file, delimiter =',')

            #gene of interest is returned as a list of a list, with indexes corresponding
            #to the different attributes of the gene
            index -=1
            geneOfInterest = [row for idx, row in enumerate(csv_reader) if idx == index]

            #assigning instance variables from the geneOfInterest
            #fetches proper id's
            id = str(geneOfInterest[0][1])
            if "|" in id:
                self.MSTRG = id.split('|')[0]
                self.DPMN = id.split('|')[1]
            else:
                self.MSTRG = id

            #assigns certain values
            self.fc = float(geneOfInterest[0][2])
            self.pval = float(geneOfInterest[0][3])
            self.qval = float(geneOfInterest[0][4])


            if "|" in id:
                print("Gene successfully initialized.\nMSTRG id = " + self.MSTRG +"\nDPMN id = " + self.DPMN +
                "\nfc = " + str(self.fc) + "\npval = " + str(self.pval) + "\nqval = " + str(self.qval) +"\n")
            else:
                print("Gene successfully initialized.\nMSTRG id = " + self.MSTRG +"\nDPMN id = None" +
                "\nfc = " + str(self.fc) + "\npval = " + str(self.pval) + "\nqval = " + str(self.qval) +"\n")

    '''
    This function takes the gene object and finds the corresponding chromosome number
    NOTE: gene must be intialized (initializeSingleGene()) for this function to work
    chromosomeNumber eturned as a string. this will make easier for searching rest of file
    '''

    def findChromosomeNumber(self, mergeFilename):
        with open(mergeFilename, "r") as mergeFile:
            if self.MSTRG != None:
                for line in mergeFile:
                    if self.MSTRG in line:
                        self.chromosomeNumber = line.split(None ,1)[0]
                        return self.chromosomeNumber
            elif self.DPMN != None:
                for line in mergeFile:
                    if self.DPMN in line:
                        self.chromosomeNumber = line.split(None ,1)[0]
                        return self.chromosomeNumber

    #find and returns indexes as floats. these will be used later for slicing
    def findSequenceStartIndex(self, mergeFilename):
        with open(mergeFilename, "r") as mergeFile:
            if self.MSTRG != None:
                for line in mergeFile:
                    if self.MSTRG in line:
                        #this is the line that actually splices the file.
                        #if you change the layout of the merge file, this line will have to be adjusted
                        self.chromosomeStartIndex = int(line.split(None ,5)[3])
                        return self.chromosomeStartIndex
            elif self.DPMN != None:
                for line in mergeFile:
                    if self.DPMN in line:
                        self.chromosomeStartIndex = int(line.split(None ,5)[3])
                        return self.chromosomeStartIndex

    def findSequenceEndIndex(self, mergeFilename):
        with open(mergeFilename, "r") as mergeFile:
            if self.MSTRG != None:
                for line in mergeFile:
                    if self.MSTRG in line:
                        self.chromosomeEndIndex = int(line.split(None ,5)[4])
                        self.chromosomeEndIndex
                        return self.chromosomeEndIndex
            elif self.DPMN != None:
                for line in mergeFile:
                    if self.DPMN in line:
                        self.chromosomeEndIndex = int(line.split(None ,5)[4])
                        self.chromosomeEndIndex
                        return self.chromosomeEndIndex

    '''
    Returns the sequence indicated by the start and end indexes of the gene.
    Use SeqIO to parse the fasta file.

    PARAMETERS - just the fasta file

    Returns: the spliced sequence as a string. To be used in BLAST searches
    '''

    def spliceSequence(self, mergeFilename, fastaFile):
        self.findChromosomeNumber(mergeFilename)
        self.findSequenceStartIndex(mergeFilename)
        self.findSequenceEndIndex(mergeFilename)
        with open(fastaFile, "rU") as handle:
            for record in SeqIO.parse(handle, "fasta"):
                #record id will match a chromosome number (e.g. "chr7" or "chr2")
                #once it finds the record that matches the chromosomeNumber of the gene object, it performs the splice
                if record.id == self.chromosomeNumber:
                    start = self.chromosomeStartIndex - 1
                    end = self.chromosomeEndIndex
                    slicedSequence = record.seq[start:end]
                    return slicedSequence

    def blastSearchSequence(self, slicedSequence):
        blast_result = NCBIWWW.qblast("blastn","nt",slicedSequence)
        print(blast_result)

        with open("blastresult.txt", "w") as resultfile:
            blastresult = blast_result.read()
            resultfile.write(blastresult)
        print("pass")

    '''
    After Gene is initialized, returns lits of the PFAM and EggNog id's
    PARAMERTERS - the annotated Zebra Mussel. Code is heavily dependent on layout of file.
    Returns - PFAMlist = list of all the pFAM values associated with the DPMN id of the gene
            - EggNogList = list of all the EggNog values associated with the DPMN id of the gene
    '''
    def retrieveEggNogAndPFAM(self, annotFilename):

        try:
            print(self.DPMN)
            with open(annotFilename, "r+") as annotFile:
                for line in annotFile:
                    if self.DPMN in line:
                        EggNogList = []
                        PFAMList = []
                        #once the id is recgonized in a line, the code will run and pick out all PFAM and EggNog ids
                        #until the word "translation" is reached. translation seems to always mark the final attirbute
                        #of a gene before a new one starts n the file, so that is why I stopped it here
                        for i in range(0,10000):


                            if "translation" in line:
                                return EggNogList, PFAMList

                            if "EggNog" in line:
                                eggNogString = line
                                eggNogStringClean = eggNogString.strip()[7:-1]
                                EggNogList.append(eggNogStringClean)

                            if "db_xref" in line:
                                PFAMString = line
                                PFAMStringClean = PFAMString.strip()[15:-1]
                                PFAMList.append(PFAMStringClean)
                            line = next(annotFile)

        except:
            if self.DPMN == None:
                print("There is no DPMN id for this gene (see csv file)")
            else:
                print("There are no EggNog or PFAM values for this gene")






def main():
    csvfilename = "Dpoly_genes_qlt05_results.csv"
    mergeFilename = "stringtie_merged_wNames.gtf"
    fastaFile = "Dpolymorpha_Assembly.V2.Final_wMito.fasta"
    annotFilename = "zebraMussel_refAnnot.gbk"

    genetest = gene()
    genetest.initializeSingleGene(csvfilename,2)

    #print(genetest.findChromosomeNumber(mergeFilename))
    #print(genetest.findSequenceStartIndex(mergeFilename))
    #print(genetest.findSequenceEndIndex(mergeFilename))
    #print(genetest.spliceSequence(mergeFilename, fastaFile))
    #genetest.blastSearchSequence(genetest.spliceSequence("Dpolymorpha_Assembly.V2.Final_wMito.fasta"))
    print(genetest.retrieveEggNogAndPFAM(annotFilename))

main()
