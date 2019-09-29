from googleapiclient.discovery import build
import npyscreen, pafy

apikey = "AIzaSyDV5fC8bUA-PJD0qgrE6SpG1ljV_r3J_Nw"

youtube = build('youtube', 'v3', developerKey=apikey)
req = youtube.search().list(part='snippet', q='gone,gone,gone', type='video', maxResults=15)
res = req.execute()
u = "https://www.youtube.com/watch?v="

k = []
for i in res['items']:
    k.append(i['id']['videoId'])

urllist = []
for i in k:
    uu = u + i
    video = pafy.new(uu)
    urllist.append(video.duration)


class book(npyscreen.Form):
    def create(self):
        pass

    def afterEdting(self):
        self.parentApp.setNextForm(None)


class ListBooks(npyscreen.MultiLineAction):
    # _contained_widgets = Display
    # _contained_widget_height = 2
    def display_value(self, vl):
        return (vl)

    def actionHighlighted(self, act_on_this, key_press):
        self.parent.parentApp.getForm('BOOK').add(npyscreen.TitleText, name="helo", value=act_on_this, editable=False,
                                                  hidden=False)
        self.parent.parentApp.switchForm('BOOK')


class display(npyscreen.Form):
    def create(self):
        vl = []
        j = 0
        for i in res['items']:
            vl.append(i['snippet']['title'])

        self.add(ListBooks, values=vl, show_scroll=True, use_two_lines=True, color="VERGOOD")


class App(npyscreen.NPSAppManaged):
    def onStart(self):
        self.addForm('MAIN', display)
        self.addForm('BOOK', book)


if __name__ == '__main__':
    Apprun = App().run()

