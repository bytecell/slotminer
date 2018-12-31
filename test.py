from rule_loader import rule_loader
from rule_process import rule_process
import logging
import time
import pdb

# logger 생성
logger = logging.getLogger('sm')
# logging.INFO는 화면에 수행과정 출력, logging.ERROR는 에러메시지만 출력
logger.setLevel(logging.INFO)
streamHandler = logging.StreamHandler()
logger.addHandler(streamHandler)

# 규칙을 파일로부터 읽어들임
rl = rule_loader(logger=logger)
rl.load('./timex3.rule')
if not rl.generate_rules():
    exit()
# 읽어들인 규칙을 화면에 표시
rl.print_rules()

# 규칙 '수행(실행)' 객체 생성
rp = rule_process(rules=rl.get_rules(), logger=logger)

while True:
    text = input()
    # 빈 줄 입력시 종료
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
