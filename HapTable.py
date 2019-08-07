import pandas as pd
import sys

def getreads_to_bases(bf2):
    read_dict = {}
    for index, row in bf2.iterrows():
        readname = row['Reads']
        read_dict[readname] = row['Bases']
    return read_dict

def addreads(read_dict, not_found_reads, bf1, rf2, file1clusters, file2clusters):
    rowslist = []
    seq1_col = file1clusters + '_seq'
    seq2_col = file2clusters + '_seq'
    for read in not_found_reads:
        rowdict = {}
        rowdict['Reads'] = read
        rowdict[file1clusters] = 'nnn'
        rowdict[file2clusters] = read_dict.get(read)
        try:
            rowdict[seq2_col] = rf2.loc[read]['Sequence']
        except:
            pass

        rowslist.append(rowdict)

    extrarows = pd.DataFrame(rowslist)

    bf1 = bf1.append(extrarows)

    bf1 = bf1[['Reads', seq1_col, seq2_col, file1clusters, file2clusters]]

    return bf1

# def main():
def main(basesfile1, basesfile2, readsfile1, readsfile2):
    # basesfile1 = 'Bases_19pB8_c1c2_seqIDs.csv'
    # basesfile2 = 'Bases_19pB8_c3c4_seqIDs.csv'
    # readsfile1 = '19pB8_c1c2.csv'
    # readsfile2 = '19pB8_c3c4.csv'

    chrom_block = basesfile1.split('_')[1]
    file1clusters = basesfile1.split('_')[2]
    file2clusters = basesfile2.split('_')[2]

    outfile = chrom_block+'_'+file1clusters+file2clusters+'.tsv'


    bf1 = pd.read_csv(basesfile1, sep='\t', header=0, index_col=None)
    bf2 = pd.read_csv(basesfile2, sep='\t', header=0, index_col=None)

    rf1 = pd.read_csv(readsfile1, sep=',', header=None, index_col=0, skiprows=6)
    rf2 = pd.read_csv(readsfile2, sep=',', header=None, index_col=0, skiprows=6)

    rf1['Sequence'] = rf1.iloc[:, :].apply(lambda x: ''.join(x), axis=1)
    rf2['Sequence'] = rf2.iloc[:, :].apply(lambda x: ''.join(x), axis=1)
    # rf1.to_csv('outseq.csv', sep='\t')

    ##make reads to bases dict for file 2
    read_dict = getreads_to_bases(bf2)
    # print(read_dict)

    found_reads = []
    seq1_col = file1clusters+'_seq'
    seq2_col = file2clusters + '_seq'

    bf1.columns=['Reads', file1clusters]

    bf1[file2clusters] = ""
    bf1[seq1_col] = ""
    bf1[seq2_col] = ""
    # print(bf1.head(2))
    for index, row in bf1.iterrows():
        readname = row['Reads']
        # print(readname)
        row[seq1_col] = rf1.loc[readname]['Sequence']
        # print(bf1.head(2))
        if readname in read_dict:
            row[file2clusters] = read_dict.get(readname)
            row[seq2_col] = rf2.loc[readname]['Sequence']
            found_reads.append(readname)
        else:
            row[file2clusters] = 'nnn'

    ##add in reads that didn't overlap
    not_found_reads = list(set(list(read_dict)) - set(found_reads))

    bf1 = addreads(read_dict, not_found_reads, bf1, rf2, file1clusters, file2clusters)


    bf1.to_csv(outfile, sep='\t', index=None)


if __name__ == '__main__':
    basesfile1 = sys.argv[1]
    basesfile2 = sys.argv[2]
    readsfile1 = sys.argv[3]
    readsfile2 = sys.argv[4]
    main(basesfile1, basesfile2, readsfile1, readsfile2)
    # main()
