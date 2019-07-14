import pandas as pd
import sys


def get_reads_to_id_dict(filepath):
    df = pd.read_csv(filepath, sep=',', header=None, index_col=None, skiprows=1)
    # print(idf.head(5))
    colnum = len(list(df))
    lastcol = colnum - 1
    idf = df[[0, lastcol]]
    idf.columns = ['Reads', 'seqid']
    # print(idf2.head(2))
    read_dict = {}
    for index, row in idf.iterrows():
        seqnum = row['seqid'].split('q')[-1]
        read_dict[seqnum] = row['Reads']
    return read_dict


def map_samplestoreads(filepath, read_dict):
    mat = pd.read_csv(filepath, sep='\t', header=0)
    # print(mdf.head(2))
    mat['Reads'] = ''
    for index, row in mat.iterrows():
        samplenum = row['samples'].split('-')[-1]
        mat.loc[index, 'Reads'] = read_dict.get(samplenum)
    return mat


def main(idfile, matrixfile):
# def main():
    id_file = idfile
    matrix_file = matrixfile
    # id_file = '11pB8_c1c2_seqIDs.csv'
    # matrix_file = 'MATRIX-COUNT11pB8_c1c2.txt'
    filename = id_file.split('/')[-1]
    output = 'Bases_' + filename
    # print(output)

    read_dict = get_reads_to_id_dict(id_file)
    # print(read_dict)

    mat = map_samplestoreads(matrix_file, read_dict)
    allcolumns = list(mat)
    columns = allcolumns[1:-1]

    mat['Bases'] = ''
    for index, row in mat.iterrows():
        for column in columns:
            if row[column] == 1:
                mat.loc[index, 'Bases'] = column

    mat_final = mat[['Reads', 'Bases']].sort_values(by=['Reads'])

    mat_final.to_csv(output, sep='\t', index=None)


if __name__ == '__main__':
    idfile = sys.argv[1]
    matrixfile = sys.argv[2]
    main(idfile, matrixfile)
    # main()
