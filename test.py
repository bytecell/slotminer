from rule_loader import rule_loader
from rule_process import rule_process
import logging
import time
import pdb

logger = logging.getLogger('sm')
logger.setLevel(logging.INFO)
streamHandler = logging.StreamHandler()
logger.addHandler(streamHandler)

rl = rule_loader(logger=logger)
rl.load('./timex3.rule')
if not rl.generate_rules():
    exit()

rl.print_rules()

rp = rule_process(rules=rl.get_rules(), logger=logger)

while True:
    text = input()
    if not text:
        break
    start_time = time.time()
    result, variables = rp.process(text)
    end_time = time.time()
    print('원본:', text)
    print('결과:')
    for x in result:
        print('{}'.format(x))
    variables.str()
    print('수행시간={}초'.format(end_time - start_time))
