from cell import Cell


class Rules(object):

    ruleSets = {'basic': {'stayAlive': '23', 'becomeAlive': '3'},
                    'hard': {'stayAlive': '45', 'becomeAlive': '5'},
                    'impossible': {'stayAlive': '67', 'becomeAlive': '7'},
                    'easy': {'stayAlive': '12', 'becomeAlive': '2'},
                    'weird': {'stayAlive': '27', 'becomeAlive': '4'},

               }

    ruleSet = 'basic'
    currentruleSet = 'basic'
    stayAlive = ruleSets[ruleSet]['stayAlive']
    becomeAlive = ruleSets[ruleSet]['becomeAlive']
    stayAlive1 = stayAlive[0]
    stayAlive2 = stayAlive[1]

    @classmethod
    def set_rules(cls, ruleSet):
        legalValues = cls.ruleSets.keys()
        if ruleSet in legalValues:
            cls.ruleSet = ruleSet
            cls.stayAlive = cls.ruleSets[ruleSet]['stayAlive']
            cls.stayAlive1 = cls.stayAlive[0]
            cls.stayAlive2 = cls.stayAlive[1]
            cls.becomeAlive = cls.ruleSets[ruleSet]['becomeAlive']
        else:
            raise ValueError(f'RuleSet must be in {legalValues}.')


    @classmethod
    def set_rules_user_values(cls, stayAlive, becomeAlive):
        numberOfCharacterSets = len(Rules.ruleSets)
        key = f'user defined {numberOfCharacterSets}'
        Rules.ruleSets[key] = {'stayAlive': stayAlive, 'becomeAlive': becomeAlive}