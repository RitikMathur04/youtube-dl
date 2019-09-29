import npyscreen, pafy
import json
import requests
from os import system
from time import sleep
import config
from googleapiclient.discovery import build

apikey = "AIzaSyDV5fC8bUA-PJD0qgrE6SpG1ljV_r3J_Nw"

try:
    youtube = build('youtube', 'v3', developerKey=apikey)
except Exception as e:
    print("Error0", e)

req = res = value = None
u = "https://www.youtube.com/watch?v="


class Exitbutton(npyscreen.ButtonPress):
    def whenPressed(self):
        print(1)
        self.parent.parentApp.setNextForm(None)


class Searchbutton(npyscreen.ButtonPress):
    def whenPressed(self):
        print(2)
        self.parent.parentApp.switchForm('loading')


class Backbutton(npyscreen.ButtonPress):
    def whenPressed(self):
        print(3)
        # not working
        self.parent.parentApp.switchForm('MAIN')


class Downloadbutton(npyscreen.ButtonPress):
    def whenPressed(self):
        print(4)
        self.parent.parentApp.switchForm('downloading')


class Search(npyscreen.FormBaseNew):

    def create(self):
        print(5)
        self.input = self.add(npyscreen.TitleText, name='Enter here', color="LABEL")
        # self.add(npyscreen.)
        self.nextrely += 2
        self.searchbutton = self.add(Searchbutton, name="SEARCH", relx=20)

    def afterEditing(self):
        print(6)
        config.inputsearch = self.input
        try:
            print(7)
            req = youtube.search().list(part='snippet', q=config.inputsearch, type='video',
                                        maxResults=20)  # type=video?
            res = req.execute()
            with open('jayati.json', 'w') as f:
                json.dump(res, f)
            print(res)
            # print (req)
            sleep(5)
            self.parentApp.switchForm('display')
        except Exception:
            pass


class Loading(npyscreen.FormBaseNew):
    def create(self):
        print(8)
        self.input = self.add(npyscreen.TitleText, name=" ", value="....Loading Search Results....", color="DANGER",
                              editable=False)
        self.nextrely += 3
        self.exit = self.add(Exitbutton, name='Exit', color="VERYGOOD")
        self.nextrely -= 1
        self.back = self.add(Backbutton, name='Back', relx=10, color="VERYGOOD")

    def afterEditing(self):
        # sleep(1)
        print(9)
        self.parentApp.switchForm('display')


"""class downloading(npyscreen.FormBaseNew):
    def create(self):
        self.display = self.add(npyscreen.TitleText, name =" ", value = "...DOWNLOADING...This may take a while", color="DANGER",editable= False)
        video = pafy.new(config.url)
        stream = video.getbest(preftype= "mp4",ftypestrict= True)
        downloads= config.home + "/Downloads/" + video.title + "." + stream.extension   # file path
        stream.download(filepath= downloads)
    def afterEditing():
"""


class displaysearchresults(npyscreen.MultiLineAction):
    # _contained_widget =
    # _contained_widget_height = 3
    # _entry_type = "SEARCH RESULTS"

    def display_value(self, vl):
        print(10)
        return vl

    def actionHighlighted(self, act_on_this, key_press):
        try:

            print(11)

            self.parent.parentApp.getForm("select").add(TitleText, name=" ", value=act_on_this, editable=False,
                                                        color="CAUTION")
            config.name = act_on_this

            self.parent.parentApp.getForm("select").add(Playbutton, name=" PLAY ", color="VERYGOOD", relx=10)
            self.parent.parentApp.getForm("select").nextrely -= 1
            self.parent.parentApp.getForm("select").add(Downloadbutton, name=" DOWNLOAD ", color="VERYGOOD", relx=15)

            self.parent.parentApp.switchForm("select")
        except Exception as e:
            print("error2", e)


class display(npyscreen.FormBaseNew):
    def create(self):
        try:

            vl = []
            print('content of res: ', res)
            for i in res['items']:
                vl.append(i['snippet']['title'])

            self.add(displaysearchresults, value=vl, show_scroll=True, use_two_lines=True, color="VERYGOOD")
        except Exception as e:
            print("error", e)


class selectoption(npyscreen.Form):
    def create(self):
        print(12)
        pass

    def afterEditing(self):
        print(13)
        self.parentApp.setNextForm(None)


class App(npyscreen.NPSAppManaged):
    def onStart(self):
        self.addForm('MAIN', Search, name='Search')
        # self.addForm('loading', Loading,name="WAIT")
        self.addForm('display', display, name="SEARCH RESULTS")
        self.addForm('select', selectoption)


if __name__ == '__main__':
    Apprun = App().run()