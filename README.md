# 목적

```
한국어 텍스트로부터 slot 형태의 임의의 정보를 추출하는 `규칙 기반` 도구로서, 아래의 목적에 활용 가능하다.

- 질의응답 시스템
- 대화시스템 (챗봇)
```

# 실행 예시
```python
원본: 3년 5개월동안
결과:
{'year': 'P3', 'type': 'DURING', 'month': 'P5', 'calendar': 'GREGORIAN', 'text': '3년 5개월', 'name': 'slot_timex3', 'extent': [(0, 6)]}

원본: 여자친구와 다음주 수요일에 만나기로 했다.
결과:
{'name': 'slot_timex3', 'week_day': '3', 'extent': [(6, 13)], 'calendar': 'GREGORIAN', 'type': 'DATE', 'text': '다음주 수요일', 'week': '+1'}
```

# 규칙 예시
```python
        "Rweek_day": {
                "name": "slot_timex3",
                "result": {"week_day": "[$s]", "type": "DATE", "calendar": "GREGORIAN"},
                "condition": [
                        {"ext": "(월[$s=1]|화[$s=2]|수[$s=3]|목[$s=4]|금[$s=5]|토[$s=6]|일[$s=0])요일"}
                ]
        },

```

# 기능

기본적으로는 다양한 형태의 `slot을 추출`하도록 설계되었으며, 규칙 파일에서 추출 규칙들을 정의함으로써 기능 확장이 가능하다.
개발자는 slotminer 의 소스코드에 기여할 수도 있고, 특정 slot을 추출하는 규칙 파일을 생성/개선함으로써 기여가 가능하다.

현재 제공되는 기능은 아래와 같다.

## 시간정보 slot

최근, 기계학습과 딥러닝 등을 통해 시간정보에 대한 '정규화'를 자동화하려는 연구들이 있으나, 실제 서비스에 적용되기에는 갈 길이 매우 멀다.
특히, `1999년`, `다음주 수요일`과 같은 표현(이를 TIMEX3 slot 이라고 부른다)에 대한 추출 및 정규화는 규칙을 기반으로 추출하는 것이 더 효과적이라 할 수 있다.
기본적으로는 ISO-8601과 ISO-TimeML 표준을 따르지만, [Y.S. Jeong et al., 2016](http://www.lrec-conf.org/proceedings/lrec2016/pdf/175_Paper.pdf) 논문에서 언급하듯이, 실제 프로그램 상에서는 위 두개의 표준을 그대로 따르게 되면 매우 비효율적이거나 표현하지 못하는 시간 정보들이 존재한다.
따라서, [Y.S. Jeong et al., 2016](http://www.lrec-conf.org/proceedings/lrec2016/pdf/175_Paper.pdf) 논문과 [C.G. Lim et al., 2018](http://aclweb.org/anthology/L18-1326) 논문에서 제시하는 새로운 Korean TimeML을 반영하여 시간정보를 추출한다.

특히, 시간정보 중에서 EVENT, MAKEINSTANCE, TLINK 등은 과감히 빼고, TIMEX3 에서 주로 사용되는 표현을 추출한다.
추출되는 TIMEX3 정보에 대한 정의는 아래와 같다.

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
week ::= mark CDATA
week_day ::= 0 | 1 | 2 | 3 | 4 | 5 | 6
mark ::= 'P' | '+' | '-' | '_' (Note: '_'는 '기원전' 표현 전용)
mod ::= 'START' | 'MID' | 'END' | 'START_MID' | 'MID_END'
```


# 라이센스, 제휴, 제안

본 프로젝트에서 제공하는 `기능`은 기본적으로 누구나 사용가능하지만, 아래 두 가지에 해당되는 경우에 이 프로젝트 책임자에게 연락하여 제휴/제안을 논의할 수 있다.

1. slotminer 프로젝트를 영리 사업에 활용하고자 하는 경우
   - 연구, 비영리 사업에는 무료로 사용 가능
2. 기존 기능의 향상된 버전(예: 시간정보 추출 기능의 향상 버전)을 필요로 하는 경우
   - 본프로젝트에서 제공되는 기능은 누구나 이용 가능하지만, 책임자가 직접 관리하는 `향상된 버전의 규칙 파일`은 open 되어있지 않으며, 이 파일을 얻고 싶은 경우
