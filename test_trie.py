from trie_loader import trie_loader
import logging
import time
import pdb

# logger
logger = logging.getLogger('sm')
logger.setLevel(logging.INFO)
streamHandler = logging.StreamHandler()
logger.addHandler(streamHandler)

tr_loader = trie_loader(logger=logger)
trie = tr_loader.make_trie('./rule/sample.trie')

while True:
    text = input('Text input>')
    if not text:
        break
    start_time = time.time()
    result = trie.process(text, longest=True)
    print(result)
    end_time = time.time()
    print('수행시간={}초'.format(end_time - start_time))
