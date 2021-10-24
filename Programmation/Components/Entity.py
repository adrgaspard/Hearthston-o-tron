from abc import abstractmethod


class Entity():

    def __init__(self, max_health: int, health: int, attack: int, image_location: str):
        self.max_health: int = max_health
        self.health: int = health
        self.attack: int = attack
        self.image_location: str = image_location

    @abstractmethod
    def take_damage(self, damage: int, is_toxic: bool):
        pass

    @abstractmethod
    def die(self):
        pass

    @abstractmethod
    def can_attack_opponent(self) -> bool:
        pass

    @abstractmethod
    def can_attack_minion(self, minion_id: int) -> bool:
        pass

    @abstractmethod
    def attack_opponent(self):
        pass

    @abstractmethod
    def attack_minion(self, minion_id: int):
        pass

    @abstractmethod
    def die(self):
        pass
