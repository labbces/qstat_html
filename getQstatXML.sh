xmlfile="/home/riano/qstat_html/qstatCluster.xml"
htmlfile="/home/riano/qstat_html/qstatCluster.html"
qstat -f -u "*" -xml  > ${xmlfile}
python3 qstatXML2HTML.py > ${htmlfile}