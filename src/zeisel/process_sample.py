import sys
import multiprocessing
from functools import partial
from contextlib import closing
import os
import zeisel.extract_umi as extract_umi
import zeisel.postprocess_umi_tag as postprocess_umi_tag
import zeisel.align as align


def process_sample(fastq_file, index):
    """extract UMIs, align fastqs, append UMIs as a tag.

    :param index: location for star index
    :param fastq_file: input fastq file
    """
    stem = fastq_file.replace('.fastq.gz', '')
    out_fastq = stem + '_umi.fastq.gz'
    extract_umi.extract_umi(fastq_file, out_fastq)
    sam_prefix = stem + '_alignment/'
    os.makedirs(sam_prefix, exist_ok=True)
    align.align(out_fastq, sam_prefix, index)
    out_sam = sam_prefix + 'Aligned.out.sam'
    postprocess_umi_tag.postprocess_umi_tag(out_sam, stem + '.bam')


def main(index, *fastq_files):
    """map jobs to a multiprocessing pool"""

    func = partial(process_sample, index=index)

    with closing(multiprocessing.Pool(18)) as pool:
        pool.map(func, fastq_files)


def print_help():
    """print help if requested or if script is miss-called"""
    print(
        '\nProcess a set of Zeisel et al. fastq file for HCA Jamboree\n'
        'Usage: python3 process_sample.py <index> <file1.fastq> <file2.fastq> ... \n'
    )


if __name__ == "__main__":
    if any(arg in ['-h', '--help'] for arg in sys.argv):
        print_help()
    else:
        try:
            main(*sys.argv[1:])
        except:
            print_help()
            raise
