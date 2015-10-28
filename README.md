# Web-Crawler / Graphs
* Navigate to updatecsdb folder. Run <code>generateurls.py</code>, 
which will fetch all of the match URLs and create a file entitled
matchurls.csv
* Run <code>updatecsdb.py</code> to get info. from each match in 
each URL specified in matchurls.csv. This will create a file 
entitled matches.csv
* If need be, source csgo.sql for creation of appropriate tables and 
filling of said tables from the above .csv file

Number of threads and cores can be changed directly from within the
<code>updatecsdb.py</code> file on lines 17 - 20. Optionally (and not recommended), one can change the number of threads used to write to 
these files. Multiple files will be written to simultaneously, then 
merged in the end. This is determined by <code>nf</code> below.

```python
nt = 20 # Number of threads for initial HTML/URL fetching
nf = 1 # Number of files being written to, and threads writing to them
np = 6 # Number of total parallel processes to run
ng = 12 # Number of threads dedicated to fetching HTML
```

File with list of URLs can be changed on line 14:

```python
urlFile = csv.reader(open('matchurls.test', 'rb')) # Match page URLs
```



