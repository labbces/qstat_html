xmlfile="/home/riano/qstat_html/qstatCluster.xml"
htmlfile="/home/riano/qstat_html/qstatCluster.html"
qstat -f -u "*" -xml  > ${xmlfile}
python3 qstatXML2HTML.py > ${htmlfile}
scp -P 2222  ${htmlfile} labbces@thevoid:~/www/infra/qstatCluster.html