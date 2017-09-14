
import json
import sys

class checkSame():
    @classmethod
    def IsSame(cls, oldOne, newOne):
        if not isinstance(oldOne, dict) or not isinstance(newOne, dict):
            print "the comparison method only can compare dictionaires"
            sys.exit(1)
        obj1Sorted = {}
        for each_key in sorted(oldOne.keys()):
            if oldOne[each_key] == "":
                continue
            obj1Sorted.update({each_key, oldOne[each_key]})

        obj2Sorted = {}
        for each_key in sorted(newOne.keys()):
            if newOne[each_key] == "":
                continue
            obj2Sorted.update({each_key, newOne[each_key]})

        obj1Json = json.dumps(obj1Sorted)
        obj2Json = json.dumps(obj2Sorted)

        if obj1Json == obj2Json:
            return True
        else:
            return False

    @classmethod
    def SameCompaignFundName(cls, oldOne, newOne):
        return oldOne["Campaign Name"] == newOne["Campaign Name"] and oldOne["Fund Name"] == newOne["Fund Name"]

    @classmethod
    def getChangedVariables(cls, oldOne, newOne):
        changed = {}
        if len(oldOne.keys()) <= len(newOne.keys()):
            iterKeys = newOne.keys()
        else:
            iterKeys = oldOne.keys()

        for eachKey in iterKeys:
            if eachKey in oldOne and eachKey in newOne:
                if oldOne[eachKey] == newOne[eachKey]:
                    changed.update({eachKey: ""})
                else:
                    changed.update({eachKey: newOne[eachKey]})
            elif eachKey in oldOne and eachKey not in newOne:
                changed.update({eachKey: oldOne[eachKey]})
            else:
                changed.update({eachKey: newOne[eachKey]})
        return changed


