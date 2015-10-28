import threading, re, multiprocessing, traceback
from bs4 import BeautifulSoup
from datetime import datetime
from cooksoup import CookSoup, BakeSoup
from containers import df_base

# Create threads linked to appropriate queues
def CreateThreads(threadCount, function, inputQ, outputQ, 
        arg1 = None, arg2 = None):
    threads = [] # List of threads
    for ii in range(threadCount):
        if arg1 == None and arg2 == None:
            newThread = function(inputQ, outputQ)
        elif arg1 and arg2 == None:
            newThread = function(inputQ, outputQ, arg2)
        elif arg1 and arg2:
            newThread = function(inputQ, outputQ, arg1, arg2)

        threads.append(newThread) # Add thread to list
        newThread.start() # Begin thread process
    inputQ.join() # Wait for get queue to be empty
    for thread in threads: 
        thread.join() # End all threads

# Gets main page URLS from HLTV
class GetMainURLs(threading.Thread):
    def __init__(self, inputQ, outputQ):
        threading.Thread.__init__(self)
        self.inputQ = inputQ
        self.outputQ = outputQ

    def run(self):
        while self.inputQ.qsize() > 0:
            if self.inputQ.qsize() % 25 == 0:
                print(str(self.inputQ.qsize()) + " URLs left")
            url = self.inputQ.get() # Gets URL from inputQ
            html = CookSoup(url) # Gets HTML from URL
            self.outputQ.put(html) # Puts HTML in queue for parsing
            self.inputQ.task_done()

# Parses main page match info (URL, ID, and date) 
class ParseMainURLs(threading.Thread):
    def __init__(self, inputQ, outputQ):
        threading.Thread.__init__(self)
        self.inputQ = inputQ
        self.outputQ = outputQ
        
        self.matchAttr = {'class':'covSmallHeadline'}

    def run(self):
        while self.inputQ.qsize() > 0:
            if self.inputQ.qsize() % 25 == 0:
                print(str(self.inputQ.qsize()) + " pages left")
            html = self.inputQ.get()
            matches = html.findAll('a', 
                    href=re.compile('/\?pageid=188&matchid='))
            matchInfo = html.findAll('div', attrs=self.matchAttr)

            # Get info for every match on page
            for ii in range(len(matches)):
                rawdate = matchInfo[6 + ii*5].text
                date = datetime.strptime(rawdate, 
                        '%d/%m %y').strftime('%y.%m.%d')

                # Match info to pass to get queue
                info = ['http://www.hltv.org' + matches[ii]['href'],
                        int(re.sub('\/\?pageid=188&matchid=', '',
                            matches[ii]['href'])),
                        date]
                        
                self.outputQ.put(info)
            self.inputQ.task_done()

# Get actual HTML, start to fill data dictionary
#class GetHTML(multiprocessing.Process):
#    def __init__(self, inputQ, outputQ):
#        multiprocessing.Process.__init__(self)
#        self.inputQ = inputQ
#        self.outputQ = outputQ
#        self.data = df_base.copy()
#
#    def run(self):
#        while True:
#            for key in self.data.keys(): self.data[key] = None
#            info = self.inputQ.get()
#            if info == "die": break
#            self.data['id'] = info[1]
#            self.data['date'] = info[2]
#            uncookedHTML = CookSoup(info[0])
#            encodedHTML = uncookedHTML.encode('utf-8')
#            self.outputQ.put([self.data, encodedHTML])
#            self.inputQ.task_done()

class GetHTML(threading.Thread):
    def __init__(self, inputQ, outputQ):
        threading.Thread.__init__(self)
        self.inputQ = inputQ
        self.outputQ = outputQ
        self.data = df_base.copy()

    def run(self):
        while True:
            for key in self.data.keys(): self.data[key] = None
            info = self.inputQ.get()
            if info == "die": break
            url = info[0]
            uncookedHTML = BakeSoup(url)
            self.data['id'] = info[1]
            self.data['date'] = info[2]
            #encodedHTML = uncookedHTML.encode('utf-8')
            self.outputQ.put([self.data.copy(), uncookedHTML, url])
            self.inputQ.task_done()

# Parse actual HTML, fill rest of data dictionary
class ParseHTML(multiprocessing.Process):
    def __init__(self, inputQ, outputQ):
        multiprocessing.Process.__init__(self)
        self.inputQ = inputQ
        self.outputQ = outputQ
        self.infoAttr = {'class':'covSmallHeadline', 'style':re.compile("font-weight:normal.*;float:left.*")}
        self.data = df_base.copy()
        
    def run(self):
        sDex = 8    # Score index location
        awpDex = 21 # Most AWP kills index location
        fDex = 24   # Most first kills index location
        pDex = 30   # Player start index location
        mDex = 2    # Map start index location
        eDex = 4    # Event start index location 
        rDex = 10   # Rating start index location

        #while self.inputQ.qsize() > 0:
        htmlInfo = "I live!"
        while True:
            #if self.inputQ.qsize() == 0: continue
            for key in self.data.keys(): self.data[key] = None
            info = self.inputQ.get()
            if info == "die": break
            self.data = info[0]
            matchHTML = BeautifulSoup(info[1])
            match = matchHTML.findAll('div', self.infoAttr)
            while match[pDex + 1].find('a') is None:
                print('Bad HTML. Refreshing...')
                matchHTML = CookSoup(info[2])
                match = matchHTML.findAll('div', self.infoAttr)

            for ii in range(len(match)):
                text = match[ii].text.__str__()
                if text == "Map": mDex = ii + 1
                elif text == "Event": eDex = ii + 1
                elif text == "Game score": sDex = ii + 1
                elif text == "Most AWP kills": awpDex = ii + 1
                elif text == "Most first kills": fDex = ii + 1
                elif text == "Rating": rDex = ii + 1
                elif text == '':
                    pDex == ii + 1
                    break

            try: self.data['map'] = match[mDex].text # Map
            except: pass
            try: self.data['event'] = match[eDex].text.strip() # Event
            except: pass
            # Get team names and ratings
            try:self.data['t1'] = match[rDex].text.strip()
            except: pass
            try:self.data['t1_rating'] = match[rDex + 1].text
            except: pass
            try:self.data['t2'] = match[rDex + 2].text.strip()
            except: pass
            try:self.data['t2_rating'] = match[rDex + 3].text
            except: pass

            # Clean up scores
            try: scores = match[sDex].text.split()
            except: pass
            try: self.data['t1_score'] = scores[0].split(':')[0]
            except: pass
            try: self.data['t2_score'] = scores[0].split(':')[1]
            except: pass
            try: self.data['t1_ct'] = scores[1].split(':')[0].strip('(')
            except: pass
            try: self.data['t2_t'] = scores[1].split(':')[1].strip(')')
            except: pass
            try: self.data['t1_t'] = scores[2].split(':')[0].strip('(')
            except: pass
            try: self.data['t2_ct'] = scores[2].split(':')[1].strip(')')
            except: pass
            
            # Misc
            try: self.data['most_awp_kills_name'] = match[awpDex].text
            except: pass
            try: self.data['most_awp_kills_score'] = match[awpDex + 1].text
            except: pass
            try: self.data['most_first_kills_name'] = match[fDex].text
            except: pass
            try: self.data['most_first_kills_score'] = match[fDex + 1].text
            except: pass

            # Sort players
            teams = [[], []]
            for ii in range((len(match) - pDex)/9): # First name
                if match[pDex + 1 + ii*9].find('a')['href'] ==\
                match[rDex].find('a')['href']:
                    newPlayer = []
                    for jj in range(9):
                        newPlayer.append(match[30 + ii*9 + jj].text)
                    teams[0].append(newPlayer)
                        
                elif match[pDex + 1 + ii*9].find('a')['href'] ==\
                match[rDex + 2].find('a')['href']:
                    newPlayer = []
                    for jj in range(9):
                        newPlayer.append(match[30 + ii*9 + jj].text)
                    teams[1].append(newPlayer)

            # Fill data field with player info
            for ii in range(2):
                for jj in range(len(teams[ii])):
                    entry = 't' + str(ii + 1) + 'p' + str(jj + 1)
                    try: player = teams[ii][jj]
                    except: pass

                    try: self.data[entry] = player[0]
                    except: pass
                    try: self.data[entry + '_k'] = player[2].split('(')[0]
                    except: pass
                    try: self.data[entry + '_hs'] = player[2].split('(')[1].strip(')')
                    except: pass
                    try: self.data[entry + '_a'] = player[3]
                    except: pass
                    try: self.data[entry + '_d'] = player[4]
                    except: pass
                    try: self.data[entry + '_kd'] = player[5] # No float
                    except: pass
                    try: self.data[entry + '_kdiff'] = player[6]
                    except: pass
                    try: self.data[entry + '_fkdiff'] = player[7]
                    except: pass
                    try: self.data[entry + '_rating'] = player[8] # No float
                    except: pass
            self.outputQ.put(self.data.copy())
            self.inputQ.task_done()

class WriteFile(threading.Thread):
    rowsWritten = 0

    def __init__(self, inputQ, writeFile):
        threading.Thread.__init__(self)
        self.inputQ = inputQ
        self.writeFile = writeFile

    def run(self):
        while True:
            if WriteFile.rowsWritten % 50 == 0: 
                print(str(WriteFile.rowsWritten/50) + " page(s) finished")
            data = self.inputQ.get()
            if data == "die": 
                self.inputQ.task_done()
                break
            try: self.writeFile.writerow(data)
            except Exception:
                print("Error")
                for key in data:
                    print(key + ": " + str(data[key]))

                traceback.print_exc()
            WriteFile.rowsWritten = WriteFile.rowsWritten + 1
            self.inputQ.task_done()
