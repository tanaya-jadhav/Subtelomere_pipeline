# Takes a bamfile, chromosome number, start and end coordinates as input
# uses pysam to get number of reads at each base, generates a dataframe for coverage
# output: a png showing coverage
# -Tanaya Jadhav

import pysam
import sys
import pandas as pd
import seaborn as sns; sns.set()
import matplotlib.pyplot as plt

#start = 18735013
#end = 18737512
#chrom = 22

def main(inputbam, chrom, start, end):
    bamfile = pysam.AlignmentFile(inputbam, "rb")
    outfile = str(inputbam).split('/')[-1].split('.')[0] + '_Cov.png'
    rows = []
    for pileupcolumn in bamfile.pileup(chrom, start, end, truncate=True, ignore_orphans=False, stepper="nofilter", MIN_BASEQ=0, BAQ=0, min_base_quality=0):
        rowdict = {}
        rowdict['position'] = pileupcolumn.pos
        rowdict['cov'] = pileupcolumn.n
        rows.append(rowdict)
    df = pd.DataFrame(rows)
    plt.plot(df['position'], df['cov'])
    plt.savefig(outfile)







if __name__ == '__main__':
    inputbam = sys.argv[1]
    chrom = sys.argv[2]
    start = int(sys.argv[3])
    end = int(sys.argv[4])
    main(inputbam, chrom, start, end)