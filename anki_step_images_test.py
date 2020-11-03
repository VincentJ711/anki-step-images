from typing import List

from extract_steps import extractSteps, Step


def _extractSteps(text: str, exp: List[Step]):
    res = extractSteps(text)
    assert len(res) == len(exp)

    for i in range(len(res)):
        assert res[i].imgurl == exp[i].imgurl
        assert res[i].desc == exp[i].desc


def test_extractSteps():
    _extractSteps('''
        !stepd desc1 !stepd
        
        <img src="1.jpg"/>
    ''', [Step('desc1', '1.jpg')])

    _extractSteps('''
        !stepd desc1a !stepd
        !stepd desc1b !stepd
        <img src="1.jpg"/>
    ''', [Step('desc1b', '1.jpg')])

    _extractSteps('''
        !stepd desc1a !stepd
        !stepd desc1b !stepd
        <img src="1.jpg"/>
        
        <img src="2.jpg"/>
    ''', [Step('desc1b', '1.jpg'), Step(None, '2.jpg')])

    _extractSteps('''
        !stepd desc1a !stepd
        !stepd desc1b !stepd
        <img src="1.jpg"/>
        
        <img src="2.jpg"/>
        
        !stepd desc3a !stepd
    ''', [Step('desc1b', '1.jpg'), Step(None, '2.jpg')])

    _extractSteps('''
        !stepd desc1a !stepd
        !stepd desc1b !stepd
        <img src="1.jpg"/>
        
        <img src="2.jpg"/>
        
        !stepd desc3a !stepd
        <img src="3.jpg"/>
    ''', [
        Step('desc1b', '1.jpg'),
        Step(None, '2.jpg'),
        Step('desc3a', '3.jpg')
    ])

    _extractSteps('''
        !stepd desc1a !stepd !stepddesc1b!stepd<img src="1.jpg"/>
        <img src="2.jpg"/>!stepd desc3a !stepd<img src="3.jpg"/>
    ''', [
        Step('desc1b', '1.jpg'),
        Step(None, '2.jpg'),
        Step('desc3a', '3.jpg')
    ])

    _extractSteps('', [])
    _extractSteps('        ', [])
    _extractSteps('!stepd a !stepd', [])
