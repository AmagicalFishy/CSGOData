import xlwt
t1date  = 0
t1map   = 1
t1opp   = 2
t1score = 3
t1diff  = 4

t2diff  = 6
t2score = 7
t2opp   = 8
t2map   = 9
t2date  = 10

def makesheet(Team1, Team2, Directory):
    workbook = xlwt.Workbook()

    bnc = xlwt.easyxf('font: bold 1; align: horiz center')
    bgreen = xlwt.easyxf('pattern: pattern solid, fore_colour green;')
    bred = xlwt.easyxf('pattern: pattern solid, fore_colour red;')
    tgreen = xlwt.easyxf('font: colour green, bold True;')
    tred = xlwt.easyxf('font: colour red, bold True;')

    sheet = workbook.add_sheet("Team Comparison")

    sheet.write(0, 2, Team1.name, bnc) #Name of 1st team
    sheet.write(0, 3, Team1.rank, bnc) #Rank of 1st team

    sheet.write(0, 4, Team1.rank - Team2.rank, bnc) #Rank Difference

    sheet.write(0, 5, Team2.rank, bnc) #Rank of 2nd team
    sheet.write(0, 6, Team2.name, bnc) #Name of 2nd team

    row = 1
    for entry in Team1.recentGames:
        sheet.write(row, t1date, entry['date']) #Date match took place
        sheet.write(row, t1map, entry['map']) #Map of Team 1's Matches
        sheet.write(row, t1opp, entry['opponent']) #Opponent name
        #If win, color green. If lose, color red.
        if entry['teamScore'] > entry['oppScore']:
            sheet.write(row, t1score, str(entry['teamScore']) + "-" + 
                str(entry['oppScore']), bgreen)

        elif entry['teamScore'] < entry['oppScore']:
            sheet.write(row, t1score, str(entry['teamScore']) + "-" + 
                str(entry['oppScore']), bred)

        
        #If higher, color green. If lower, color red.
        rankDiff = Team1.rank - entry['oppRank']
        if rankDiff > 0:
            sheet.write(row, t1diff, rankDiff, tgreen)
        if rankDiff < 0:
            sheet.write(row, t1diff, rankDiff, tred)

        row = row + 1

    row = 1

    for entry in Team2.recentGames:
        sheet.write(row, t2date, entry['date'])
        sheet.write(row, t2map, entry['map'])
        sheet.write(row, t2opp, entry['opponent'])

        #If win, color green. If lose, color red.
        if entry['teamScore'] > entry['oppScore']:
            sheet.write(row, t2score, str(entry['teamScore']) + "-" + 
                str(entry['oppScore']), bgreen)
        elif entry['teamScore'] < entry['oppScore']:
            sheet.write(row, t2score, str(entry['teamScore']) + "-" + 
                str(entry['oppScore']), bred)

        
        #If higher, color green. If lower, color red.
        rankDiff = Team2.rank - entry['oppRank']
        if rankDiff > 0:
            sheet.write(row, t2diff, rankDiff, tgreen)
        if rankDiff < 0:
            sheet.write(row, t2diff, rankDiff, tred)

        row = row + 1
    sheetName = Team1.name + "-" + Team2.name + ".xls"
    sheetName = sheetName.replace(" ", "")
    workbook.save(Directory + sheetName)

    return sheetName
