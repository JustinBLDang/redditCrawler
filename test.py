fields = ('permalink', 'id', 'title', 'url','selftext','score', 'upvote_ratio', 'created_utc', 'num_comments', 'comments')

testdictionary = {field:field for field in fields}

testdictionary['test'] = ["I am testing how to add to a dictionary.", "banana", "eggs", "combine to make dinner"]
testarray = []
testarray.append(testdictionary)

print(testarray[0]['test'])