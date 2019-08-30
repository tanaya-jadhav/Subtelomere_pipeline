#Input: takes a fasta file with consensus sequences
#Output: A tsv that lists the haplotypes and the number od ambiguous bases in each
#author: Tanaya Jadhav


def main():
    consfile = '9pB2_c1c2_Tahaconsensus.fa'
    outfile = consfile.split('.')[0] + '_ambiguouscounts.tsv'
    with open(outfile, 'w') as o:
        o.write('Haplotype' + '\t' + '# of ambiguous bases' + '\n')
    with open(consfile, 'r') as i:
        lines = i.readlines()
        for line in lines:
            if line.startswith('>'):
                hap = line.strip()
            else:
                seq = line.upper()
                acount = seq.count('A')
                tcount = seq.count('T')
                gcount = seq.count('G')
                ccount = seq.count('C')
                # ncount = seq.count('N')
                ambiguous = len(seq) - acount - gcount - tcount - ccount
                with open(outfile, 'a') as o:
                    o.write(hap + '\t' + str(ambiguous) + '\n')



if __name__ == '__main__':
    main()