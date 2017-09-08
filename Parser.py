from More_Op import more_Op as mo

class Parser():
    @classmethod
    def parseSpecificVariable(cls, element, config, variable_name):
        param = config["param"]
        more_op = config["moreOp"]
        tags = element.select(param)
        values = []
        for each_tag in tags:
            values.append(mo[more_op](each_tag))
        one_variable = {variable_name: " ".join(value for value in values)}
        return one_variable

    @classmethod
    def parseStringVariable(cls, config, variable_name):
        return {variable_name: mo[config]()}

    @classmethod
    def parseStringWithEle(cls, element, config, variable_name):
        return {variable_name: mo[config](element)}

    @classmethod
    def parseKeyValue(cls, element, config):
        key_param = config["key"]["param"]
        key_more_op = config["key"]["moreOp"]
        value_param = config["value"]["param"]
        value_more_op = config["value"]["moreOp"]

        one_property = {}
        keys_elements = element.select(key_param)
        value_elements = element.select(value_param)
        for i in range(len(keys_elements)):
            key = mo[key_more_op](keys_elements[i])
            value = mo[value_more_op](value_elements[i])
            one_property.update({key: value})
        return one_property
