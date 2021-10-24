import pandas as pd

from Data.ActionDictionary import ActionDictionary
from Definitions.Action import Action
from Definitions.CardDefinition import CardDefinition
from Definitions.MinionCardDefinition import MinionCardDefinition
from Definitions.SpellCardDefinition import SpellCardDefinition
from Definitions.WeaponCardDefinition import WeaponCardDefinition
from Utils.Configuration import Configuration


class CardDictionary:
    class __Singleton:

        def __init__(self):
            self.card_definitions: [MinionCardDefinition] = []

            try:
                database = pd.read_csv(Configuration.CARD_DEFINITIONS_PATH, sep=Configuration.CSV_SEPARATOR)
            except FileNotFoundError:
                print("Erreur > Fichier non trouvé.")
                return

            action_dictionary: ActionDictionary = ActionDictionary()
            for i in range(len(database)):
                if database.iloc[i]["Pattern"] == 0:  # Est une définition d'un serviteur.
                    self.card_definitions.append(MinionCardDefinition(database.iloc[i]["Id"], database.iloc[i]["Name"],
                                                                      "",  # database.iloc[i]["Description"]
                                                                      database.iloc[i]["Rarity"],
                                                                      database.iloc[i]["Cost"],
                                                                      database.iloc[i]["Attack"],
                                                                      database.iloc[i]["Health_or_Durability"],
                                                                      database.iloc[i]["Effects"],
                                                                      database.iloc[i]["ImageLocation"]))
                if database.iloc[i]["Pattern"] == 1:  # Est une définition d'une arme.
                    self.card_definitions.append(WeaponCardDefinition(database.iloc[i]["Id"], database.iloc[i]["Name"],
                                                                      "",  # database.iloc[i]["Description"]
                                                                      database.iloc[i]["Rarity"],
                                                                      database.iloc[i]["Cost"],
                                                                      database.iloc[i]["Attack"],
                                                                      database.iloc[i]["Health_or_Durability"],
                                                                      database.iloc[i]["ImageLocation"]))
                if database.iloc[i]["Pattern"] == 2:  # Est une définition d'un sort.
                    actions: [Action] = []
                    action_codes: str = (database.iloc[i]["Spell_actions"]).split()
                    for code in action_codes:
                        actions.append(action_dictionary.get_action(code))
                    self.card_definitions.append(SpellCardDefinition(database.iloc[i]["Id"], database.iloc[i]["Name"],
                                                                     "",  # database.iloc[i]["Description"]
                                                                     database.iloc[i]["Rarity"],
                                                                     database.iloc[i]["Cost"],
                                                                     database.iloc[i]["Spell_target"],
                                                                     actions,
                                                                     database.iloc[i]["ImageLocation"]))

    __instance: __Singleton = None

    def __init__(self):
        if not CardDictionary.__instance:
            CardDictionary.__instance = CardDictionary.__Singleton()

    def get_cards(self) -> [MinionCardDefinition]:
        return self.__instance.card_definitions

    def get_card(self, code: str) -> MinionCardDefinition:
        for card_definition in self.get_cards():
            if card_definition.code == code:
                return card_definition
        return None
