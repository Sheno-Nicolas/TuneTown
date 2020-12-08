from PyQt5.QtWidgets import QMessageBox, QComboBox, QLineEdit, QLabel, QPushButton, QRadioButton, QVBoxLayout, QHBoxLayout, QApplication, QWidget
from PyQt5 import QtGui
from PyQt5.QtGui import QColor
import sys
from PyQt5 import QtCore
import main

class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.title = "TuneTown"
        self.top = 0
        self.left = 0
        self.width = 560
        self.height = 80
        self.first = False
        self.best = False

        self.InitWindow()
        
    #Initializing the window
    def InitWindow(self):
        #Creating widgits and interfacce
        artist_line_edit = QLineEdit()

        hour_line_edit = QLineEdit()
        minute_line_edit = QLineEdit()
        second_line_edit = QLineEdit()

        random_label = QPushButton("Random Playlist!")
        user_input_label = QPushButton("Make My Own!")
        alg_select_label = QLabel("Select an Algorithm:")
        first_fit_button = QRadioButton("First Fit")
        best_fit_button = QRadioButton("Best Fit")
        both_button = QRadioButton("Both")
        submit_button = QPushButton("Generate Playlist!")

        vBox = QVBoxLayout()
        vBox.addWidget(QLabel("MUSIC TIMER"))

        vBox.addWidget(alg_select_label)
        hBox2 = QHBoxLayout()
        hBox2.addWidget(first_fit_button)
        hBox2.addWidget(best_fit_button)
        hBox2.addWidget(both_button)
        #hBox2.addStretch(1)
        vBox.addLayout(hBox2)

        hChoice = QHBoxLayout()
        hChoice.addWidget(random_label)
        hChoice.addWidget(user_input_label)
        vBox.addLayout(hChoice)
        # vBox.addWidget(QLabel("Artist(s): "))
        # vBox.addWidget(artist_line_edit)
            
        # vBox.addWidget(QLabel("How long should the playlist be?"))

        # hBox = QHBoxLayout()
        # hBox.addWidget(hour_line_edit)
        # hBox.addWidget(QLabel("hour(s)"))
        # hBox.addWidget(minute_line_edit)
        # hBox.addWidget(QLabel("minute(s)"))
        # hBox.addWidget(second_line_edit)
        # hBox.addWidget(QLabel("second(s)"))
        # vBox.addLayout(hBox)

        #vBox.addWidget(submit_button)
        
        self.setLayout(vBox)
        
        #Changing the design and color of our GUI
        palette = QtGui.QPalette()
        palette.setColor(QtGui.QPalette.Window, QColor("#e7daf9"))
        palette.setColor(QtGui.QPalette.WindowText, QColor("#000000"))
        palette.setColor(QtGui.QPalette.Base, QColor("#ffffff"))
        palette.setColor(QtGui.QPalette.Text, QtCore.Qt.black)
        palette.setColor(QtGui.QPalette.Button, QtCore.Qt.black)
        palette.setColor(QtGui.QPalette.ButtonText, QtCore.Qt.black)
        palette.setColor(QtGui.QPalette.Midlight, QtCore.Qt.white)
        self.setPalette(palette)
        
        #More items added to interface
        make_playlist = QLabel("Want to add your playlist to Spotify?")
        yes = QRadioButton("Yes")
        no = QRadioButton("No")
        hBox3 = QHBoxLayout()
        hBox3.addWidget(yes)
        hBox3.addWidget(no)
        
        #On click of make_own button we go to the make_own function which adds to the interface for that functionality
        user_input_label.clicked.connect(lambda: make_own())
        #Taking in input from user to make their own playlist
        def make_own():
            vBox.addWidget(QLabel("Artist(s): "))
            vBox.addWidget(artist_line_edit)
                
            vBox.addWidget(QLabel("How long should the playlist be?"))

            hBox = QHBoxLayout()
            hBox.addWidget(hour_line_edit)
            hBox.addWidget(QLabel("hour(s)"))
            hBox.addWidget(minute_line_edit)
            hBox.addWidget(QLabel("minute(s)"))
            hBox.addWidget(second_line_edit)
            hBox.addWidget(QLabel("second(s)"))
            vBox.addLayout(hBox)

            vBox.addWidget(submit_button)
        #main object
        mainObj = main.mainClass()
        #User submitting their inputs 
        submit_button.clicked.connect(lambda: hold_user_input())
        #taking in user input and putting it to use
        def hold_user_input():
            #allows for input of multiple artists
            artist_list = artist_line_edit.text().split(", ")
            set(artist_list)

            #artist_list = set([artist_line_edit.text()])
            mainObj.setValues(artist_list, hour_line_edit.text(), minute_line_edit.text(), second_line_edit.text())
            #checks if first fit or best fit is clicked
            self.first = first_fit_button.isChecked()
            self.best = best_fit_button.isChecked()
            if both_button.isChecked() :
                self.first = True
                self.best = True

            print_songs = mainObj.generate(self.first, self.best)

            # POP OUT BOX TO PRINT OUT OUTPUT
            alert = QMessageBox()
            alert.setText(print_songs) 
            alert.exec_()

            vBox.addWidget(make_playlist)
            vBox.addLayout(hBox3)
        
        
        #Taking in more input from the user
        ask_for_addy = QLabel("Please enter the authorization token:")
        input_addy = QLineEdit()
        ask_for_name = QLabel("What would you like to name your playlist(s)?")
        first_name = QLabel("First-Fit Playlist Name")
        first_input = QLineEdit()
        best_name = QLabel("Best-Fit Playlist Name")
        best_input = QLineEdit()
        submit2 = QPushButton("Submit")
        hBox_first = QHBoxLayout()
        hBox_first.addWidget(first_name)
        hBox_first.addWidget(first_input)
        hBox_best = QHBoxLayout()
        hBox_best.addWidget(best_name)
        hBox_best.addWidget(best_input)
        
        #Random functionality 
        random_label.clicked.connect(lambda: make_random())
        def make_random():
            self.first = first_fit_button.isChecked()
            self.best = best_fit_button.isChecked()
            if both_button.isChecked() :
                self.first = True
                self.best = True
            #Calls random function from main
            mainObj.randomValues()

            print_songs = mainObj.generate(self.first, self.best)

            # POP OUT BOX 
            alert = QMessageBox()
            alert.setText(print_songs) 
            alert.exec_()

            vBox.addWidget(make_playlist)
            vBox.addLayout(hBox3)

        yes.toggled.connect(lambda: set_up_playlist())
        no.toggled.connect(self.close) #Pressing no closes program

        def set_up_playlist():
            import spotify
            #vBox.addWidget(ask_for_addy)
            #vBox.addWidget(input_addy)

            vBox.addWidget(ask_for_name)
            if self.first:
                vBox.addLayout(hBox_first)

            if self.best:
                vBox.addLayout(hBox_best)

            vBox.addWidget(submit2)
        
        submit2.clicked.connect(lambda: done())
        #Imports playlist to spotify 
        def done():
            # import spotify
            # spotify.spotify_token = input_addy.text()
            if self.first & self.best:
                mainObj.make_first_playlist(first_input.text())
                mainObj.make_best_playlist(best_input.text())
            elif self.first:
                mainObj.make_first_playlist(first_input.text())
            else:
                mainObj.make_best_playlist(best_input.text())

            vBox.addWidget(QLabel("ALL DONE!"))
        
        
        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.width, self.height)
        self.show()

#Starts up actual window  
app = QApplication(sys.argv)
window = Window()
sys.exit(app.exec())
