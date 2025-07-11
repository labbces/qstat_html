# qstat_html
Produce stats from SGE's QSTAT in HTML
 
There is a couple of python scripts that show current usage and some statsitics of our [Bioinformatics cluster at CENA/USP](https://labbces.cena.usp.br/infra/qstatCluster.html)

For all python script to work the following environment is required:

```
python3 -m venv myenv
source myenv/bin/activate
pip install pandas numpy seaborn matplotlib
pip freeze > requirements.txt
```

We have an script to test the python environment:

```
python3 test_env.py 

✅ Built-in modules loaded.

📦 Module locations:
pandas:     /home/riano/qstat_html/myenv/lib/python3.8/site-packages/pandas/__init__.py
numpy:      /home/riano/qstat_html/myenv/lib/python3.8/site-packages/numpy/__init__.py
seaborn:    /home/riano/qstat_html/myenv/lib/python3.8/site-packages/seaborn/__init__.py
matplotlib: /home/riano/qstat_html/myenv/lib/python3.8/site-packages/matplotlib/__init__.py
pyplot:     /home/riano/qstat_html/myenv/lib/python3.8/site-packages/matplotlib/pyplot.py

🐍 Python executable: /home/riano/qstat_html/myenv/bin/python3

```
