import bs4
import requests
import pandas as pd
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from database import DataBase
from kivymd.app import MDApp


class CreateAccountWindow(Screen):
    namee = ObjectProperty(None)
    email = ObjectProperty(None)
    password = ObjectProperty(None)

    def submit(self):
        if self.namee.text != "" and self.email.text != "" and self.email.text.count(
                "@") == 1 and self.email.text.count(".") > 0:
            if self.password != "":
                db.add_user(self.email.text, self.password.text, self.namee.text)

                sm.current = "login"
            else:
                invalidForm()
        else:
            invalidForm()

    def login(self):
        sm.current = "login"

    def reset(self):
        self.email.text = ""
        self.password.text = ""
        self.name.text = ""


class LoginWindow(Screen):
    email = ObjectProperty(None)
    password = ObjectProperty(None)

    def loginBtn(self):
        if db.validate(self.email.text, self.password.text):
            ProfileWindow.current = self.email.text
            self.reset()
            sm.current = "main"
        else:
            invalidLogin()

    def createBtn(self):
        self.reset()
        sm.current = "create"

    def reset(self):
        self.email.text = ""
        self.password.text = ""


class MainWindow(Screen):
    def btn(self):
        sm.current = "login"

    def btn1(self):
        sm.current = "data"

    def btn2(self):
        sm.current = "profile"


class DataWindow(Screen):
    def homebtn(self):
        sm.current = "main"

    def mapbtn(self):
        sm.current = "map"

    def infobtn(self):
        sm.current = "info"

    def showbtn(self):
        url = "https://radioaktywnosc-pomiary.umcs.lublin.pl/wykresy_front/wykresy_podstawowe/wykresy.php"
        page = requests.get(url)

        soup = bs4.BeautifulSoup(page.content, "lxml")

        results = soup.find("h4")
        contamination = soup.find("div", class_="success-msg")
        table = soup.find("div", class_="tableMoc")

        historical_results = results.text
        historical_constamination = contamination.text
        historical_table = pd.read_html(str(table))
        historical_table = historical_table[0]

        self.ids.rv.data.append({'text': str(historical_results), 'halign': 'center'})
        self.ids.rv.data.append({'text': str(historical_constamination), 'halign': 'center'})
        self.ids.rv.data.append({'text': str(historical_table), 'halign': 'center'})


class InfoWindow(Screen):
    def logout(self):
        sm.current = "data"


class MapWindow(Screen):
    def logout(self):
        sm.current = "data"


class ProfileWindow(Screen):
    n = ObjectProperty(None)
    created = ObjectProperty(None)
    email = ObjectProperty(None)
    current = ""

    def logout(self):
        sm.current = "main"

    def on_enter(self, *args):
        password, name, created = db.get_user(self.current)
        self.n.text = "Account Name: " + name
        self.email.text = "Email: " + self.current
        self.created.text = "Created On: " + created


class WindowManager(ScreenManager):
    pass


def invalidLogin():
    pop = Popup(title='Invalid Login',
                content=Label(text='Invalid username or password.'),
                size_hint=(None, None), size=(400, 400))
    pop.open()


def invalidForm():
    pop = Popup(title='Invalid Form',
                content=Label(text='Please fill in all inputs with valid information.'),
                size_hint=(None, None), size=(400, 400))

    pop.open()


sm = WindowManager()
db = DataBase("users.txt")


class MainApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Teal"
        Builder.load_file("my.kv")
        screens = [LoginWindow(name="login"), CreateAccountWindow(name="create"), MainWindow(name="main"),
                   DataWindow(name="data"), ProfileWindow(name="profile"), MapWindow(name="map"),
                   InfoWindow(name="info")]
        for screen in screens:
            sm.add_widget(screen)
        sm.current = "login"
        return sm


if __name__ == "__main__":
    MainApp().run()
