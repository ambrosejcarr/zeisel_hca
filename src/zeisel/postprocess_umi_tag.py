import pysam
import sys


def print_help():
    """print help if requested or if script is miss-called"""
    print('\nExtract UMI from Linnarrson sam filename, add as a tag, write bam.\n'
          'Usage: python3 postprocess_umi_tag.py <linnarrson_file.sam> '
          '<linnarrson_file.bam>\n')


def postprocess_umi_tag(sam_file, out_bamfile):
    """post-process a sam file, produce bam.

    :param out_bamfile: name of .bam file to be written
    :param sam_file: sam file with prepended umi (see extract_umi.py script) to post-process
    :return:
    """
    samfile = pysam.AlignmentFile(sam_file, 'r')
    try:
        with pysam.AlignmentFile(out_bamfile, "wb", header=samfile.header) as outf:
            # append a tag
            # subset the name field
            # write the line to bam
            for alignment in samfile:
                alignment.set_tag('XM', alignment.qname[:6])
                alignment.qname = alignment.qname[7:]  # strip the umi flag from the name
                outf.write(alignment)
    finally:
        samfile.close()

if __name__ == "__main__":
    # script takes two fastq files
    if any(arg in ['-h', '--help'] for arg in sys.argv) or len(sys.argv) != 3:
        print_help()
    else:
        try:
            postprocess_umi_tag(*sys.argv[1:])
        except:
            print_help()
            raise
