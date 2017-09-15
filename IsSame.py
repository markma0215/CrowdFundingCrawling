
import json
import sys

class checkSame():

    notComparedVariables = ["Campaign ID", "link", "Data Collection Date", "First_Time(0/1)",
                            "Campaign Name", "Fund Name", "Portal ID"]

    @classmethod
    def IsSame(cls, oldOne, newOne):
        if not isinstance(oldOne, dict) or not isinstance(newOne, dict):
            print "the comparison method only can compare dictionaries"
            sys.exit(1)

        obj1Sorted = []
        for each_key in sorted(oldOne.keys()):
            if oldOne[each_key] == "" or each_key in cls.notComparedVariables:
                continue
            obj1Sorted.append(each_key + ": " + oldOne[each_key])

        obj2Sorted = []
        for each_key in sorted(newOne.keys()):
            if newOne[each_key] == "" or each_key in cls.notComparedVariables:
                continue
            obj2Sorted.append(each_key + ": " + newOne[each_key].decode("utf-8"))

        obj1Json = json.dumps(obj1Sorted)
        obj2Json = json.dumps(obj2Sorted)

        # print obj1Json
        # print obj2Json

        if obj1Json == obj2Json:
            return True
        else:
            return False

    @classmethod
    def getChangedVariables(cls, oldOne, newOne):
        changed = {}
        iterKeys = list(set(oldOne.keys() + newOne.keys()))

        for eachKey in iterKeys:

            if eachKey == "link":
                changed.update({eachKey: newOne[eachKey]})
                continue

            if eachKey in cls.notComparedVariables:
                changed.update({eachKey: oldOne[eachKey]})
                continue

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

    @classmethod
    def eraseSameVariables(cls, property):
        cannotBeErased = ["Portal ID", "link", "Campaign ID", "Campaign Name", "Data Collection Date"]
        for each_key in property:
            if each_key in cannotBeErased:
                continue
            else:
                property.update({each_key: ""})
        return property


