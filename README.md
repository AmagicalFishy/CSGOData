# CSGOData
<<<<<<< HEAD
This doesn't tell you who to bet on. It just aggregates data for the 
recent-matches of two teams. All data's taken from GosuGamers.net.

You need BeautifulSoup (to parse the HTML), urllib2 (to fetch the 
HTML/J-script generated HTML), and xlwt (to write an Excel file) 
installed in python. 

chmod -x main.py and run it with a couple of arguments.

There are two flags:
t - output and open a text file w/ all the data formatted so you can 
paste it into Reddit (I did it on the CS:GO betting forums for every 
game; people came)
w - output and open an excel spreadsheet w/ the data.

Unless you plan to go on Reddit at all, just use w. 

The other two arguments are the GosuGamers ID of the teams you want to 
compare. Say you want to get data from fnatic and Virtuous Pro. Their 
GosuGamer URLs are 
http://www.gosugamers.net/counterstrike/teams/7386-fnatic and 
http://www.gosugamers.net/counterstrike/teams/7455-virtus-pro-cs 
respectively. You just want to use the last clause of their URLs in the 
arguments.

So, for example: 

./main.py w 7455-virtus-pro-cs 7386-fnatic 

... will start the program, collect data, and open up an Excel sheet.

One might have to add a time.sleep(3) statement to the last for loop in 
teaminfo.py
=======
Crawler that fetches data of recent CS:GO matches
>>>>>>> 2256b17475ca3d86b83fe594e9e104ae637e831a
