from Definitions.MinionCardDefinition import MinionCardEffectTypes


class Utils:

    @staticmethod
    def polish_minion_effect_type(effects: MinionCardEffectTypes) -> MinionCardEffectTypes:
        if effects & MinionCardEffectTypes.RUSH != 0:
            effects -= MinionCardEffectTypes.RUSH
        if effects & MinionCardEffectTypes.CHARGE != 0:
            effects -= MinionCardEffectTypes.CHARGE
        return effects
