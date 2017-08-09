import pandas as pd
import numpy as np
from itertools import product
import random

import argparse

class Simulation():
    def __init__(self, team0, team1, guess):
        self.team0 = team0
        self.team1 = team1
        self.guess = guess
        self.stats = pd.read_csv("Pokemon.csv").groupby('#').first()
        self.type_stats = pd.read_csv("Type_Stats.csv", index_col=0)

    def check_guess(self):
        team0_alive = self.stats.loc[self.team0,:].sort_values('Total')
        team1_alive = self.stats.loc[self.team1,:].sort_values('Total')
        team0_turn = team0_alive.loc[:,"Speed"].sum() > team1_alive.loc[:,"Speed"].sum()
        while not team0_alive.empty and not team1_alive.empty:
            if team0_turn:
                team0_alive, team1_alive = self.fight(team0_alive,team1_alive)
            else:
                team1_alive, team0_alive = self.fight(team1_alive,team0_alive)
            team0_turn = not team0_turn
        winner = team0_alive.empty
        return self.guess == winner


    def fight(self, attack_team, defend_team):
        defender_hp = defend_team.iloc[0]["HP"]
        attacker_attack = attack_team.iloc[0]["Attack"]
        defender_defense = defend_team.iloc[0]["Defense"]
        attack_types = [attack_team.iloc[0]["Type 1"],attack_team.iloc[0]["Type 2"]]
        defense_types = [defend_team.iloc[0]["Type 1"],defend_team.iloc[0]["Type 2"]]
        attack_types = [x for x in attack_types if str(x) != 'nan']
        defense_types = [x for x in defense_types if str(x) != 'nan']
        attack_modifier = []
        for i in product(attack_types, defense_types):
            attack_modifier.append(self.type_stats.loc[i])
        attack_modifier = np.prod(attack_modifier)

        if random.random() < 0.33:
            attacker_attack = attack_team.iloc[0]["Sp. Atk"]

        if random.random() <0.33:
            defender_defense = defend_team.iloc[0]["Sp. Def"]

        attack_pwr = attacker_attack*attack_modifier - defender_defense

        attack_pwr = max(1,attack_pwr)

        defender_hp = defender_hp - attack_pwr
        if defender_hp > 0:
            defend_team.iloc[0, defend_team.columns.get_loc('HP')] = defender_hp
        else:
            defend_team = defend_team.drop(defend_team.index[0])
        return attack_team, defend_team

    def run(self):
        return self.check_guess()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-t1','--team0', nargs='+', help='<Required> Set flag', required=True)
    parser.add_argument('-t2','--team1', nargs='+', help='<Required> Set flag', required=True)
    parser.add_argument('-g', '--guess', type=int)
    args = parser.parse_args()
    print(Simulation(list(map(int, args.team0)), list(map(int, args.team1)), args.guess).run())
