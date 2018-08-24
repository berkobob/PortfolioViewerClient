import sys
import requests
from PyQt5.QtWidgets import QApplication as App
from PyQt5.QtWidgets import QWidget as Window
from PyQt5.QtWidgets import QPushButton as Button
from PyQt5.QtWidgets import QLabel as Label
from PyQt5.QtWidgets import QHBoxLayout as HBox
from PyQt5.QtWidgets import QVBoxLayout as VBox

url = {'new': "http://localhost:5000/api/new",
       'new1': "http://devserver:5000/api/new",
       'add': "http://localhost:5000/api/add",
       'add1': "http://devserver:5000/api/add",
       'api1': "http://devserver:5000/api/",
       'api': "http://localhost:5000/api/",
       "ports": "http://localhost:5000/api/ports",
       'head': {"Content-Type": "application/json"},
       'stock': ['port', 'ticker', 'shares', 'price', 'exchange',],
       'port': ['PORT', 'VALUE', 'DELTA'],
       'stocks': ['PORT', 'NAME', 'TICK', 'QTY', 'PRICE', 'EXCH', 'LAST', 'DELTA', '%', 'STAMP', '£']
       }

class Main_Window(Window):

    def __init__(self):
        super().__init__()
        self.button = Button('Push Me')
        self.label = Label('I have not been clicked')

        hbox = HBox()
        hbox.addStretch()
        hbox.addWidget(self.label)
        hbox.addStretch()

        vbox = VBox()
        vbox.addWidget(self.button)
        vbox.addLayout(hbox)

        reply = requests.get(url['ports'], headers=url['head'])
        if reply.json()['result'] == 'success':
            for port in reply.json()['ports']:
                vbox.addWidget(Label(port[0]))
        else:
            print (reply.text)

        self.setLayout(vbox)
        self.setWindowTitle('Portfolio Viewer')

        self.button.clicked.connect(self.button_click)
        self.show()

    def button_click(self):
        self.label.setText('I have been clicked')

app = App(sys.argv)
app.aboutToQuit.connect(app.deleteLater)
main_window = Main_Window()
sys.exit(app.exec_())