# 목적

텍스트로부터 slot 형태의 임의의 정보를 추출하는 `규칙 기반` 도구로서, 아래의 목적에 활용 가능하다.
한국어를 겨냥해서 설계되었으나, 본 프로젝트의 근간이 되는 `규칙 파일`은 언어와 독립적이므로, 세계 어떤 언어이든간에 구분없이 사용 가능하다.

- 질의응답 시스템
- 대화시스템 (챗봇)
- 텍스트 전처리 및 슬롯(slot) 추출

# 설치 방법

본 프로젝트를 클론받고 환경변수 설정

```
(예시) 만약 bash 사용 중이라면, ~/.bashrc 파일에서 아래와 같이 환경설정 

SLOTMINER=/home/you/slotminer
PYTHON_PATH=$PYTHON_PATH:$SLOTMINER
```

# 의존성 (dependency)

- python 3.x

# 테스트 실행 방법

아래와 같이 쉘창에서 테스트를 실행 가능하다.
사용자가 직접 규칙 파일을 작성한 후, test.py 내용을 참고하여 다른 어플리케이션 또는 서비스에 사용할 수 있다.
텍스트에 대하여 규칙을 체크할 때, Tree(트리) 기반으로 recursive call으로써 규칙을 체크하기 때문에 너무 긴 텍스트에 대해서는 '콜스택 오버플로우' 등의 에러가 발생할 수 있으므로 유의해야 한다.
따라서, test.py 내용을 참고하여 너무 긴 텍스트는 적당한 길이(예: 100~500글자 사이)로 잘라서 사용하는 것을 권장한다.
또한, 영어 알파벳 텍스트에 적용할 경우에는 소문자화하여 규칙을 체크하도록 한다.

```
~/slotminer$ python3 test.py
```

# 기능

기본적으로는 다양한 형태의 `slot을 추출`하도록 설계되었으며, 규칙 파일에서 추출 규칙들을 정의함으로써 기능 확장이 가능하다.
개발자는 slotminer 의 소스코드에 기여할 수도 있고, 특정 slot을 추출하는 규칙 파일을 생성/개선함으로써 기여가 가능하다.
특징으로는 white-space (스페이스바)은 텍스트 매칭 대상에서 기본적으로 무시되므로, 규칙이 "기원전"일 경우, "기  원  전", "기원  전" 등과 같은 텍스트들이 모두 규칙 매칭에 통과된다.
명시적으로 규칙에서 white-space 를 체크하도록 하고 싶을 경우, white-space 를 대괄호로 둘러싼 형태(예: [ ])를 사용하면 된다. 

현재 제공되는 기능은 아래와 같다.

## 기능1: 시간정보추출

최근, 기계학습과 딥러닝 등을 통해 시간정보에 대한 '정규화'를 자동화하려는 연구들이 있으나, 실제 서비스에 적용되기에는 갈 길이 매우 멀다.
특히, `1999년`, `다음주 수요일`과 같은 표현(이를 TIMEX3 slot 이라고 부른다)에 대한 추출 및 정규화는 규칙을 기반으로 추출하는 것이 더 효과적이라 할 수 있다.
기본적으로는 ISO-8601과 ISO-TimeML 표준을 따르지만, [Y.S. Jeong et al., 2016](http://www.lrec-conf.org/proceedings/lrec2016/pdf/175_Paper.pdf) 논문에서 언급하듯이, 실제 프로그램 상에서는 위 두개의 표준을 그대로 따르게 되면 매우 비효율적이거나 표현하지 못하는 시간 정보들이 존재한다.
따라서, [Y.S. Jeong et al., 2016](http://www.lrec-conf.org/proceedings/lrec2016/pdf/175_Paper.pdf) 논문과 [C.G. Lim et al., 2018](http://aclweb.org/anthology/L18-1326) 논문에서 제시하는 새로운 Korean TimeML을 반영하여 시간정보를 추출한다.
이 기능을 위한 규칙파일은 `rule/timex3.rule` 이다. 

특히, 시간정보 중에서 EVENT, MAKEINSTANCE, TLINK 등은 제외하고, TIMEX3 에서도 주로 사용되는 표현 외에는 과감히 제외하였다.
예를 들면, 추출되는 정보를 불필요하게 번잡하게 만드는 'SET' 타입 TIMEX3는 제외되었다.
추출되는 TIMEX3 정보에 대한 정의는 아래와 같다.
만약 기업/기관에서 사용하려는 별도의 시간정보를 추가하는 작업을 의뢰하고 싶다면 본문 맨 밑에 적혀있는 제휴문의를 참고바란다.


```python
attributes ::= type text extent calendar [year] [month] [day] [week] [week_day] [mod] 
type ::= 'DATE' | 'TIME' | 'DURATION'
text ::= CDATA
extent ::= [(begin, end), ...]
begin ::= CDATA {begin ::= <integer>}
end ::= CDATA {end ::= <integer>}
calendar ::= 'GREGORIAN' | 'LUNAR' | 'JULIAN'
year ::= mark CDATA
month ::= mark CDATA
day ::= mark CDATA
hour ::= mark CDATA
minute ::= mark CDATA
second ::= mark CDATA
week ::= mark CDATA
week_day ::= 0 | 1 | 2 | 3 | 4 | 5 | 6
mark ::= 'P' | '+' | '-' | '_' (Note: '_'는 '기원전' 표현 전용)
mod ::= 'START' | 'MID' | 'END' | 'START_MID' | 'MID_END'
```

### 실행 예시
```python
원본: 3년 5개월동안
결과:
{'year': 'P3', 'type': 'DURATION', 'month': 'P5', 'calendar': 'GREGORIAN', 'text': '3년 5개월', 'name': 'slot_timex3', 'extent': [(0, 6)]}

원본: 여자친구와 다음주 수요일에 만나기로 했다.
결과:
{'name': 'slot_timex3', 'week_day': '3', 'extent': [(6, 13)], 'calendar': 'GREGORIAN', 'type': 'DATE', 'text': '다음주 수요일', 'week': '+1'}
```

### 규칙 예시
```python
        "Rweek_day": {
                "name": "slot_timex3",
                "result": {"week_day": "[$s]", "type": "DATE", "calendar": "GREGORIAN"},
                "condition": [
                        {"ext": "(월[$s=1]|화[$s=2]|수[$s=3]|목[$s=4]|금[$s=5]|토[$s=6]|일[$s=0])요일"}
                ]
        },

```

## 기능2: 병원 마취전 평가서 텍스트로부터 정형화된 정보 추출

병원에서 수술을 앞둔 시점에 '평가서'를 작성하는데, 이 평가서에는 환자의 상태, 특징 등의 정보를 담고 있으므로 여러가지로 활용(예: 환자의 수술후 예후 예측 등)이 가능하다.
하지만, 이 평가서는 자연어 문장의 나열로써 작성되기 때문에 평가서로부터 정형화된 정보를 추출하는 작업이 필요하다.
이 기능은 임상 의료인이 수술전에 작성하는 평가서 텍스트로부터 정형화된 정보를 추출해준다.

```python
attributes ::= name feature text extent 
name ::= 'slot_param1'
feature ::= CDATA
text ::= CDATA
extent ::= [(begin, end), ...]
begin ::= CDATA {begin ::= <integer>}
end ::= CDATA {end ::= <integer>}
```

기본적으로는 `순천향대학교 서울병원`(https://www.schmc.ac.kr/seoul/index.do)에서 사용되는 전문용어/약어를 기준으로 규칙이 작성되었으며, 다른 병원 및 기관에서는 다소의 용어 차이가 존재할 수 있다.
규칙파일 경로는 `rule/sch_seoul.rule` 이다.

결과물로 생성되는 slot들 중에 'name'값이 'slot_number'로써 생성되는 slot들은 단순숫자표현만을 인지하므로 무시하도록 한다.
숫자표현을 인식하는 이유는 glucose, TFT 등과 같이 수치값을 추출하는 용어에 대한 처리를 위함이다.

따라서 'name'값이 'slot_param1'인 slot에 대하여, `feature`항목의 값은 약 50가지 이상의 전문용어/약어에 대한 정보를 담게 된다.
이 정보는 특정 용어/약어가 평가서에 존재하는지 여부를 나타내며, 때때로 수치값(예: glucose:50)을 추출해주기도 한다.

추출되는 용어/약어들에 대한 목록은 아래와 같다.
만약 병원/기관에서 사용하는 별도의 용어들을 추가하는 작업을 의뢰하고 싶다면 본문 맨 밑에 적혀있는 제휴문의를 참고바란다.

- COPD, Bedridden, CPR, Alcoholic hepatitis, Alcoholic LC, IPF, Anemia, Myocardial infarction, PCI, Atherosclerosis, DVT, Carotid artery stenosis, Cerebral atherosclerosis, ESRD KT, Hyperparathyroidism, CAD, Fatty liver, Angina, VPC, APC, CHF, MR, MS, HTN, Pulmonary hypertension, Pulmonary embolism, TR, DM, Diastolic dysfunction, Concentric LVH, Eccentric LVH, HCMP, LAE, RAE, LVE, RVE, Ischemic heart disease, Regional wall motion abnormality, LV systolic dysfunction, RV dysfunction, A.fib, DCMP, AS, AR, Uremic CMP, IVC plethora, Pericardial effusion, Pleural effusion, Depression, Cancer, Glucose, aBGA, EGFR, CAG, TFT  

### 실행 예시
```python
원본:  TFT : TSH/fT4/T3 3.66(N)/1.26(N)/60.03(L)
결과:
{'text': 'fT4/T33.66(N)/1.26(N)/60.03', 'name': 'slot_param1', 'feature': 'ft4:1.26:t3:60.03', 'extent': [(10, 37)]}

원본:  Chest CT :. Diffuse tubular bronchiectasis and multiple small subsolid/solid 
결과: 
{'text': 'bronchiectasis', 'name': 'slot_param1', 'feature': 'copd', 'extent': [(60, 74)]}
```

### 규칙 예시
```python
        "Rtft": {
                "name": "slot_param1",
                "result": {"feature": "ft4:[$s0]:t3:[$s1]"},
                "condition": [
                        {"ext": "(ft4/t3)([ ])?[$s=([@Rnumber.value])]([.]){3}/[$s0=([@Rnumber.value])]([.]){3}/[$s1=([@Rnumber.value])]"}
                ]
        }
```


# 규칙 작성 방법

1. 규칙파일: 규칙파일은 1개 이상의 규칙들의 모음이며, 규칙은 json 양식으로 기술된다. 규칙파일에는 다음의 것들이 포함된다.

   - 전/후처리 정보
   - 규칙들
  
2. 규칙: 규칙은 기본적으로 텍스트 매칭을 통해 `결과물`(슬롯 또는 태그)을 생성한다. 규칙파일에서 기술되는 각각의 규칙은 아래 사항을 포함한다.

   - 규칙 이름 (주의: 규칙이름은 중복될 수 없다. 중복되면 나중에 정의된 규칙이 앞선 규칙을 덮어쓴다.)
   - 생성될 결과물의 이름, 키-값의 쌍, 조건들
      - 참고: 결과물은 최소한 3가지(name, text, extent)의 키-값 쌍을 포함한다.
   
3. 규칙 작성 방법 (기초레벨 I)

   아래 규칙을 참고하자. 이 규칙에서는, 규칙의 이름은 Rule 이고, 결과물의 이름은 slot_sample, 키-값의 쌍은 value: 100 이며, 조건들은 condition 에 해당한다.
   
   ```python
   "Rule" : {
     "name": "slot_sample",
     "result": {"value": "100"},
     "condition": [
        {"ext": "hundred"}
     ]
   }
   ```
  
  이 규칙을 텍스트 "one hundred"에 적용하면, 아래와 같은 결과물이 생성된다. 
  
  ```python
  {'name': 'slot_sample', 'extent': [(4, 11)], 'text': 'hundred', 'value': '100'}
  ```
  
4. 규칙 작성 방법 (기초레벨 II)

   아래 규칙을 참고하자.
   condition 부분에서 매칭하려는 텍스트 부분을 관찰해보면, 정규식 문법과 유사하게 작성된 것을 볼 수 있다.
   사용가능한 표현들은 +, ?, | 이다.
   이 표현들은 소괄호와 항상 함께 써야 한다. 예를 들어, (a)+ 이라고 하면, a 문자 1개 이상을 의미한다.
   기본적으로 공백은 무시하도록 되어있는데, 만약 공백을 체크하고 싶을 경우에는 [ ] 이라고 기술하면 된다.
   문장의 맨 처음이거나 white-space(' ', '\t' 등)인 경우는 [<] 이라고 기술할 수 있으며, 문장의 맨 끝이거나 white-space인 경우는 [>]이라고 기술한다.
   
   ```python
   "Rule" : {
     "name": "slot_sample",
     "result": {"value": "pet"},
     "condition": [
        {"ext": "(dog|cat)"}
     ]
   }
   ```
  
  이 규칙을 텍스트 "I have a dog and a cat"에 적용하면, 아래와 같은 결과물이 생성된다.
  
  ```python
  {'extent': [(9, 12)], 'value': 'pet', 'text': 'dog', 'name': 'slot_sample'}
  {'extent': [(19, 22)], 'value': 'pet', 'text': 'cat', 'name': 'slot_sample'}
  ```
  
  주의할 점으로,
  | 표현을 사용할 때에는 항목들을 왼쪽부터 고려한다는 점에 유의해야 한다.
  예를 들어, (dog|doggie) 라는 기술할 경우, "It's a doggie" 문장에 대해 적용했을 때 "dog" 부분이 매칭될 것이다. 규칙에 dog 또는 doggie 를 검출하도록 기술했음에도 불구하고, dog 가 doggie 보다 왼쪽에 있으므로, dog가 매칭되었을 때 doggie는 더이상 고려되지 않는 것이다.
  이런 문제를 해결하고 싶다면, `(doggie|dog)` 또는 `(dog(gie)?)` 와 같이 기술할 수 있다.  
  
5. 규칙 작성 방법 (기초레벨 III)

   아래 규칙을 참고하자.
   먼저 condition 부분을 잘 관찰해보자. 대괄호로 둘러싸인 부분의 동작은 `s` 라는 이름의 `변수`를 만들고, 그 변수에 `3`이라는 값을 넣는 것이다.
   그 다음은 result 부분을 살펴보면, value 키의 값에 `변수 s`가 사용되었다. 즉, condition 부분에서 생성한 변수의 값을 결과물의 키-값에서 사용이 가능한 것이다.
   
   ```python
   "Rule" : {
     "name": "slot_sample",
     "result": {"value": "[$s]"},
     "condition": [
        {"ext": "three[$s=3]"}
     ]
   }
   ```
   
   이 규칙을 텍스트 "I am three years old"에 적용하면, 아래와 같은 결과물이 생성된다.

   ```python
   {'text': 'three', 'extent': [(5, 10)], 'value': '3', 'name': 'slot_sample'}
   ```

6. 규칙 작성 방법 (중급레벨 I)

   아래 규칙을 참고하자.
   condition 에서 변수를 생성하고 있는데, 변수의 값에 해당하는 부분을 소괄호로 둘러싸서 or 연산(|)으로 기술하는 경우, 이 부분이 직접 변수의 값에 들어가게 된다.
   
   ```python
   "Rule" : {
     "name": "slot_sample",
     "result": {"value": "[$s]"},
     "condition": [
        {"ext": "[$s=(dog|cat)]"}
     ]
   }
   ```
   
   이 규칙을 텍스트 "I have a dog and a cat"에 적용하면, 아래와 같은 결과물이 생성된다.

   ```python
   {'text': 'dog', 'value': 'dog', 'name': 'slot_sample', 'extent': [(9, 12)]}
   {'text': 'cat', 'value': 'cat', 'name': 'slot_sample', 'extent': [(19, 22)]}
   ```
   
   위 규칙 예시에서는 변수의 값에 소괄호가 등장하였는데, 반대로 소괄호와 |(or) 연산의 안쪽에 변수 값을 지정하는 것도 가능하다.
   물론, 이 두 가지를 섞어서 쓰는 것도 가능하다.
   아래 예시를 관찰해보자.
   가장 바깥쪽 | 표현의 왼쪽 부분은 (dog|puppy) 를 만족할 경우 $s 변수에 `강아지` 값을 넣는다는 내용이며, 오른쪽 부분은 (cat|kitten) 을 만족할 경우 그 텍스트 자체를 $s 변수에 넣는다는 내용이다.
   
   ```python
   "Rule" : {
     "name": "slot_sample",
     "result": {"value": "[$s]"},
     "condition": [
        {"ext": "((dog|puppy)[$s=강아지]|[$s=(cat|kitten)])"}
     ]
   }
   ```
   
   이 규칙을 텍스트 "I have a dog and a kitten."에 적용하면, 아래와 같은 결과물이 생성된다.
   
   ```python
   {'text': 'dog', 'name': 'slot_sample', 'value': '강아지', 'extent': [(9, 12)]}
   {'text': 'kitten', 'name': 'slot_sample', 'value': 'kitten', 'extent': [(17, 23)]}
   ```
   
   
7. 규칙 작성 방법 (중급레벨 II)

   지금까지는 condition 부분에 1개의 조건만 포함시켰으나, 2개 이상의 조건을 포함시킬 수 있다.
   아래 예시를 보자.
   
   ```python
   "Rule" : {
     "name": "slot_sample",
     "result": {"value": "[$s]"},
     "condition": [
        {"ext": "(one[$s=1]|two[$s=2])"},
        {"ext": "dollar"}
     ]
   }
   ```
   
   이 규칙을 텍스트 "I have two dollars!"에 적용하면, 아래와 같은 결과물이 생성된다.
   
   ```python
   {'extent': [(7, 10), (11, 17)], 'name': 'slot_sample', 'text': 'twodollar', 'value': '2'}
   ```
   
   기술하였던 조건들과 결과물을 관찰해보면, 결국 2개의 조건들을 `(one[$s=1]|two[$s=2])dolloar`로써 1개의 조건으로 합칠 수 있다는 것을 알 수 있다.
   이렇듯 여러 개의 조건들을 1개의 조건으로 쉽게 합칠 수 있음에도 불구하고, condition 부분에서 여러 조건들을 둘 수 있도록 한 것은 아래와 규칙을 보면 알 수 있다.
   이 규칙은 언뜻 보면 위 규칙과 동일해 보이지만, 첫 번째 조건의 키가 `ext`가 아닌 `next`라는 점을 알 수 있다.
   조건의 키가 `ext`인 것은 결과물 텍스트 extent(범위)에 포함이 된다는 의미이며, `next`는 포함되지 않는다는 뜻이다.
   
   ```python
   "Rule" : {
     "name": "slot_sample",
     "result": {"value": "[$s]"},
     "condition": [
        {"next": "(one[$s=1]|two[$s=2])"},
        {"ext": "dollar"}
     ]
   }
   ```
   
   이 규칙을 텍스트 "I have two dollars!"에 적용하면, 아래와 같은 결과물이 생성된다.
   
   ```python
   {'extent': [(11, 17)], 'name': 'slot_sample', 'text': 'dollar', 'value': '2'}
   ```
   
   각 조건의 키는 `ext` 또는 `next`중에 하나만을 가질 수 있으며, 조건을 체크하면서도 원하는 부분만 결과물 텍스트 범위에 포함할 수 있게 된다.


# 라이센스, 제휴

연구, 비영리 사업 목적에 해당하는 경우, 본 프로젝트를 자유롭게 사용할 수 있다.
단, 각 기능에 대하여 아래의 항목들 중에 적어도 1개를 해당 사업 또는 연구논문에 reference 로 추가하는 조건 하에 사용할 수 있다.

## 기능1: 시간정보추출

- [Y.S. Jeong et al., 2016](http://www.lrec-conf.org/proceedings/lrec2016/pdf/175_Paper.pdf)
- [C.G. Lim et al., 2018](http://aclweb.org/anthology/L18-1326)
- [Y.S. Jeong et al., 2017](http://www.dbpia.co.kr/Journal/ArticleDetail/NODE07286957)
- [Y.S. Jeong et al., 2015](http://aclweb.org/anthology/K15-1028)

## 기능2: 병원 마취전 평가서 텍스트로부터 정형화된 정보 추출

- [H. Kim et al., 2020](https://www.mdpi.com/2076-3417/10/3/1151)

특히, 아래 두 가지에 해당되는 경우에는 본 프로젝트 책임자( pinodewaider_at_gmail.com )에게 연락하여 제휴/제안을 논의할 수 있다.

1. slotminer 프로젝트를 영리 사업에 활용하고자 하는 경우
   - 연구, 비영리 사업에는 무료로 사용 가능(단, 위의 각 기능 별로 1개 이상의 reference 명시)
2. 향상된 버전(예: 시간정보 추출 규칙파일 공개버전보다 향상된 버전)을 필요로 하는 경우
   - 본프로젝트에서 제공되는 기능은 누구나 이용 가능하지만, 책임자가 직접 관리하는 `향상된 버전의 규칙 파일`은 open 되어있지 않으며, 이 파일을 얻고 싶은 경우
