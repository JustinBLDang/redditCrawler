import json
fields = ("permalink", "user")

testdictionary = {field:field for field in fields}

# testdictionary['test'] = ["I am testing how to add to a dictionary.", "banana", "eggs", "combine to make dinner"]
testarray = []
testarray.append(testdictionary)
jsonstr = json.dumps(testarray)
result = json.loads(jsonstr)
result.append(testdictionary)

print(testarray)
print(result)