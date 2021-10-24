from Player.Movement import Movement
from Utils.Utils import Utils


class TradeMovement(Movement):

    def __init__(self, winrate: float, nb_try: int, attacker_attack: int, attacker_health: int, attacker_effects: int,
                 opponent_attack: int, opponent_health: int, opponent_effects: int):
        super().__init__(winrate, nb_try)
        self.attacker_attack = attacker_attack
        self.attacker_health = attacker_health
        self.attacker_effects = int(Utils.polish_minion_effect_type(attacker_effects))
        self.opponent_attack = opponent_attack
        self.opponent_health = opponent_health
        self.opponent_effects = int(Utils.polish_minion_effect_type(attacker_effects))

    def __eq__(self, other):
        return self.attacker_attack == other.attacker_attack and self.attacker_health == other.attacker_health and self.attacker_effects == other.attacker_effects and self.opponent_attack == other.opponent_attack and self.opponent_health == other.opponent_health and self.opponent_effects == other.opponent_effects
