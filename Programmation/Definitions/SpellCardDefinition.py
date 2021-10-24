from Definitions.Action import ActionTypes
from Definitions.CardDefinition import CardDefinition, CardPattern, TargetTypes, CardRarity

# NE SERA PAS UTILISE AU RENDU DU PROGRAMME : On a pas assez de temps pour utiliser ce contenu mais on fait en sorte
# qu'il pourra l'être dans le futur.


class SpellCardAction:
    def __init__(self, code: str, actionType: ActionTypes, target: TargetTypes, parameter):
        self.code: str = code
        self.actionType: ActionTypes = actionType
        self.target: TargetTypes = target
        self.parameter = parameter  # Pour les types d'action spéciaux et le give_effect


class SpellCardDefinition(CardDefinition):
    def __init__(self, code: str, name: str, description: str, rarity: CardRarity, cost: int, target: TargetTypes, actions: [SpellCardAction], image_location: str):
        super().__init__(code, name, description, rarity, cost, CardPattern.SPELL, image_location)
        self.target: TargetTypes = target
        self.actions: [SpellCardAction] = actions
