export SGE_CELL=default
export SGE_ARCH=lx-amd64
export SGE_ROOT=/Storage/progs/sge-8.1.9/
export SGE_CLUSTER_NAME=bioinfclustr
. "/Storage/progs/miniconda3/etc/profile.d/conda.sh"

export PATH=${SGE_ROOT}/bin/${SGE_ARCH}:$PATH

qacctfile="/home/riano/qstat_html/qAccounting.txt.gz"
pngfile="/home/riano/qstat_html/pending_vs_running_time_log10.png"
qacct -j |gzip > ${qacctfile}
python3 qacctHistogram.py -f ${qacctfile} -o ${pngfile}
scp  -i /home/riano/.ssh/id_rsa2 -P 2222  ${pngfile} labbces@thevoid:~/www/infra/pending_vs_running_time_log10.png
