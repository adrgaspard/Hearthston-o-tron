from Player.Movement import Movement


class FaceMovement(Movement):

    def __init__(self, winrate: float, nb_try: int, attacker_attack: int, opponent_health: int):
        super().__init__(winrate, nb_try)
        self.attacker_attack = attacker_attack
        self.opponent_health = opponent_health

    def __eq__(self, other):
        return self.attacker_attack == other.attacker_attack and self.opponent_health == other.opponent_health
