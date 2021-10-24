import sqlite3
from sqlite3 import Cursor
from Player.FaceMovement import FaceMovement
from Player.TradeMovement import TradeMovement
from Utils.Configuration import Configuration


class DataCollector:
    class __Singleton:

        def __init__(self):
            self.trade_movements: [TradeMovement] = []
            self.face_movements: [FaceMovement] = []
            self.connection = sqlite3.connect(Configuration.DATABASE_PATH)
            print(self.connection)
            if self.connection is not None:
                self.statement: Cursor = self.connection.cursor()
            else:
                self.statement: Cursor = None
            result = self.statement.execute("SELECT * FROM trademove").fetchall()
            for i in range(len(result)):
                self.trade_movements.append(TradeMovement(result[i][6], result[i][7], result[i][0], result[i][1], result[i][2], result[i][3], result[i][4], result[i][5]))
            print(str(len(self.trade_movements)) + " mouvement(s) désensif(s) chargé(s).")
            result = self.statement.execute("SELECT * FROM facemove").fetchall()
            for i in range(len(result)):
                self.face_movements.append(FaceMovement(result[i][2], result[i][3], result[i][0], result[i][1]))
            print(str(len(self.face_movements)) + " mouvement(s) offensif(s) chargé(s).")

    __instance: __Singleton = None

    def __init__(self):
        if not DataCollector.__instance:
            DataCollector.__instance = DataCollector.__Singleton()

    def get_face_movements(self) -> [FaceMovement]:
        return self.__instance.face_movements

    def get_trade_movements(self) -> [TradeMovement]:
        return self.__instance.trade_movements

    def get_winrate_trade_movement(self, attacker_attack: int, attacker_health: int, attacker_effects: int, opponent_attack: int, opponent_health: int, opponent_effects: int) -> float:
        for trade_move in self.get_trade_movements():
            if trade_move.attacker_attack == attacker_attack and trade_move.attacker_health == attacker_health and trade_move.attacker_effects == attacker_effects and trade_move.opponent_attack == opponent_attack and trade_move.opponent_health == opponent_health and trade_move.opponent_effects == opponent_effects:
                return trade_move.winrate
        return -1

    def get_winrate_face_movement(self, attacker_attack: int, opponent_health: int) -> float:
        for face_move in self.get_face_movements():
            if face_move.attacker_attack == attacker_attack and face_move.opponent_health == opponent_health:
                return face_move.winrate
        return -1
