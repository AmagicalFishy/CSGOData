dictKeyList = ['date', 'opponent', 'oppRank', 'map', 'teamScore',
        'oppScore','event']

class Team:
    def __init__(self, teamName, teamRank):
        self.name = teamName
        self.rank = teamRank
        self.recentGames = []

    def add_game(self):
        game = {key: None for key in dictKeyList}
        self.recentGames.append(game)

