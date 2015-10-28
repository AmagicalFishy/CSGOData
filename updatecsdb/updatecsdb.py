import threading, multiprocessing, re, urllib2, urlparse, time, csv, sys, Queue, time, csdb, _strptime, os
from bs4 import BeautifulSoup, SoupStrainer
from datetime import datetime
from cooksoup import CookSoup
from containers import df_base

today = datetime.today().strftime('-%Y.%m.%d') # Current Date

# Set encoding to deal with weird things
reload(sys)
sys.setdefaultencoding("utf-8")

# Files
urlFile = csv.reader(open('matchurls.test', 'rb')) # Match page URLs
#htmlFile = csv.writer(open('csdbhtml.csv', 'wb')) # Match page HTML

nt = 20 # Number of threads for initial HTML/URL fetching
nf = 1 # Number of files being written to, and threads writing to them
np = 6 # Number of total parallel processes to run
ng = 12 # Number of threads dedicated to fetching HTML

dFile = [open('matchinfo' + str(x) + '.csv', 'wb') for x in range(nf)]
dataFile = [csv.DictWriter(dfile, df_base.keys()) for dfile in dFile]
dataFile[0].writeheader()
mainFile = open('matchinfo.csv', 'wb')
mainWriter = csv.writer(mainFile)

matchURLs = [url[0] for url in urlFile] # List of URLs

infoAttr = {'class':'covSmallHeadline', 'style':re.compile("font-weight:normal.*;float:left.*")}

# Thread Queues
mainGetQ = Queue.Queue()
mainParseQ = Queue.Queue()

#matchGetQ = multiprocessing.JoinableQueue()
matchGetQ = Queue.Queue() 
matchParseQ = multiprocessing.JoinableQueue()
dataQ = multiprocessing.JoinableQueue()

for url in matchURLs: mainGetQ.put(url)

start = time.time() # Measures time program takes
if __name__ == "__main__":
    dataList = [] # List of all match data-dictionaries

    # Get main page HTML
    print("Getting main page HTML...")
    csdb.CreateThreads(nt, csdb.GetMainURLs, mainGetQ, mainParseQ)
    time.sleep(5)

    # Parse main page URLs
    print("Parsing main page HTML...")
    csdb.CreateThreads(nt, csdb.ParseMainURLs, mainParseQ, matchGetQ)
    time.sleep(5)
    mainParseQ.join()
    # Make sure HTML processes stop running when completed
    for ii in range(ng):
        matchGetQ.put("die")

    print("Getting and parsing match HTML...")
    # Get match HTML
    getThreads = []
    for ii in range(ng):
        newThread = csdb.GetHTML(matchGetQ, matchParseQ)
        getThreads.append(newThread)
        newThread.start()

    ## Parse match HTML
    parseProcesses = []
    for ii in range(np):
        newProcess = csdb.ParseHTML(matchParseQ, dataQ)
        parseProcesses.append(newProcess)
        newProcess.start()
    
    # Write data file header and pass to thread
    writeThreads = []
    for ii in range(nf):
        writeThread = csdb.WriteFile(dataQ, dataFile[ii])
        writeThreads.append(writeThread)
        writeThread.start()

    for thread in getThreads: thread.join() # Wait for HTML
    print('HTML fetch complete.')

    # Kill all procsses
    for ii in range(np):
        matchParseQ.put("die")
    for process in parseProcesses: process.join()
    dataQ.join()
    time.sleep(5) # So thread doesn't miss any last-minute matches

    # Close writing threads
    while True:
        if dataQ.qsize() == 0: 
            for ii in range(nf):
                dataQ.put("die")
            break
    for ii in range(nf):
        writeThreads[ii].join()
        dFile[ii].close()

    # Collapse individual match .csv files into one csv file
    for ii in range(nf):
        tmp = 'matchinfo' + str(ii) + '.csv'
        tmpFile = csv.reader(open(tmp, 'rb'))
        for row in tmpFile:
            mainWriter.writerow(row)
        os.remove(tmp)
    mainFile.close()

print("Elapsed Time: " + str(time.time() - start) + "s")
