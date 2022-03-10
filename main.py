from kivy.lang import Builder
from kivy.properties import StringProperty
from datetime import date, datetime
import pandas as pd
from datetime import timedelta
from kivymd.app import MDApp
from kivymd.uix.list import IRightBodyTouch, OneLineAvatarIconListItem, ThreeLineListItem
from kivy.clock import Clock
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from io import StringIO
gauth = GoogleAuth()
# Create GoogleDrive instance with authenticated GoogleAuth instance.
drive = GoogleDrive(gauth)
def get_table_pandas(table):
    file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
    for file in file_list:
        if file['title'] == table:
            new_file = drive.CreateFile({'title': file['title'], 'id': file['id']})
            new_file = pd.read_csv(StringIO(new_file.GetContentString()))
            return new_file


def loaz():
    from datetime import date
    import datetime
    import hdate
    hb = str(hdate.HDate(datetime.date(date.today().year, date.today().month, date.today().day)
                         , hebrew=True))
    hb = str(hb)
    hb = hb.replace('"',"")
    hb = hb.replace("'", "")
    return hb
print(loaz())

KV = f'''
<OneLineAvatarIconListItem>:

MDBoxLayout:
    orientation: "vertical"
    MDToolbar:
        title: "רישום התמימים"[::-1]
        id: tlb
        MDLabel:
            text: f"{loaz()[::-1]}"
            font_name:"david"
        MDLabel:
            text: ""

    MDBoxLayout:
        ScrollView:
            MDList:
                id: scroll
        ScrollView:
            MDList:
                id: scroll_tow
        ScrollView:
            MDList:
                id: scroll_three
    MDToolbar:
        id:tlb_tim
        title: "blabla"
        MDLabel:
            id: sb

'''



class MainApp(MDApp):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self.set_toolbar_font_name)
        self.now = datetime.now()

    def set_toolbar_font_name(self, *args):
        self.root.ids.tlb.ids.label_title.font_name = "david"

    def build(self):
        return Builder.load_string(KV)

    def on_start(self):
        Clock.schedule_interval(self.update_clock, 1)
        self.theme_cls.font_styles["david"] = ["david", 15, False, 0]
        df = get_table_pandas("student_data.csv")
        idf = list(df.drop_duplicates(["שיעור"], keep="first", ignore_index=False)["שיעור"])[::-1]
        for i1 in idf:
            srl = [self.root.ids.scroll, self.root.ids.scroll_tow, self.root.ids.scroll_three]
            df2 = df[df["שיעור"] == i1]["שם ומשפחה"]
            for i in df2:
                srl[idf.index(i1)].add_widget(
                    OneLineAvatarIconListItem(text=f"{i[::-1]}", bg_color=[0 , 0 , 0, 0],
                                              on_release=lambda x=i: self.pra(x), font_style="david")

            )
    def pra(self,x):
        if x.bg_color == [0, 0, 0, 0]:
            x.bg_color = [0, 0.95, 0, 0.15]
        else:
            x.bg_color = [0, 0, 0, 0]


    def update_clock(self, *args):
        self.now = self.now + timedelta(seconds=1)
        self.root.ids.sb.text = self.now.strftime('%H:%M:%S')


MainApp().run()