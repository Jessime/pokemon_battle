import pandas as pd

class Simulation():
    def __init__(self, team1, team2, guess):
        self.team1 = team1
        self.team2 = team2
        self.guess = guess
        self.stats = pd.read_csv("Pokemon.csv").groupby('#').first()

    def check_guess(self):
        team1_alive = self.stats.loc[self.team1,:].sort_values('Total')
        team2_alive = self.stats.loc[self.team2,:].sort_values('Total')
        team1_turn = team1_alive.loc[:,"Speed"].sum() > team2_alive.loc[:,"Speed"].sum()
        while not team1_alive.empty and not team2_alive.empty:
            if team1_turn:
                team1_alive, team2_alive = self.fight(team1_alive,team2_alive)
            else:
                team2_alive, team1_alive = self.fight(team2_alive,team1_alive)
            team1_turn = not team1_turn
        if team1_alive.empty:
            winner = 2
        else:
            winner = 1
        return self.guess == winner


    def fight(self, attack_team, defend_team):
        defender_hp = defend_team.iloc[0]["HP"]
        attack_pwr = attack_team.iloc[0]["Attack"] - defend_team.iloc[0]["Defense"]

        attack_pwr = max(1,attack_pwr)

        defender_hp = defender_hp - attack_pwr
        if defender_hp > 0:
            defend_team.iloc[0, defend_team.columns.get_loc('HP')] = defender_hp
        else:
            defend_team = defend_team.drop(defend_team.index[0])
        return attack_team, defend_team

    def run(self):
        return self.check_guess() 
