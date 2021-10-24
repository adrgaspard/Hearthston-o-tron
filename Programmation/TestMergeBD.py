from datetime import datetime
from os import listdir
from os.path import join, isfile

from Data.DataSerializer import DataSerializer

bd1 = "Data/bdd1.sqlite"
bd2 = "Data/bdd2.sqlite"
bdres = "Data/bddRES.sqlite"

MULTIPLE_MERGES = True
MULTIPLE_MERGES_PATH = "Data/TO_MERGE/"
MULTIPLE_MERGES_BDRES = "Data/MERGED/bdd-" + str(datetime.now().minute) + str(datetime.now().second) + str(datetime.now().microsecond) + ".sqlite"

if MULTIPLE_MERGES:
    begin = datetime.now()
    list_to_merge = [f for f in listdir(MULTIPLE_MERGES_PATH) if isfile(join(MULTIPLE_MERGES_PATH, f))]
    if len(list_to_merge) >= 2:
        for i in range(0, len(list_to_merge), 2):
            DataSerializer.merge_bdd(MULTIPLE_MERGES_PATH + list_to_merge[i], MULTIPLE_MERGES_PATH + list_to_merge[i + 1], MULTIPLE_MERGES_PATH + "_MERGED_" + list_to_merge[i] + "___+___" + list_to_merge[i + 1])
    delta = datetime.now() - begin
    print("Temps : " + str(int(delta.seconds / 3600)) + "h " + str(int((delta.seconds / 60) % 60)) + "m " + str(delta.seconds % 60) + "." + str(delta.microseconds) + "s")


else:
    begin = datetime.now()
    DataSerializer.merge_bdd(bd1, bd2, bdres)
    delta = datetime.now() - begin
    print("Temps : " + str(int(delta.seconds / 3600)) + "h " + str(int((delta.seconds / 60) % 60)) + "m " + str(delta.seconds % 60) + "." + str(delta.microseconds) + "s")
