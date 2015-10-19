def writetable(table, team):
    table.write("**" + team.name + "** Rank: " + str(team.rank) + '\n\n')
    table.write('Date|Event|Map|Score|Opponent|Rank Difference|W/L')
    table.write('\n')
    table.write(':-- | :-: | :-: | :-: | :-: | :-: | :-: \n')
    for entry in team.recentGames:
        rankDiff = team.rank - entry['oppRank']
        table.write(entry['date'] + '|' + entry['event'] + '|' + entry['map'] + '|'
        + str(entry['teamScore']) + '-' + str(entry['oppScore']) + '|'
        + entry['opponent'] + '|' + str(rankDiff) + '|')
        if entry['teamScore'] > entry['oppScore']:
            table.write('Win\n')
        elif entry['teamScore'] < entry['oppScore']:
            table.write('Lose\n')
        else:
            table.write('Tie\n')

    table.write('\n\n &nbsp; \n\n')

def maketable(Team1, Team2, Directory):
    tableName = Team1.name + "-" + Team2.name + '.txt'
    tableName = tableName.replace(" ", "")
    table = open(Directory + tableName, 'w+')

    writetable(table, Team1)
    writetable(table, Team2)

    table.write("If I've missed any games, feel free to PM me with "
    "any requests. (If you don't mind, include the Reddit URL, too.) If you "
    "want to ask me for betting advice, you probably shouldn't. My advice sucks."
    "\n\n&nbsp;\n\n"
    "^(Ranks are those used by GosuGamers. Be weary; I've been told they're bad "
    "(I'm working on adding average-player ranks from HLTV, but that will "
    "take a while; for now, GosuGamers ranking will have to do.))"
    "\n\n")

    table.write("http://steamcommunity.com/profiles/76561198011946609/")
    
    table.close()
    return tableName

#Debugging
if __name__ == "__main__":
    from containers import Team

