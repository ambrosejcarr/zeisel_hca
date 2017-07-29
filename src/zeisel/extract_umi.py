import sys
from seqc.sequence import fastq


def extract_umi(fastq_input, fastq_output):
    """extract umi from read

    :param fastq_output: umi prepended to name
    :param fastq_input: linnarrson fastq file
    """
    rd = fastq.Reader(fastq_input)
    with open(fastq_output, 'wb') as fout:
        for record in rd:

            # don't want malformed reads resulting from duplicate line termination
            if len(record) <= 10:
                continue

            # find the umi, drop the G sequences
            umi = record.sequence[:6]
            i = 0
            while i < 5:
                if not record.sequence[6:] == b'G':
                    break
                i += 1

            # prepend umi, remove unalignable sequence, write output
            record.add_annotation((umi,))
            record.quality = record.quality[6 + i:]
            record.sequence = record.sequence[6 + i:]
            fout.write(bytes(record))


def print_help():
    """print help if requested or if script is miss-called"""
    print('\nExtract UMI from Linnarrson fastq file to produce an alignable fastq file.\n'
          'Usage: python3 extract_umi.py <linnarrson_file.fastq> <output_filename.fastq>'
          '\n')


if __name__ == "__main__":
    # script takes two fastq files
    if any(arg in ['-h', '--help'] for arg in sys.argv) or len(sys.argv) != 3:
        print_help()
    else:
        try:
            extract_umi(*sys.argv[1:])
        except:
            print_help()
            raise


