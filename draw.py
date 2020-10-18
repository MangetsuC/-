#高约90px 宽度不确定 15 [10] 10 [15] 10 [15] 15
import json
from PIL import Image, ImageDraw, ImageFont

def drawRoundRec(drawObject, color, x, y, w, h, r):
    drawObject.ellipse((x,y,x+r,y+r),fill=color)    
    drawObject.ellipse((x+w-r,y,x+w,y+r),fill=color)    
    drawObject.ellipse((x,y+h-r,x+r,y+h),fill=color)    
    drawObject.ellipse((x+w-r,y+h-r,x+w,y+h),fill=color)

    drawObject.rectangle((x+r/2,y, x+w-(r/2), y+h),fill=color)    
    drawObject.rectangle((x,y+r/2, x+w, y+h-(r/2)),fill=color)
    


def drawDiceResult(path, maxLine, maxColumn):
    fontTime = ImageFont.truetype(u'simhei.ttf', 15)
    fontText = ImageFont.truetype(u'simhei.ttf', 20)
    with open(path + '/diceData.json', mode='r') as f:
        diceData = f.read()
    
    diceData = json.loads(diceData)
    diceData = diceData['dice']

    diceNum = 0
    while diceNum < len(diceData):
        tempImg = Image.new("RGB", (1600, 90 * maxLine), color=(250, 250, 250))
        drawImg = ImageDraw.Draw(tempImg)
        totalW = 0
        isContinue = False

        for j in range(maxColumn):
            nowColumnMaxW = 0
            

            for i in range(maxLine):
                tempDice = diceData[diceNum]
                textTime = tempDice['locateTime']
                textInput = '.r{0}d{1}'.format(tempDice['times'], tempDice['max'])
                textAns = '骰出了({0}d{1} = {2}) = {3}'.format(tempDice['times'], tempDice['max'], tempDice['eachNum'], tempDice['sumNum'])
                maxW, uselessH = fontText.getsize(textAns)
                nowColumnMaxW = maxW if maxW > nowColumnMaxW else nowColumnMaxW
                if 25 * (j + 1) + 20 * j + totalW + 45 + maxW > 1600:
                    isContinue = True
                    break
                drawRoundRec(drawImg, (67, 68, 72), 25 * j + 20 * j + totalW + 15, 90 * i + 10, maxW + 20, 75, 20)
                drawImg.text((25 * (j + 1) + 20 * j + totalW, 90 * i + 15), textTime, font = fontTime, fill=(255, 255, 255))
                drawImg.text((25 * (j + 1) + 20 * j + totalW, 90 * i + 35), textInput, font = fontText, fill=(255, 255, 255))
                drawImg.text((25 * (j + 1) + 20 * j + totalW, 90 * i + 60), textAns, font = fontText, fill=(255, 255, 255))
                diceNum += 1
                if diceNum >= len(diceData):
                    isContinue = True
                    break
            totalW += nowColumnMaxW
            if isContinue:
                break
        tempImg.save(path + f'/{diceNum}.png')


