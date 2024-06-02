import re
import json

import logging, sys
logging.disable(sys.maxsize)

import os
import lucene
from java.nio.file import Paths
from org.apache.lucene.store import MMapDirectory, SimpleFSDirectory, NIOFSDirectory
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.document import Document, Field, FieldType
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.index import FieldInfo, IndexWriter, IndexWriterConfig, IndexOptions, DirectoryReader
from org.apache.lucene.search import IndexSearcher, BoostQuery, Query
from org.apache.lucene.search.similarities import BM25Similarity


def create_index(dir):
    if not os.path.exists(dir):
        os.mkdir(dir)
    store = SimpleFSDirectory(Paths.get(dir))
    analyzer = StandardAnalyzer()
    config = IndexWriterConfig(analyzer)
    config.setOpenMode(IndexWriterConfig.OpenMode.CREATE)
    writer = IndexWriter(store, config)

    metaType = FieldType()
    metaType.setStored(True)
    metaType.setTokenized(False)

    contextType = FieldType()
    contextType.setStored(True)
    contextType.setTokenized(True)
    contextType.setIndexOptions(IndexOptions.DOCS_AND_FREQS_AND_POSITIONS)
    
    regex = re.compile('.*[1234567890]+\.json')

    for filename in os.listdir(os.getcwd()):
        if regex.fullmatch(filename):
            with open(os.path.join(os.getcwd(), filename), 'r') as f:
                data = json.load(f)
                print(type(data))
                permalink = data['permalink']
                id = data['id']
                title = data["title"]
                url = data["url"]
                selftext = data["selftext"]
                score = data["score"]
                upvote_ratio = data["upvote_ratio"]
                created_utc = data["created_utc"]
                num_comments = data["num_comments"]
                author = data["author"]
                comments = data["comments"]

                doc = Document()
                doc.add(Field('Permalink', str(permalink), metaType))
                doc.add(Field('Id', str(id), metaType))
                doc.add(Field('Url', str(url), metaType))
                doc.add(Field('Title', str(title), contextType))
                doc.add(Field('Selftext', str(selftext), contextType))
                doc.add(Field('Score', str(score), metaType))
                doc.add(Field('Upvote_ratio', str(upvote_ratio), metaType))
                doc.add(Field('Created_utc', str(created_utc), metaType))
                doc.add(Field('Num_comments', str(num_comments), metaType))
                doc.add(Field('Author', str(author), metaType))
                for comment in comments:
                    doc.add(Field('Comment', str(comment), contextType))

                f.close()
                writer.addDocument(doc)
    writer.close()

def retrieve(storedir, query):
    searchDir = NIOFSDirectory(Paths.get(storedir))
    searcher = IndexSearcher(DirectoryReader.open(searchDir))
    
    parser = QueryParser('Context', StandardAnalyzer())
    parsed_query = parser.parse(query)

    topDocs = searcher.search(parsed_query, 10).scoreDocs
    topkdocs = []
    for hit in topDocs:
        doc = searcher.doc(hit.doc)
        print(hit)
        print(doc)
        # topkdocs.append({
        #     "score": hit.score,
        #     "text": doc.get("Context")
        # })
    return topkdocs
    
# need to change directory to match cs172 server directory
directory = "/home/cs172/redditCrawler"

sample.initVM(vmargs=['-Djava.awt.headless=true'])
create_index(directory)
query = "experiment"
loop = True
while loop:
    print("\nHit enter with no input to quit.")
    query = input("Enter a string: ")
    while(isinstance(query, str)):
        if query == '':
            loop = False
            break
        
        topkDocs = retrieve(directory, query)


