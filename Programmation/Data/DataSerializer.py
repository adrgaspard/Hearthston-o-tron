import sqlite3
from sqlite3 import Cursor

import numpy

from Definitions.MinionCardDefinition import MinionCardEffectTypes
from Player.FaceMovement import FaceMovement
from Player.TradeMovement import TradeMovement
from Utils.Configuration import Configuration
from Utils.Utils import Utils


class DataSerializer:

    def __init__(self):
        try:
            self.connection = sqlite3.connect(Configuration.DATABASE_PATH)
            print(self.connection)
        except AttributeError:
            print('Can\'t find ' + Configuration.DATABASE_PATH)
        if self.connection is not None:
            self.statement: Cursor = self.connection.cursor()
            self.setup()
        else:
            self.statement: Cursor = None

    def setup(self):
        query = [
            """CREATE TABLE IF NOT EXISTS trademove (
            attacker_attack INTEGER NOT NULL,
            attacker_health INTEGER NOT NULL,
            attacker_effects INTEGER NOT NULL,
            opponent_attack INTEGER NOT NULL,
            opponent_health INTEGER NOT NULL,
            opponent_effects INTEGER NOT NULL,
            winrate REAL NOT NULL,
            nbTry INTEGER NOT NULL
            );"""
            ,
            """CREATE TABLE IF NOT EXISTS facemove (
            attacker_attack INTEGER NOT NULL,
            opponent_health INTEGER NOT NULL,
            winrate REAL NOT NULL,
            nbTry INTEGER NOT NULL
            );"""
            ,
            """CREATE TABLE IF NOT EXISTS firstQueueTrademove (
           attacker_attack INTEGER NOT NULL,
           attacker_health INTEGER NOT NULL,
           attacker_effects INTEGER NOT NULL,
           opponent_attack INTEGER NOT NULL,
           opponent_health INTEGER NOT NULL,
           opponent_effects INTEGER NOT NULL,
           isWin INTEGER
           );"""
            ,
            """CREATE TABLE IF NOT EXISTS secondQueueTrademove (
            attacker_attack INTEGER NOT NULL,
            attacker_health INTEGER NOT NULL,
            attacker_effects INTEGER NOT NULL,
            opponent_attack INTEGER NOT NULL,
            opponent_health INTEGER NOT NULL,
            opponent_effects INTEGER NOT NULL,
            isWin INTEGER
            );"""
            ,
            """CREATE TABLE IF NOT EXISTS firstQueueFacemove (
            attacker_attack INTEGER NOT NULL,
            opponent_health INTEGER NOT NULL,
            isWin INTEGER
            );"""
            ,
            """CREATE TABLE IF NOT EXISTS secondQueueFacemove (
            attacker_attack INTEGER NOT NULL,
            opponent_health INTEGER NOT NULL,
            isWin INTEGER
            );"""]
        for i in range(0, 6):
            self.statement.execute(query[i])

    def commit(self):
        self.connection.commit()

    def addTradeMoveInQueue(self, numQueue: int, attacker_attack: int, attacker_health: int, attacker_effects: int, opponent_attack: int, opponent_health: int, opponent_effects: int):
        attacker_effects = int(Utils.polish_minion_effect_type(attacker_effects))
        opponent_effects = int(Utils.polish_minion_effect_type(opponent_effects))
        if numQueue == 0:
            query = "INSERT INTO firstQueueTrademove VALUES ('" + str(attacker_attack) + "', '" + str(attacker_health) + "', '" + str(attacker_effects) + "', '" + str(opponent_attack) + "', '" + str(opponent_health) + "', '" + str(opponent_effects) + "', NULL);"
        else:
            query = "INSERT INTO secondQueueTrademove VALUES ('" + str(attacker_attack) + "', '" + str(attacker_health) + "', '" + str(attacker_effects) + "', '" + str(opponent_attack) + "', '" + str(opponent_health) + "', '" + str(opponent_effects) + "', NULL);"
        self.statement.execute(query)

    def addFaceMoveInQueue(self, numQueue: int, attacker_attack: int, opponent_health: int):
        if numQueue == 0:
            query = "INSERT INTO firstQueueFacemove VALUES ('" + str(attacker_attack) + "', '" + str(opponent_health) + "', NULL);"
        else:
            query = "INSERT INTO secondQueueFacemove VALUES ('" + str(attacker_attack) + "', '" + str(opponent_health) + "', NULL);"
        self.statement.execute(query)

    def flushQueues(self, winningQueue: int):
        if winningQueue == 0:
            query = [
                "UPDATE firstQueueTrademove SET isWin = 1;",
                "UPDATE secondQueueTrademove SET isWin = 0;",
                "UPDATE firstQueueFacemove SET isWin = 1;",
                "UPDATE secondQueueFacemove SET isWin = 0;"]
        else:
            query = [
                "UPDATE firstQueueTrademove SET isWin = 0;",
                "UPDATE secondQueueTrademove SET isWin = 1;",
                "UPDATE firstQueueFacemove SET isWin = 0;",
                "UPDATE secondQueueFacemove SET isWin = 1;"]

        for i in range(0, 4):
            self.statement.execute(query[i])

        self.statement.execute("SELECT * FROM firstQueueTrademove;")
        for row in self.statement.fetchall():
            self.addTradeMove(row)

        self.statement.execute("SELECT * FROM secondQueueTrademove;")
        for row in self.statement.fetchall():
            self.addTradeMove(row)

        self.statement.execute("SELECT * FROM firstQueueFacemove;")
        for row in self.statement.fetchall():
            self.addFaceMove(row)

        self.statement.execute("SELECT * FROM secondQueueFacemove;")
        for row in self.statement.fetchall():
            self.addFaceMove(row)

        self.statement.execute("DELETE FROM firstQueueTrademove;")
        self.statement.execute("DELETE FROM secondQueueTrademove;")
        self.statement.execute("DELETE FROM firstQueueFacemove;")
        self.statement.execute("DELETE FROM secondQueueFacemove;")
        self.commit()

    def addTradeMove(self, row):
        is_win = row[6]
        count = self.statement.execute("SELECT count(*) FROM trademove WHERE attacker_attack=:aa AND attacker_health=:ah AND attacker_effects=:ae AND opponent_attack=:oa AND opponent_health=:oh AND opponent_effects=:oe", {"aa": row[0], "ah": row[1], "ae": row[2], "oa": row[3], "oh": row[4], "oe": row[5]})

        cpt = count.fetchall()[0][0]
        if cpt == 0:
            self.statement.execute("INSERT INTO trademove VALUES(" + str(row[0]) + ", " + str(row[1]) + ", " + str(row[2]) + ", " + str(row[3]) + ", " + str(row[4]) + ", " + str(row[5]) + ", " + str(is_win) + ", 1);")
        else:
            for i in range(cpt):
                move_founds = self.statement.execute("SELECT * FROM trademove WHERE attacker_attack=:aa AND attacker_health=:ah AND attacker_effects=:ae AND opponent_attack=:oa AND opponent_health=:oh AND opponent_effects=:oe", {"aa": row[0], "ah": row[1], "ae": row[2], "oa": row[3], "oh": row[4], "oe": row[5]})
                result = move_founds.fetchone()
                winrate = result[6]
                nb_try = result[7]
                new_nb_try = nb_try + 1
                new_winrate = (winrate * nb_try + is_win) / new_nb_try
                self.statement.execute("UPDATE trademove SET winrate=:new_winrate, nbTry=:new_nb_try WHERE attacker_attack=:aa AND attacker_health=:ah AND attacker_effects=:ae AND opponent_attack=:oa AND opponent_health=:oh AND opponent_effects=:oe", {"new_winrate": new_winrate, "new_nb_try": new_nb_try, "aa": row[0], "ah": row[1], "ae": row[2], "oa": row[3], "oh": row[4], "oe": row[5]})

    def addFaceMove(self, row):
        is_win = row[2]
        count = self.statement.execute("SELECT count(*) FROM facemove WHERE attacker_attack=:aa AND opponent_health=:oh", {"aa": row[0], "oh": row[1]})
        cpt = count.fetchall()[0][0]
        if cpt == 0:
            self.statement.execute("INSERT INTO facemove VALUES(" + str(row[0]) + ", " + str(row[1]) + ", " + str(is_win) + ", 1);")

        else:
            for i in range(cpt):
                move_founds = self.statement.execute("SELECT * FROM facemove WHERE attacker_attack=:aa AND opponent_health=:oh", {"aa": row[0], "oh": row[1]})
                result = move_founds.fetchone()
                winrate = result[2]
                nb_try = result[3]
                new_nb_try = nb_try + 1
                new_winrate = (winrate * nb_try + is_win) / new_nb_try
                self.statement.execute("UPDATE facemove SET winrate=:new_winrate, nbTry=:new_nb_try WHERE attacker_attack=:aa AND opponent_health=:oh", {"new_winrate": new_winrate, "new_nb_try": new_nb_try, "aa": row[0], "oh": row[1]})

    def __del__(self):
        self.connection.close()

    @staticmethod
    def merge_bdd(bdd1, bdd2, resultBDD):
        connection1 = sqlite3.connect(bdd1)
        print(connection1)
        if connection1 is not None:
            statement1: Cursor = connection1.cursor()
        else:
            statement1: Cursor = None

        connection2 = sqlite3.connect(bdd2)
        print(connection2)
        if connection2 is not None:
            statement2: Cursor = connection2.cursor()
        else:
            statement2: Cursor = None

        connection3 = sqlite3.connect(resultBDD)
        print(connection3)
        if connection3 is not None:
            statement3: Cursor = connection3.cursor()
        else:
            statement3: Cursor = None

        query = [
            """CREATE TABLE IF NOT EXISTS trademove (
            attacker_attack INTEGER NOT NULL,
            attacker_health INTEGER NOT NULL,
            attacker_effects INTEGER NOT NULL,
            opponent_attack INTEGER NOT NULL,
            opponent_health INTEGER NOT NULL,
            opponent_effects INTEGER NOT NULL,
            winrate REAL NOT NULL,
            nbTry INTEGER NOT NULL
            );"""
            ,
            """CREATE TABLE IF NOT EXISTS facemove (
            attacker_attack INTEGER NOT NULL,
            opponent_health INTEGER NOT NULL,
            winrate REAL NOT NULL,
            nbTry INTEGER NOT NULL
            );"""]
        for i in range(0, 2):
            statement3.execute(query[i])

        #
        #
        #
        #
        #
        # Face Move

        facemove_array1 = []
        facemoves1 = statement1.execute("SELECT * FROM facemove").fetchall()

        for facemove1 in facemoves1:
            facemove_array1.append(FaceMovement(facemove1[2], facemove1[3], facemove1[0], facemove1[1]))
        print('Nb facemoves BD 1 ' + str(len(facemove_array1)))

        facemove_array2 = []
        facemoves2 = statement2.execute("SELECT * FROM facemove").fetchall()
        for facemove2 in facemoves2:
            facemove_array2.append(FaceMovement(facemove2[2], facemove2[3], facemove2[0], facemove2[1]))
        print('Nb facemoves BD 2 ' + str(len(facemove_array2)))

        for facemove1 in facemove_array1:
            statement3.execute("INSERT INTO facemove VALUES(" + str(facemove1.attacker_attack) + ", " + str(facemove1.opponent_health) + ", " + str(facemove1.winrate) + ", " + str(facemove1.nb_try) + ");")

        for facemove2 in facemove_array2:
            if facemove_array1.__contains__(facemove2):
                similar_move = facemove_array1[facemove_array1.index(facemove2)]
                new_nb_try = similar_move.nb_try + facemove2.nb_try
                new_win_rate = (facemove2.winrate * facemove2.nb_try + similar_move.winrate * similar_move.nb_try) / new_nb_try
                statement3.execute("UPDATE facemove SET winrate=:new_winrate, nbTry=:new_nb_try WHERE attacker_attack=:aa AND opponent_health=:oh", {"new_winrate": new_win_rate, "new_nb_try": new_nb_try, "aa": facemove2.attacker_attack, "oh": facemove2.opponent_health})
            else:
                statement3.execute("INSERT INTO facemove VALUES(" + str(facemove2.attacker_attack) + ", " + str(facemove2.opponent_health) + ", " + str(facemove2.winrate) + ", " + str(facemove2.nb_try) + ");")
        connection3.commit()

        #
        #
        #
        #
        #
        # Trade Move

        trademove_array1 = []
        trademoves1 = statement1.execute("SELECT * FROM trademove").fetchall()
        for trademove1 in trademoves1:
            trademove_array1.append(TradeMovement(trademove1[6], trademove1[7], trademove1[0], trademove1[1], trademove1[2], trademove1[3], trademove1[4], trademove1[5]))
        print('Nb trademove BD 1 ' + str(len(trademove_array1)))

        trademove_array2 = []
        trademoves2 = statement2.execute("SELECT * FROM trademove").fetchall()
        for trademove2 in trademoves2:
            trademove_array2.append(TradeMovement(trademove2[6], trademove2[7], trademove2[0], trademove2[1], trademove2[2], trademove2[3], trademove2[4], trademove2[5]))
        print('Nb trademove BD 2 ' + str(len(trademove_array2)))

        for trademove1 in trademove_array1:
            statement3.execute("INSERT INTO trademove VALUES(" + str(trademove1.attacker_attack) + ", " + str(trademove1.attacker_health) + ", " + str(trademove1.attacker_effects) + ", " + str(trademove1.opponent_attack) + ", " + str(trademove1.opponent_health) + ", " + str(trademove1.opponent_effects) + ", " + str(trademove1.winrate) + ", " + str(trademove1.nb_try) + ");")

        for trademove2 in trademove_array2:
            if trademove_array1.__contains__(trademove2):
                similar_move = trademove_array1[trademove_array1.index(trademove2)]
                new_nb_try = similar_move.nb_try + trademove2.nb_try
                new_win_rate = (trademove2.winrate * trademove2.nb_try + similar_move.winrate * similar_move.nb_try) / new_nb_try
                statement3.execute("UPDATE trademove SET winrate=:new_winrate, nbTry=:new_nb_try WHERE attacker_attack=:aa AND attacker_health=:ah AND attacker_effects=:ae AND opponent_attack=:oa AND opponent_health=:oh AND opponent_effects=:oe", {"new_winrate": new_win_rate, "new_nb_try": new_nb_try, "aa": trademove2.attacker_attack, "ah": trademove2.attacker_health, "ae": trademove2.attacker_effects, "oa": trademove2.opponent_attack, "oh": trademove2.opponent_health, "oe": trademove2.opponent_effects})
            else:
                statement3.execute("INSERT INTO trademove VALUES(" + str(trademove2.attacker_attack) + ", " + str(trademove2.attacker_health) + ", " + str(trademove2.attacker_effects) + ", " + str(trademove2.opponent_attack) + ", " + str(trademove2.opponent_health) + ", " + str(trademove2.opponent_effects) + ", " + str(trademove2.winrate) + ", " + str(trademove2.nb_try) + ");")

        connection3.commit()

        print('Done !')

    @staticmethod
    def sanitize_bdd(bdd):
        connection = sqlite3.connect(bdd)
        print(connection)
        if connection is not None:
            statement: Cursor = connection.cursor()
        else:
            statement: Cursor = None
        queries = ['CREATE TABLE IF NOT EXISTS facemoveREAL (attacker_attack INTEGER NOT NULL,opponent_health INTEGER NOT NULL,winrate REAL NOT NULL,nbTry INTEGER NOT NULL);',
                   'INSERT INTO facemoveREAL (attacker_attack,opponent_health,winrate,nbTry) SELECT DISTINCT attacker_attack, opponent_health, winrate, nbTry FROM facemove;',
                   'DELETE FROM facemove;',
                   'INSERT INTO facemove (attacker_attack,opponent_health,winrate,nbTry) SELECT DISTINCT attacker_attack, opponent_health, winrate, nbTry FROM facemoveREAL;',
                   'DROP TABLE facemoveREAL;',
                   'CREATE TABLE IF NOT EXISTS trademoveREAL (attacker_attack INTEGER NOT NULL,attacker_health INTEGER NOT NULL,attacker_effects INTEGER NOT NULL,opponent_attack INTEGER NOT NULL,opponent_health INTEGER NOT NULL,opponent_effects INTEGER NOT NULL,winrate REAL NOT NULL,nbTry INTEGER NOT NULL);',
                   'INSERT INTO trademoveREAL (attacker_attack,attacker_health,attacker_effects,opponent_attack,opponent_health,opponent_effects,winrate,nbTry) select DISTINCT attacker_attack,attacker_health,attacker_effects,opponent_attack,opponent_health,opponent_effects,winrate,nbTry FROM trademove;',
                   'DELETE FROM trademove;',
                   'INSERT INTO trademove (attacker_attack,attacker_health,attacker_effects,opponent_attack,opponent_health,opponent_effects,winrate,nbTry) select DISTINCT attacker_attack,attacker_health,attacker_effects,opponent_attack,opponent_health,opponent_effects,winrate,nbTry FROM trademoveREAL;',
                   'DROP TABLE trademoveREAL;']

        for i in range(0, len(queries)):
            statement.execute(queries[i])
