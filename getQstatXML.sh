export SGE_CELL=default
export SGE_ARCH=lx-amd64
export SGE_ROOT=/Storage/progs/sge
export SGE_CLUSTER_NAME=bioinfclustr
. "/Storage/progs/miniconda3/etc/profile.d/conda.sh"

export PATH=${SGE_ROOT}/bin/${SGE_ARCH}:$PATH
xmlfile="/home/riano/qstat_html/qstatCluster.xml"
htmlfile="/home/riano/qstat_html/qstatCluster.html"
stylefile="/home/riano/qstat_html/style.css"
qstat -f -u "*" -xml  > ${xmlfile}
/Storage/progs/miniconda3/bin/python3 /home/riano/qstat_html/qstatXML2HTML.py > ${htmlfile}
scp  -i /home/riano/.ssh/id_rsa2 -P 2222  ${htmlfile} labbces@thevoid:~/www/infra/qstatCluster.html
scp  -i /home/riano/.ssh/id_rsa2 -P 2222  ${stylefile} labbces@thevoid:~/www/infra/style.css
