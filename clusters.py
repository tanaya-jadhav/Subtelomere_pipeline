import pandas as pd
import sys
import os


def main(inputfile):
    df_path = inputfile
    outcsv = df_path.split('/')[-1].split('.')[0] + "_seqIDs.csv"
    out_fasta = df_path.split('/')[-1].split('.')[0] + ".fa"
    # print(outcsv)
    df = pd.read_csv(df_path, sep=',', header=0, index_col=0)
    # print(df.head(10))

    #split into 2 dataframes with necessary information
    reads = df[5:]
    bases = df.loc[['A', 'T', 'C', 'G']]

    #get positions with highest minor allele frequencies
    positions_list = list(bases)
    # print(bases_columns)
    maf_posdict = {}
    maj_alleledict = {}
    for position in positions_list:
        base_values = pd.to_numeric(bases[position])
        # print(base_values)
        maf = base_values.nlargest(n=2, keep='last')[-1]
        major_allele = max(base_values)
        maf_posdict[position] = maf
        inv_series = {v: k for k, v in base_values.iteritems()}
        maj_alleledict[position] = inv_series[major_allele]
    # print(maf_posdict)
    # print(maf_alleledict)
    highest_maf_pos = sorted(maf_posdict, key=maf_posdict.get, reverse=True)[:3]
    # print(highest_maf_pos)


    base_num = 20 - len(positions_list)
    bases_to_add = 'A' * base_num
    # print(bases_to_add)
    counter = 0
    with open(out_fasta, 'w') as f:
        for index, row in reads.iterrows():
            seq = ""
            counter = counter + 1
            for position in positions_list:
                if position in highest_maf_pos:
                    seq = seq + row[position]
                else:
                    seq = seq + maj_alleledict[position]
            readname = ">" + "Seq" + str(counter) + '\n'
            f.write(readname)
            f.write(seq + bases_to_add  + '\n')

    reads['seq_id'] = ''
    counter = 1
    for index, row in reads.iterrows():
        readname = "Seq" + str(counter)
        row['seq_id'] = readname
        counter = counter + 1
    reads.to_csv(outcsv, sep=',')

if __name__ == '__main__':
    inputfile = sys.argv[1]
    main(inputfile)
    # main()