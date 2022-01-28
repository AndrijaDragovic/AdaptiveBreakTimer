from kivy.app import App
# from kivy.lang import Builder
from kivy.properties import StringProperty, ListProperty
# from kivy.uix.boxlayout import BoxLayout
# from kivy.uix.gridlayout import GridLayout
from time import time
from datetime import datetime
# from kivy.core.window import Window
# from kivy.uix.button import Button
# from kivy.uix.relativelayout import RelativeLayout
# from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen  #,NoTransition
from kivy.clock import Clock
from kivy.storage.jsonstore import JsonStore

__version__ = '3.9.9'

store = JsonStore("state.json")




try:
    if store.get('sleepTimer')['value'] > time() - store.get('unixTime')['value']:
        sleep = True
    else:
        sleep = False
except:
    sleep = False


try:
    work = bool(store.get('work')['value'])
except:
    work = False

try:
    oldSleepTime = store.get('sleepTime')['value']
except:
    oldSleepTime = 0.0


try:
    if sleep:
        sleepTime = store.get('sleepTime')['value'] + time() - float(store.get('unixTime')['value'])
        sleepTimer = store.get('sleepTimer')['value'] - time() + float(store.get('unixTime')['value'])
    else:
        sleepTime = store.get('sleepTime')['value'] + store.get('sleepTimer')['value']
        sleepTimer = 0.0
except:
    sleepTime = 0.0
    sleepTimer = 0.0


try:
    fraction = float(store.get('fraction')['value'])
except:
    fraction = 2 / 3

try:
    if not work:
        timer = float(store.get('timer')['value']) - time() + float(store.get('unixTime')['value']) + sleepTime - oldSleepTime
    else:
        timer = float(store.get('timer')['value']) + (time() - float(store.get('unixTime')['value'])) * ((1 - fraction) / fraction)
except:
    timer = 3600

try:
    unixTime = float(store.get('unixTime')['value'])
except:
    unixTime = time()

def stringize(n):
    if n>-1 and n<10:
        return str("0" + str(n))
    else:
        return str(n)

def days(t):
    d = int(t) // 57600
    if d == 1:
        return "1 day,\n"
    elif d == 0:
        return ""
    else:
        return str(d) + " days,\n"




class WindowManager(ScreenManager):
    pass


class SecondWindow(Screen):
    global sleep

    sleepTimerText = StringProperty(str(stringize(int(sleepTimer) // 3600)) + ":" + str(stringize(int(sleepTimer) % 3600 // 60)) + ":" + str(stringize(int(sleepTimer) % 60)))
    if not sleep:
        sleepTimerText = StringProperty("")

    button3Color = ListProperty([0.3, 0, 0.7, 1])
    button3Label = ListProperty([1, 1, 1, 1])

    if not sleep:
        button3Color = ListProperty([0, 0, 0, 0])
        button3Label = ListProperty([0, 0, 0, 0])

    def setFraction(self, widget):
        global fraction
        fraction = eval(widget.text)
        store.put('fraction', value=fraction)

    def setTimer(self, widget):
        global timer
        global futureSeconds
        futureTime = widget.text
        one = True

        alphabet = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t",
                    "u", "v", "w", "x", "y", "z", "š", "đ", "ž", "č", "ć", ".", ",", ":", ";", "-", "/", "!", "?", "'",
                    " "]
        for i in alphabet:
            if len(futureTime.split(i)) == 3:
                if i in futureTime:
                    futureSeconds = futureTime.split(i)[0] * 57600 + futureTime.split(i)[1] * 3600 + futureTime.split(i)[2] * 60
                    one = False
            elif len(futureTime.split(i)) == 2:
                if i in futureTime:
                    futureSeconds = int(futureTime.split(i)[0]) * 3600 + int(futureTime.split(i)[1]) * 60
                    one = False
        if one == True:
            try:
                futureSeconds = int(futureTime) * 3600
            except:
                return


        timer = futureSeconds
        store.put('timer', value=timer)

    def updateSleepTimerText(self):
        global sleepTimer
        self.sleepTimerText = stringize(int(sleepTimer) // 3600) + stringize(int(sleepTimer) % 3600 // 60) + stringize(int(sleepTimer) % 60)


    def setSleep(self, widget):
        global sleep
        global sleepTimer
        global button3Color
        global button3Label
        global work

        sleep = True
        work = False
        one = False
        currentTime = datetime.now()
        futureTime = widget.text

        alphabet = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t",
                    "u", "v", "w", "x", "y", "z", "š", "đ", "ž", "č", "ć", ".", ",", ":", ";", "-", "/", "!", "?", "'",
                    " "]
        for i in alphabet:
            try:
                if futureTime != futureTime.split(i)[0] + futureTime.split(i)[1]:
                    futureTime = [futureTime.split(i)[0], futureTime.split(i)[1]]
                    one = False
                    break
            except:
                one = True
                continue
        try:
            if not one:
                if int(futureTime[0]) > 24 or int(futureTime[1]) > 60:
                    return
                futureSeconds = int(futureTime[0]) * 3600 + int(futureTime[1]) * 60
            else:
                if int(futureTime[0]) > 60:
                    return
                futureSeconds = int(futureTime) * 3600
        except:
            return

        currentSeconds = currentTime.hour * 3600 + currentTime.minute * 60 + currentTime.second

        if futureSeconds > currentSeconds:
            sleepTimer = futureSeconds - currentSeconds
        else:
            sleepTimer = 24 * 3600 - (currentSeconds - futureSeconds)

        #sleepTimer = float((widget.text).split()[0]) * 3600 + float((widget.text).split()[1]) * 60
        self.button3Color = [0.3, 0, 0.7, 1]
        self.button3Label = [1, 1, 1, 1]



    def awaken(self):
        global sleep
        global sleepTimer
        global sleepTime
        global button3Color
        global button3Label
        sleepTimer = 0.0
        sleepTime = 0.0
        sleep = False
        self.button3Color = [0, 0, 0, 0]
        self.button3Label = [0, 0, 0, 0]
        MainWindow.awakenMain(self)

    def awakenWithoutRecursion(self):
        global sleep
        global sleepTimer
        global sleepTime
        global button3Color
        global button3Label
        sleepTimer = 0.0
        sleepTime = 0.0
        sleep = False
        self.button3Color = [0, 0, 0, 0]
        self.button3Label = [0, 0, 0, 0]









class MainWindow(Screen):
    global fraction
    global work
    global SecondWindow
    text = StringProperty("")
    clockColor = ListProperty([0.3, 0, 0.7, 1])
    button4Color = ListProperty([0.3, 0, 0.7, 1])
    button4Label = ListProperty([1, 1, 1, 1])
    button1Label = ListProperty([1, 1, 1, 1])
    button2Label = ListProperty([1, 1, 1, 1])

    button1Color = ListProperty([0, 1, 0, 1])
    button2Color = ListProperty([0.5, 0.5, 0.5, 1])


    def __init__(self, **kwargs):
        super(MainWindow, self).__init__(**kwargs)
        Clock.schedule_interval(self.update, 1 / 30)


    def update(self, s):
        global timer
        global fraction
        global unixTime
        global sleep
        global sleepTimer
        global sleepTime
        global work


        tempTimer = 0

        if not sleep:
            self.clockColor = [1, 1, 1, 1]
            self.text = days(timer) + str(stringize(int(timer) % 57600 // 3600)) + " : " + str(stringize(int(timer) % 3600 // 60)) + " : " + str(stringize(int(timer) % 60)) + "\n\n"
            self.button1Label = [1, 1, 1, 1]
            self.button2Label = [1, 1, 1, 1]
            if timer < 0:
                self.clockColor = [1, 0.1, 0.1, 1]
                tempTimer = - timer
                self.text = "- " + days(tempTimer) + str(stringize(int(tempTimer) % 57600 // 3600)) + " : " + str(stringize(int(tempTimer) % 3600 // 60)) + " : " + str(stringize(int(tempTimer) % 60)) + " " + "\n\n"

        else:
            self.clockColor = [0.3, 0, 0.7, 1]
            self.button4Color = [0.3, 0, 0.7, 1]
            self.button4Label = [1, 1, 1, 1]

            self.text = stringize(int(sleepTimer + 60) // 3600) + " : " + stringize(int(sleepTimer + 60) % 3600 // 60) + "\n\n"

        if not work and not sleep:
            # timer -= 1 / 30
            timer -= time() - unixTime

            sleepTime = 0.0
            sleepTimer = 0.0
            SecondWindow.awaken(self)

            self.button2Color = [1, 0.2, 0.2, 1]
            self.button1Color = [0.5, 0.5, 0.5, 1]
            self.button1Label = [1, 1, 1, 1]
            self.button2Label = [1, 1, 1, 1]

        elif not sleep:
            # timer += (1 - fraction) / fraction / 30
            timer += (1 - fraction) / fraction * (time() - unixTime)
            sleepTime = 0.0
            sleepTimer = 0.0
            SecondWindow.awaken(self)
            self.button2Color = [0.5, 0.5, 0.5, 1]
            self.button1Color = [0, 1, 0, 1]
            self.button1Label = [1, 1, 1, 1]
            self.button2Label = [1, 1, 1, 1]
        else:
            # sleepTimer -= 1/30
            # sleepTime += 1/30
            sleepTimer -= time() - unixTime
            sleepTime += time() - unixTime

            self.button2Color = [0, 0, 0, 0]
            self.button1Color = [0, 0, 0, 0]
            self.button1Label = [0, 0, 0, 0]
            self.button2Label = [0, 0, 0, 0]
            SecondWindow.updateSleepTimerText(self)
            if sleepTimer <= 0:
                sleep = False
        #self.text = str(int(timer) % 86400 // 3600) + " : " + str(int(timer) % 3600 // 60) + " : " + str(int(timer) % 60)
        unixTime = time()
        store.put('unixTime', value=unixTime)
        store.put('timer', value=timer)
        store.put('work', value=work)
        store.put('sleepTimer', value=sleepTimer)
        store.put('sleepTime', value=sleepTime)


    def tapButton1(self):
        global work
        global sleep
        if sleep:
            return
        self.button1Color = [0, 1, 0, 1]
        self.button2Color = [0.5, 0.5, 0.5, 1]
        work = True
        store.put('work', value=True)

    def killButtons(self):
        self.button1Color = [0, 0, 0, 0]
        self.button2Color = [0, 0, 0, 0]
        self.button1Label = [0, 0, 0, 0]
        self.button2Label = [0, 0, 0, 0]


    def tapButton2(self):
        global sleep
        if sleep:
            return
        global work
        self.button2Color = [1, 0.2, 0.2, 1]
        self.button1Color = [0.5, 0.5, 0.5, 1]
        work = False
        store.put('work', value=False)

    def awakenMain(self):
        SecondWindow.awakenWithoutRecursion(self)
        self.button4Color = [0, 0, 0, 0]
        self.button4Label = [0, 0, 0, 0]

    def setSleepMain(self):
        self.button4Color = [0.3, 0, 0.7, 1]
        self.button4Label = [1, 1, 1, 1]
        self.button1Color = [0, 0, 0, 0]
        self.button2Color = [0, 0, 0, 0]
        self.button1Label = [0, 0, 0, 0]
        self.button2Label = [0, 0, 0, 0]

    def awakenMainFromSecond(self):
        self.button4Color = [0, 0, 0, 0]
        self.button4Label = [0, 0, 0, 0]


class breaktimerApp(App):
    pass


if __name__ == "__main__":
    breaktimerApp().run()
