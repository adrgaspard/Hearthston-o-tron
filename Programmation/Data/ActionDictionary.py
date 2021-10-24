import pandas as pd

from Definitions.Action import Action
from Utils.Configuration import Configuration


class ActionDictionary:
    class __Singleton:

        def __init__(self):
            self.action_definitions: [Action] = []
            database = pd.read_csv(Configuration.ACTION_DEFINITIONS_PATH, sep=Configuration.CSV_SEPARATOR)
            for i in range(len(database)):
                self.action_definitions.append(
                    Action(database.iloc[i]["Id"], database.iloc[i]["Action_type"], database.iloc[i]["Action_target"],
                           database.iloc[i]["Value"]))

    __instance: __Singleton = None

    def __init__(self):
        if not ActionDictionary.__instance:
            ActionDictionary.__instance = ActionDictionary.__Singleton()

    def get_actions(self) -> [Action]:
        return self.__instance.action_definitions

    def get_action(self, code: str) -> Action:
        for action_definition in self.get_actions():
            if action_definition.code == code:
                return action_definition
        return None
