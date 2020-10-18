from tkinter import Tk, Label, Button, Entry, StringVar
from tkinter.filedialog import askdirectory
from os import getcwd
import json
from  configparser import ConfigParser

import rollDice
import draw

class App:
    def __init__(self):
        self.tk = Tk()
        self.tk.title('会画图的骰娘')
        self.workPath = getcwd()
        self.config = ConfigParser()
        self.config.read(getcwd() + '/config.ini')

        self.workPath = self.config.get('default', 'nowWorkPath') if self.config.get('default', 'nowWorkPath') != '0' else self.workPath
        self.tk.bind('<Return>', self.enterRoll)
        self.initUI()

    def initUI(self):
        self.labelBeforeInput = Label(self.tk, text = '.r')
        self.labelBeforeInput.grid(row = 0, column = 0)
        self.labelMaxLine = Label(self.tk, text = '最大行数')
        self.labelMaxLine.grid(row = 3, column = 0)
        self.entryMaxLine = Entry(self.tk)
        self.entryMaxLine.insert(0, self.config.get('default', 'maxLine'))
        self.entryMaxLine.grid(row = 3, column = 1)
        self.labelMaxColumn = Label(self.tk, text = '最大列数')
        self.labelMaxColumn.grid(row = 3, column = 2)
        self.entryMaxColumn = Entry(self.tk)
        self.entryMaxColumn.insert(0, self.config.get('default', 'maxColumn'))
        self.entryMaxColumn.grid(row = 3, column = 3)
        self.entryInput = Entry(self.tk)
        self.entryInput.grid(row = 0, column = 1, columnspan = 3)
        self.buttonRoll = Button(self.tk, text = 'Roll', command = self.roll)
        self.buttonRoll.grid(row = 1, column = 0, columnspan = 4)
        self.buttonSelPath = Button(self.tk, text = '选择工作路径', command = self.selectPath)
        self.buttonSelPath.grid(row = 4, column = 0, columnspan = 2)
        self.buttonDraw = Button(self.tk, text = '开始绘图', command = self.drawDicePic)
        self.buttonDraw.grid(row = 4, column = 2, columnspan = 2)

        self.stringAns = StringVar()
        self.labelAns = Label(self.tk, textvariable = self.stringAns)
        self.labelAns.grid(row = 2, column = 0, columnspan = 4)

    def roll(self):
        tempText = self.entryInput.get()
        tempText = tempText.split('d')
        try:
            times = int(tempText[0])
            maxNum = int(tempText[1])
        except:
            pass
        ans = rollDice.roll(times, maxNum)
        textAns = '骰出了({0}d{1} = {2}) = {3}'.format(ans['times'], ans['max'], ans['eachNum'], ans['sumNum'])
        self.stringAns.set(textAns)
        with open(self.workPath + '/diceData.json', 'a+') as f:
            f.seek(0, 0)
            existData = f.read()
            if existData == '':
                tempData = []
            else:
                tempData = json.loads(existData)['dice']
            tempData.append(ans)
        with open(self.workPath + '/diceData.json', 'w') as f:
            f.write(json.dumps({'dice' : tempData}, sort_keys=True, indent=4, separators=(',', ': ')))

    def enterRoll(self, ev = None):
        self.roll()

    def selectPath(self):
        self.workPath = askdirectory(initialdir = self.workPath)
        self.config.set('default', 'nowWorkPath', self.workPath)
        with open(getcwd() + '/config.ini', 'w') as f:
            self.config.write(f)

    def drawDicePic(self):
        self.config.set('default', 'maxLine', self.entryMaxLine.get())
        self.config.set('default', 'maxColumn', self.entryMaxColumn.get())
        with open(getcwd() + '/config.ini', 'w') as f:
            self.config.write(f)
        draw.drawDiceResult(self.workPath, int(self.entryMaxLine.get()), int(self.entryMaxColumn.get()))

    def mainloop(self):
        self.tk.mainloop()

if __name__ == '__main__':
    app = App()
    app.mainloop()