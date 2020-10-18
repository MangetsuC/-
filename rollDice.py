from random import randint
from time import strftime, localtime
import json

def roll(times :int, maxNum :int) -> dict:
    result = dict()
    result['times'] = times
    result['max'] = maxNum
    result['locateTime'] = strftime("%Y-%m-%d %H:%M:%S", localtime())

    sumNum = 0

    for i in range(times):
        diceNum = randint(1, maxNum)
        sumNum += diceNum
        result['eachNum'] = result.get("eachNum", '') + f'{diceNum}'
        if i != times - 1:
            result['eachNum'] = result.get("eachNum", '') + ' + '
    result['sumNum'] = sumNum
    
    return result

