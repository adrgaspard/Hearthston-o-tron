#from Components.Hero import Hero
from Definitions.Action import Action, ActionTypes


class ActionTranslator:

    @staticmethod
    def apply_action(action: Action, launcher):
        if action.actionType == ActionTypes.SPECIAL:
            return ActionTranslator.apply_special_action(action, launcher)
        # /!\ Ne sera pas implémenté, mais ici il faut coder pour chaque ActionTypes ce que ça va produire

    @staticmethod
    def apply_special_action(action: Action, launcher):
        # Vérification que l'action est bien légitime a être envoyée sur cette méthode
        if action.actionType & ActionTypes.SPECIAL == 0:
            raise ValueError("L'action doit être spéciale.")

        # Application des effets selon le code (id) de l'action.
        if action.code == "coin":
            launcher.mana = launcher.mana + 1
