import pandas as pd
import pysam
import sys

def filetolist(file):
    with open(file, 'r') as f:
        l = f.readlines()
    l = [x.strip() for x in l]
    return l

def main(bamfile, start, end, chr, ReadBasesfile):
# def main():
#     chr = '1'
#     start = 635380
#     end = 640380
#     bamfile = './sorted1pB8_c1c2.bam'
#     ReadBasesfile = './1pB8_c1c2ReadBases.txt'
    Readfile = './Read.txt'
    Spotsfile = './Spots.txt'
    name = ReadBasesfile.split('/')[-1].split('R')[0]
    outfile = name + '_Linedupreads.txt'


    samfile = pysam.AlignmentFile(bamfile, "rb")
    position_dict = {}
    for read in samfile.fetch(chr, start, end):
        read_name = read.qname
        start_pos = read.pos
        end_pos = read.positions[-1]
        position_dict[read_name] = (start_pos, end_pos)
    # print(position_dict)

    reads = filetolist(Readfile)
    spots = filetolist(Spotsfile)

    base_df = pd.read_csv(ReadBasesfile, header=None, sep='\t')
    base_df.columns = ['Position', 'Reads', 'x', 'y', 'Base']
    # print(base_df.head(2))
    base_dict = {}
    for index, row in base_df.iterrows():
        pos = str(row['Position'])
        readname = row['Reads'].strip()
        if readname in reads:
            base_dict[(readname, pos)] = row['Base']

    outstring = ''
    for read in reads:
        for spot in spots:
            tup = (read, spot)
            if tup in base_dict.keys():
                outstring = outstring + base_dict[tup].strip() + ','
            elif read in position_dict.keys():
                s = position_dict[read][0]
                e = position_dict[read][1]
                if int(spot) > int(s) and int(spot) < int(e):
                    outstring = outstring + 'N,'
                else:
                    outstring = outstring + 'X,'
            else:
                outstring = outstring + 'X,'

        outstring = outstring + '\n'

    with open(outfile, 'w') as o:
        o.write(outstring)




if __name__ == '__main__':
    bamfile = sys.argv[1]
    start = int(sys.argv[2])
    end = int(sys.argv[3])
    chr = sys.argv[4]
    ReadBasesfile = sys.argv[5]
    main(bamfile, start, end, chr, ReadBasesfile)
    # main()