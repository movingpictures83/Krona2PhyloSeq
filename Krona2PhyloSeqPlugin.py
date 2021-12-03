import sys
import PyPluMA

class Krona2PhyloSeqPlugin:
    def input(self, infile):
       self.filelist = open(infile, 'r')

    def run(self): 
       self.taxtab = dict()
       self.taxtree = dict()


       newtaxon = 1
       self.samples = []

       for line in self.filelist:
         contents2 = line.strip().split(',')
         sample = contents2[0].replace('_','')
         self.samples.append(sample)
         filename = PyPluMA.prefix()+"/"+contents2[1]
         kronafile = open(filename, 'r')
         for line in kronafile:
           contents = line.strip().replace(',', '').split('\t')
           count = float(contents[0])
           highestindex = len(contents)-1
           if (highestindex == 3):
               prefix = "(Kingdom)"
           elif (highestindex == 4):
               prefix = "(Phylum)"
           elif (highestindex == 5):
               prefix = "(Class)"
           elif (highestindex == 6):
               prefix = "(Order)"
           elif (highestindex == 7):
               prefix = "(Family)"
           elif (highestindex == 8):
               prefix = "(Genus)"
           elif (highestindex == 9):
               prefix = "(Species)"
           else:
               prefix = "(Unclassified)"

           if (3 > highestindex):
               mydata = prefix+contents[highestindex]
           else:
               mydata = contents[3]
           if (4 > highestindex):
               mydata += "&"+prefix+contents[highestindex]
           else:
               mydata += "&"+contents[4]
           if (5 > highestindex):
               mydata += "&"+prefix+contents[highestindex]
           else:
               mydata += "&"+contents[5]
           if (6 > highestindex):
               mydata += "&"+prefix+contents[highestindex]
           else:
               mydata += "&"+contents[6]
           if (7 > highestindex):
               mydata += "&"+prefix+contents[highestindex]
           else:
               mydata += "&"+contents[7]
           if (8 > highestindex):
               mydata += "&"+prefix+contents[highestindex]
           else:
               mydata += "&"+contents[8]
           if (9 > highestindex):
               mydata += "&"+prefix+contents[highestindex]
           else:
               mydata += "&"+contents[9]
           if (10 > highestindex):
               mydata += "&"+prefix+contents[highestindex]
           else:
               mydata += "&"+contents[10]

           if (mydata not in self.taxtree):
               self.taxtree[mydata] = "TAX"+str(newtaxon)
               newtaxon += 1
    
           count = float(contents[0])
           if (sample not in self.taxtab):
               self.taxtab[sample] = dict()
           self.taxtab[sample][self.taxtree[mydata]] = count

    def output(self, filename):
       self.taxtabfile = open(filename+".tab.csv", 'w')
       self.taxtreefile = open(filename+".tax.csv", 'w')

       self.taxtabfile.write('\"\"')
       self.taxtreefile.write('\"\",\"Kingdom\",\"Phylum\",\"Class\",\"Order\",\"Family\",\"Genus\",\"Species\",\"Strain\"\n')
       for sam in self.samples:
           self.taxtabfile.write(','+sam)
       self.taxtabfile.write('\n')

       for taxon in self.taxtree:
           self.taxtabfile.write('\"'+self.taxtree[taxon]+'\"')
           for sam in self.samples:
               if (self.taxtree[taxon] in self.taxtab[sam]):
                   self.taxtabfile.write(","+str(self.taxtab[sam][self.taxtree[taxon]]))
               else:
                   self.taxtabfile.write(",0")
           self.taxtabfile.write('\n')
           self.taxtreefile.write('\"'+self.taxtree[taxon]+'\"')
           taxonomy = taxon.split('&')
           #print(taxonomy)
           for i in range(len(taxonomy)):
               self.taxtreefile.write(",\""+taxonomy[i]+'\"')
           self.taxtreefile.write('\n')
