import sys
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import (QTextBrowser, QLabel, QMessageBox, QLineEdit, QApplication, QPushButton, QAction, qApp, QMenu, QDesktopWidget)
from PyQt5.QtGui import QIcon, QFont
from sendMail import SendMailDialog as SendMailDialog
from login import LoginDialog as LoginDialog
from reciever import Pop3Client
from SMTP import SmtpClient


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.pop3 = Pop3Client(self)
        self.smtp = SmtpClient(self)

        self.accountInfo = '' # mail adress : self.accountInfo["login"]  password : self.accountInfo["password"]
    
        # Shortcut to exit Ctrl + Q
        exitAction = QAction(QIcon('exit.png'), '&Exit', self)        
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(qApp.quit)

        self.statusbar = self.statusBar()

        # Menu Bar
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAction)

        # Sub Menu
        importMenu = QMenu('Import', self)
        importFileAction = QAction('Import file', self) 
        importMenu.addAction(importFileAction)
        
        newMailAction = QAction('New Mail', self)
        
        fileMenu.addAction(newMailAction)
        newMailAction.triggered.connect(self.sendMail)       

        fileMenu.addMenu(importMenu)
        

        # Status Bar
        self.statusBar().showMessage('Ready')

        # Login Button
        self.loginButton = QPushButton('Log in', self)
        self.loginButton.setToolTip('Click to log in')
        self.loginButton.setObjectName("loginButton")
        self.loginButton.move(425,300)
        self.loginButton.resize(200,50)
        self.loginButton.setStyleSheet("background-color: green; color: white; font-size: 20px;")

        self.loginButton.clicked.connect(self.login)    

        # Number of mails
        self.labelNumEmails = QLabel(self)
        self.labelNumEmails.move(900, 700)
        self.labelNumEmails.hide()
        self.labelNumEmails.setText("Number of Mails") 
 
        self.textBrowserNumEmails = QTextBrowser(self)
        self.textBrowserNumEmails.move(900,725)
        self.textBrowserNumEmails.setObjectName("textBrowserNumEmails")
        self.textBrowserNumEmails.hide()

        # Send Mail Button
        self.sendMailButton = QPushButton('Send Mail', self)
        self.sendMailButton.setStyleSheet("background-color: green; color: white;")
        self.sendMailButton.setToolTip('Click to send mail')
        self.sendMailButton.move(100,25)
        self.sendMailButton.clicked.connect(self.sendMail)     
        self.sendMailButton.hide() 

        # Logout button
        self.logoutButton = QPushButton('Log out', self)
        self.logoutButton.setStyleSheet("background-color: red; color: white;")
        self.logoutButton.move(900, 25) 
        self.logoutButton.setObjectName("logoutButton")
        self.logoutButton.hide()
        self.logoutButton.clicked.connect(self.logout)  

        # Mails
        self.listWidgetEmails = QtWidgets.QListWidget(self)
        self.listWidgetEmails.setGeometry(QtCore.QRect(60, 90, 900, 600))
        self.listWidgetEmails.setObjectName("listWidgetEmails")
        self.listWidgetEmails.itemClicked.connect(self.showEmail)
        self.listWidgetEmails.hide()

        # Show mail 
        self.textBrowserShowMail = QtWidgets.QTextBrowser(self)
        self.textBrowserShowMail.setGeometry(QtCore.QRect(60, 90, 900, 600))
        self.textBrowserShowMail.setFontPointSize(20)
        self.textBrowserShowMail.setObjectName("textBrowserShowMail")
        self.textBrowserShowMail.hide()

        # Button to go back to main window
        self.backToMainButton = QPushButton('Back', self)
        self.backToMainButton.move(400, 25)
        self.backToMainButton.hide()
        self.backToMainButton.clicked.connect(self.goBack)

        # Button to delete email
        self.deleteMailButton = QPushButton('Delete', self)
        self.deleteMailButton.move(500, 25)
        self.deleteMailButton.hide()
        self.deleteMailButton.clicked.connect(self.deleteMailClicked)

        # Button to reset deletion marks
        # self.resetMailButton = QPushButton('Reset marks', self)
        # self.resetMailButton.move(700, 25)
        # self.resetMailButton.hide()
        # self.resetMailButton.clicked.connect(self.pop3.resetDeletion)
        
        # Refresh mails
        self.refreshButton = QPushButton('Refresh', self)
        self.refreshButton.setStyleSheet("background-color: green; color: white;")
        self.refreshButton.move(0,25)
        self.refreshButton.hide()
        self.refreshButton.clicked.connect(self.pop3.relogin)

        # Main window configurations
        self.resize(1024, 768)
        self.center()
        self.setWindowTitle('CS3800 Email Client')
        self.setWindowIcon(QIcon('test.png')) 
        self.setStyleSheet("background-color: white;")
        self.show()

    # Log in POP3
    def login(self):
        sender = self.sender()
        login = LoginDialog(parent=self, pop3=self.pop3, parentWindow=main)
        self.loginButton.hide()
        login.show()
        login.setStyleSheet("background-color: white;")
        if not login.exec_(): 
            self.statusBar().showMessage('Log in cancelled')
    
    # Shows send mail dialog
    def sendMail(self):
        sendMail = SendMailDialog(smtp=self.smtp, parent=main)
        sendMail.exec_()
        sendMail.show()

    def logout(self):
        self.logoutButton.hide()
        self.loginButton.show()
        self.pop3.quit()
        self.loginButton.setText('Log in')
        self.listWidgetEmails.clear()
        self.listWidgetEmails.hide()
        self.refreshButton.hide()
        self.statusBar().showMessage('Logged out')
        self.labelNumEmails.hide()
        self.textBrowserNumEmails.setText('0')
        self.textBrowserNumEmails.hide()
        self.textBrowserShowMail.hide()
        self.refreshButton.hide()
        self.backToMainButton.hide()
        self.deleteMailButton.hide()
        self.sendMailButton.hide()
        #self.resetMailButton.hide()

    
    # Asking to quit
    def closeEvent(self, event):
        # Message box
        reply = QMessageBox.question(self, 'Exit',"Are you ready to quit?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()    
  

    # To center window on start
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def toggleMenu(self, state):
        if state:
            self.statusbar.show()
        else:
            self.statusbar.hide()

    def showEmail(self):
        self.pop3.retrieveMail(self.listWidgetEmails.currentItem().text(), self)

        self.listWidgetEmails.hide()
        self.textBrowserShowMail.show()
        self.backToMainButton.show()
        self.deleteMailButton.show()
    
    def goBack(self):
        self.listWidgetEmails.show()
        self.textBrowserShowMail.hide()
        self.backToMainButton.hide()
        self.deleteMailButton.hide()

    def deleteMailClicked(self):
        deleteSuccess = self.pop3.deleteEmail(self.listWidgetEmails.currentItem().text())
        if deleteSuccess:
            # Removes the mail from the list widget
            self.listWidgetEmails.takeItem(self.listWidgetEmails.currentRow())
            self.goBack()
        else: 
            QMessageBox.warning(self, 'Error', 'Error while deleting the email')
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = MainWindow()
    main.show()

    sys.exit(app.exec_())