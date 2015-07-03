#!/usr/bin/env python

import sys
import os
import tcmods #Team Compare Modules
from tcmods import thisDirectory

def main():
    if len(sys.argv) == 3:
        firstTeam = str(sys.argv[1])
        secondTeam = str(sys.argv[2])

    elif len(sys.argv) == 4:
        firstTeam = str(sys.argv[2])
        secondTeam = str(sys.argv[3])
        flags = list(sys.argv[1])

    print("Gathering recent match info. on the first team...")
    teamOneInfo = tcmods.teaminfo(firstTeam)
    print("\nGathering recent match info on the second team...")
    teamTwoInfo = tcmods.teaminfo(secondTeam)
    
    if 'w' in flags:
        print("\nCreating worksheet...")
        worksheetDir = thisDirectory + '/sheets/'
        worksheetName = tcmods.makesheet(
                teamOneInfo,
                teamTwoInfo,
                worksheetDir)
        openCommand = str('xdg-open ' + worksheetDir + worksheetName)
        os.system(openCommand)

    if 't' in flags:
        print("\nCreating Reddit table...")
        tableDir = thisDirectory + '/tables/'
        tableName = tcmods.maketable(
                teamOneInfo,
                teamTwoInfo,
                tableDir)
        openCommand = str('xdg-open ' + tableDir + tableName)
        os.system(openCommand)

if __name__ == "__main__":
    main()

