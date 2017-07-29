import subprocess


def align(fastq, prefix, index):
    """ align a de-identified star

    :param index: location of star index
    :param fastq: input fastq file
    :param prefix: output file prefix for STAR alignment results
    """
    cmd = (
        'STAR '
        '--genomeDir {INDEX} '
        '--readFilesIn {FASTQ} '
        '--outFileNamePrefix {PREFIX} '  # think about this one
        '--genomeLoad LoadAndKeep '
        '--runThreadN 2'
    ).format(INDEX=index, FASTQ=fastq, PREFIX=prefix)

    p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    out, err = p.communicate()
    if err:
        raise ChildProcessError(err.decode())
