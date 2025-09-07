from re import search
from sys import stdin




teams = {}

for line in stdin:
    if m := search(r'"(?P<team1>.+)" \- "(?P<team2>.+)" (?P<g1>\d+):(?P<g2>\d+)', line):
        team1 = m['team1']
        team2 = m['team2']
        g1 = int(m['g1'])
        g2 = int(m['g2'])
        if team1 not in teams:
            teams[team1] = {'games': 1, 'all_goals': g1, 'players' : {}}
        else:
            teams[team1]['games'] += 1
            teams[team1]['all_goals'] += g1

        if team2 not in teams:
            teams[team2] = {'games': 1, 'all_goals': g2, 'players' : {}}
        else:
            teams[team2]['games'] += 1
            teams[team2]['all_goals'] += g2
        open_goal = ["Some", 95]
        for i in range(g1):
            line = input()
            if m:= search("(?P<player>.+) (?P<m>\d+)'", line):
                player = m['player']
                minute = int(m['m'])
                if player in teams[team1]['players']:
                    teams[team1]['players'][player]['goals'].append(minute)
                else:
                    teams[team1]['players'][player] = {'goals' : [minute], 'open_goal' :0}
                if i == 0:
                    open_goal[0] = player
                    open_goal[1] = minute
            else:
                print("Not found goal!!!")
        if g2 == 0 and open_goal[1] != 95:
            teams[team1]['players'][open_goal[0]]['open_goal'] += 1
        for i in range(g2):
            line = input()
            if m:= search("(?P<player>.+) (?P<m>\d+)'", line):
                player = m['player']
                minute = int(m['m'])
                if player in teams[team2]['players']:
                    teams[team2]['players'][player]['goals'].append(minute)
                else:
                    teams[team2]['players'][player] = {'goals' : [minute], 'open_goal' :0}
                if i == 0:
                    if minute<open_goal[1]:
                        teams[team2]['players'][player]['open_goal'] += 1
                    else:
                        teams[team1]['players'][open_goal[0]]['open_goal'] += 1
            else:
                print("Not found goal!!!")

    elif m := search(r'Total goals for "(?P<team>.+)"', line):
        team = m['team']
        if team not in teams:
            print(0)
        else:
            print(teams[team]['all_goals'])

    elif m := search(r'Mean goals per game for "(?P<team>.+)"', line):
        team = m['team']
        if team not in teams:
            print(0)
        else:
            print(teams[team]['all_goals'] / teams[team]['games'])

    elif m := search(r'Total goals by (?P<player>.+)', line):
        player = m['player']
        for team in teams.values():
            if player in team['players']:
                print(len(team['players'][player]['goals']))
                break
        else:
            print(0)

    elif m := search(r'Mean goals per game by (?P<player>.+)', line):
        player = m['player']
        for team in teams.values():
            if player in team['players']:
                print(len(team['players'][player]['goals']) / team['games'])
                break
        else:
            print(0)

    elif m:=search(r'Goals on minute (?P<m>\d+) by (?P<player>.+)', line):
        minute = int(m['m'])
        player = m['player']
        res = 0
        for team in teams.values():
            if player in team['players']:
                for minute_ in team['players'][player]['goals']:
                    if minute == minute_:
                        res +=1
        print(res)

    elif m:=search(r'Goals on first (?P<m>\d+) minutes by (?P<player>.+)', line):
        minute = int(m['m'])
        player = m['player']
        res = 0
        for team in teams.values():
            if player in team['players']:
                for minute_ in team['players'][player]['goals']:
                    if minute_ <= minute:
                        res +=1
        print(res)

    elif m:=search(r'Goals on last (?P<m>\d+) minutes by (?P<player>.+)', line):
        minute = int(m['m'])

        player = m['player']
        res = 0
        for team in teams.values():
            if player in team['players']:
                for minute_ in team['players'][player]['goals']:
                    if minute_ >= 91-minute and minute_ <= 90:
                        res +=1
                break
        print(res)

    elif m:=search(r'Score opens by "(?P<team>.+)"', line):
        team = m['team']
        res = 0
        if team in teams:
            for player in  teams[team]['players'].values():
                res += player['open_goal']
        print(res)

    elif m:=search(r'Score opens by (?P<player>.+)', line):
        player = m['player']
        res = 0
        for team in  teams.values():
            if player in team['players']:
                print(team['players'][player]['open_goal'])
                break
        else:
            print(0)
    else:
        pass










