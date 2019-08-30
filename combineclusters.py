import pandas as pd
import sys


# def main():
def main(file1, file2):
    # file1 = '19pB2_c3.csv'
    # file2 = '19pB2_c4.csv'
    chrom = file1.split('/')[-1].split('_')[0]
    cluster1 = file1.split('/')[-1].split('_')[1].split('.')[0]
    cluster2 = file2.split('/')[-1].split('_')[1].split('.')[0]
    outfile = chrom + '_' + cluster1 + cluster2 + '.csv'

    f1 = pd.read_csv(file1, sep=',', header=0, index_col=0)
    f2 = pd.read_csv(file2, sep=',', header=0, index_col=0)

    # print(f1.shape)
    # print(f2.shape)

    f3 = pd.concat([f1, f2], axis=1)
    # merge(f2, how='outer', left_index=True, right_index=True)
    # concat([f1, f2], axis=1, join='inner')
    f3.to_csv(outfile, sep=',')




if __name__ == '__main__':
    file1 = sys.argv[1]
    file2 = sys.argv[2]
    main(file1, file2)