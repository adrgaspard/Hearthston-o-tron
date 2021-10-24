from datetime import datetime
from Graphics.ConsoleGame import ConsoleGame
from Utils.Configuration import Configuration
import random

VERBOSE = False
REGISTER_DB = True
RANDOM_NAME_DB = True
LOADING_GUI = True
PUTTY_UI = False

old_path = Configuration.DATABASE_PATH

try:
    print("Entrez le nombre de parties : ")
    numberOfGame = int(input())
except ValueError:
    numberOfGame = 1

if RANDOM_NAME_DB:
    Configuration.DATABASE_PATH = "Data/bdd" + str(random.randint(0, 1000000)) + "___" + str(numberOfGame) + ".sqlite"

print("Traitement de " + str(numberOfGame) + " partie(s)...")
begin = datetime.now()
consoleGame = ConsoleGame(VERBOSE, REGISTER_DB)
consoleGame.start_multiple_games(numberOfGame, LOADING_GUI, PUTTY_UI)
delta = datetime.now() - begin
if not PUTTY_UI:
    consoleGame.print_statistics()
print("Temps : " + str(int(delta.seconds / 3600)) + "h " + str(int((delta.seconds / 60) % 60)) + "m " + str(delta.seconds % 60) + "." + str(delta.microseconds) + "s")


Configuration.DATABASE_PATH = old_path

