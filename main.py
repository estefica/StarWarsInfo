#Postulante para ROBOTILSA S.A
#By : Estefania Asimbaya

import sys

import random
from PyQt5 import uic, QtWidgets,QtCore,QtGui
from PyQt5.QtWidgets import QApplication, QListWidget, QListWidgetItem, QMenu
from PyQt5.QtCore import QTimer, QTime, QDate,QEvent
import requests
from bs4 import BeautifulSoup
from ventana_secundaria import Ui_SecondWindow

qtCreatorFile = 'Postulante.ui'
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class MyApp(QtWidgets.QMainWindow,Ui_MainWindow):
    def __init__(self):
        super().__init__()
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)


        #LISTWIDGET
        self.listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget.setGeometry(QtCore.QRect(60, 50, 311, 511))
        self.listWidget.setObjectName("listWidget")
        self.listWidget.installEventFilter(self) #activo evento para la lista



        #TIMER
        timer = QTimer(self)
        timer.timeout.connect(self.displayTime)
        timer.start(1000)

        # PUSHBUTTON
        self.Request.clicked.connect(self.agregar_elemento)


    def open_second_window(self):
        self.SecondW = QtWidgets.QMainWindow()
        self.ui = Ui_SecondWindow()
        self.ui.setupUi(self.SecondW)
        self.SecondW.show()

    def eventFilter(self, source, event):

        if event.type() == QEvent.ContextMenu and source is self.listWidget:
            menu = QMenu()
            menu.addAction('Informacion adicional')

            if menu.exec_(event.globalPos()):
                item = source.itemAt(event.pos())
                self.open_second_window()
                index = self.n_items.index(item.text())


                self.ui.height_d.setText(self.complete_information[index][1])
                self.ui.mass_d.setText(self.complete_information[index][2])
                self.ui.hair_color_d.setText(self.complete_information[index][3])
                self.ui.skin_color_d.setText(self.complete_information[index][4])
                self.ui.eye_color_d.setText(self.complete_information[index][5])
                self.ui.birth_year_d.setText(self.complete_information[index][6])
                self.ui.gender_d.setText(self.complete_information[index][7])

            return True
        return super().eventFilter(source, event)
    def agregar_elemento(self):
        # ACUMULADOR INFORMACION
        char_information = []
        self.check_repeated_item = []
        self.complete_information = {}

        #RANDOM 10 NOMBRES
        self.listWidget.clear()

        for char_numbers in range (10): #number of characters required
            url = self.random_number()
            page = requests.get(url)

            soup = BeautifulSoup(page.content, 'html.parser')
            dict_soup = soup.prettify()
            dict_soup = dict_soup[1: -1]
            new_s = dict_soup.split('\",\"')

            for element in range(8): # We chose just de util information
                name_ch = new_s[element].split(':')
                name_ch = name_ch[1][1:]
                char_information.append(name_ch)

            self.complete_information[char_numbers]=char_information
            char_information = []
        self.n_items = self.names_item(self.complete_information)

        font = QtGui.QFont()
        font.setPointSize(15)
        self.listWidget.setFont(font)
        self.listWidget.addItems(self.n_items)



    def names_item(self, c):
        items= []
        for x in range(10):
            item = c[x][0]
            items.append(item)
        return items


    def random_number(self):
        a = 1

        while a==1:
            random_number = random.randint(1, 83)
            self.check_repeated_item.append(random_number)
            if self.check_repeated_item.count(random_number) <2:
                url = 'https://swapi.dev/api/people/'+ str(random_number)
                a==0
                break
            if self.check_repeated_item.count(random_number) >= 2:
                a = 1
        a= 1
        return url
    def displayTime(self):
        currentTime = QTime.currentTime()
        currentDate = QDate.currentDate()
        displayText = currentTime.toString('hh:mm:ss')
        displayDate = currentDate.toString('dd/MM/yyyy')
        self.reloj.setText(displayText)
        self.fecha.setText(displayDate)

if __name__=="__main__":
    app =QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    try:
        sys.exit(app.exec_())
    except SystemExit:
        print('Se cerro la ventana, ¡Adios!')
