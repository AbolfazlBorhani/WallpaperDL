from concurrent.futures import ThreadPoolExecutor
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtCore import QRect
from PyQt5.QtGui import QPixmap, QMovie
from genericpath import exists
from threading import Thread
from PyQt5.uic import loadUi
from threading import Thread
from requests import get
from getpass import getuser
from random import randint
from shutil import rmtree, move
from PyQt5 import QtWidgets, QtCore, QtGui
from bs4 import BeautifulSoup
from sys import argv
from os import mkdir, getcwd, path

class WallpaperDL(QMainWindow):
    url = ''
    path = ''
    percent = 0
    imagesLinks = []
    firstPath = []

    LoadingGifPath = getcwd() + '\\Img\\Loading.gif'
    tempPath = 'C:\\Users\\JONATHAN\\Desktop\\Temp_Folder\\'
    
    def __init__(self):
        super(WallpaperDL, self).__init__()
        loadUi('UI\\Main.ui', self)

        self.setWindowIcon(QtGui.QIcon(getcwd() + '\\Img\\WHI3PER.ico'))
        self.PATH.insert('C:\\Users\\' + getuser() + '\\Desktop\\Wallpaper\\')
        
        self.SELECT_ALL.clicked.connect(self.setSelectAll)
        self.DESELECT_ALL.clicked.connect(self.setDeselectAll)
            
        self.GO.clicked.connect(self.runProgram)
        self.START_DOWNLOAD.clicked.connect(self.moveImages)
        self.EXIT.clicked.connect(self.exitProgram)

        self.ABOUT.triggered.connect(self.aboutMe)
        
        self.PROGRESS_BAR.setValue(0)
        self.deleteDir()
        self.setLoadingGifsForCheckbox()

    # ============================================================================================== #

    def aboutMe(self):
        loadUi('UI\\About Me.ui', self)
        self.LOGO_LABEL.setPixmap(QPixmap(getcwd() + '\\Img\\WHI3PER.png'))
        self.EMAIL.setPixmap(QPixmap(getcwd() + '\\Img\\Gmail.png'))
        self.GITHUB.setPixmap(QPixmap(getcwd() + '\\Img\\Github.png'))
        self.LINKDIN.setPixmap(QPixmap(getcwd() + '\\Img\\Linkdin.png'))
        self.TELEGRAM.setPixmap(QPixmap(getcwd() + '\\Img\\Telegram.png'))
        
    # ============================================================================================== #

    def clearVariables(self):
        self.url = ''
        self.path = ''
        self.percent = 0
        self.imagesLinks.clear()
        self.firstPath.clear()

    # ============================================================================================== #

    def getInputs(self):
        self.url = self.URL.text()
        self.path = self.PATH.text()

    # ============================================================================================== #

    def makeFolder(self):
        self.deleteDir()
        mkdir(self.path)
        
    # ============================================================================================== #
    
    def deleteDir(self):
        if path.exists(self.path):
            rmtree(self.path)
            
        if path.exists(self.tempPath):
            rmtree(self.tempPath)
        
    # ============================================================================================== #

    def webProcess(self):
        page = get(self.url)
        soup = BeautifulSoup(page.text, 'html.parser')

        self.imagesLinks = [link.get('href') for link in soup.find_all('link')]

        self.percent = (100 / len(self.imagesLinks))

        # =============================================================== #
        
        if not path.exists(self.tempPath):
            mkdir(self.tempPath)

        # =============================================================== #

        threads = []

        for i in range(len(self.imagesLinks)):
            temp = Thread(target = self.downloadImage, args = [self.imagesLinks[i], f'R{i}.jpg'])
            temp.start()
            threads.append(temp)

        for item in threads:
            item.join()
        
    # ============================================================================================== #

    def downloadImage(self, link, name):
        with open(self.tempPath + name, 'wb') as file:
            try:
                file.write(get(link).content)
            except:
                pass

    # ============================================================================================== #

    
    # ============================================================================================== #

    def setLoadingGifsForCheckbox(self):
        self.movie = QMovie(self.LoadingGifPath)
        
        labelsList = [self.L1,  self.L2,  self.L3,  self.L4, 
                      self.L5,  self.L6,  self.L7,  self.L8, 
                      self.L9,  self.L10, self.L11, self.L12, 
                      self.L13, self.L14, self.L15, self.L16]
        
        for item in labelsList:
            item.setMovie(self.movie)
        
        self.movie.start()
    
    # ============================================================================================== #

    def setWallpaperImagesForCheckbox(self):
        self.movie.stop()
        index = 0
        
        for i in range(16):
            result = f'{self.tempPath}R{randint(8, len(self.imagesLinks))}.jpg'

            if not result in self.firstPath:
                self.firstPath.append(result)

        labelsList = [self.L1,  self.L2,  self.L3,  self.L4, 
                      self.L5,  self.L6,  self.L7,  self.L8, 
                      self.L9,  self.L10, self.L11, self.L12, 
                      self.L13, self.L14, self.L15, self.L16]

        try:
            for item in labelsList:
                item.clear()
                item.setPixmap(QPixmap(self.firstPath[index]))
                index += 1
            
            self.show()
        except:
            print('Error in setCheckboxIcon():\n- Out of range.\n- image not found.\n')
        
    # ============================================================================================== #
    
    def setSelectAll(self):
        self.selectOrDeselectAllBox(True)
        
    # ============================================================================================== #
    
    def setDeselectAll(self):
        self.selectOrDeselectAllBox(False)
    
    # ============================================================================================== #
    
    def selectOrDeselectAllBox(self, FLAG):
        
        if FLAG:
            self.DESELECT_ALL.setChecked(False)
            flag = True
        else:
            self.SELECT_ALL.setChecked(False)
            flag = False
        
        checkBoxsList = [self.CHECK_BOX_1, self.CHECK_BOX_2,  self.CHECK_BOX_3,  self.CHECK_BOX_4, 
                        self.CHECK_BOX_5,  self.CHECK_BOX_6,  self.CHECK_BOX_7,  self.CHECK_BOX_8,
                        self.CHECK_BOX_9,  self.CHECK_BOX_10, self.CHECK_BOX_11, self.CHECK_BOX_12,
                        self.CHECK_BOX_13, self.CHECK_BOX_14, self.CHECK_BOX_15, self.CHECK_BOX_16]
        
        for item in checkBoxsList:
            item.setChecked(flag)

    # ============================================================================================== #
    
    def moveImages(self):
        percent = 0
        index = 0
        
        checkBoxsList = [self.CHECK_BOX_1, self.CHECK_BOX_2,  self.CHECK_BOX_3,  self.CHECK_BOX_4, 
                        self.CHECK_BOX_5,  self.CHECK_BOX_6,  self.CHECK_BOX_7,  self.CHECK_BOX_8,
                        self.CHECK_BOX_9,  self.CHECK_BOX_10, self.CHECK_BOX_11, self.CHECK_BOX_12,
                        self.CHECK_BOX_13, self.CHECK_BOX_14, self.CHECK_BOX_15, self.CHECK_BOX_16]
        
        try:
            for item in checkBoxsList:
                if item.isChecked():
                    temp = self.firstPath[index]
                    move(temp, self.path + temp[temp.rfind('\\') + 1:])
                    percent += 1
                    index += 1
        except:
            print('Error in move_images():\n- Out of range.\n- image not found.\n')
                
        percent = (100 // percent)
        
        while percent <= 100:
            percent += percent
            
            if percent > 100:
                self.PROGRESS_BAR.setValue(100)    
                break
            
            self.PROGRESS_BAR.setValue(percent)
            
        rmtree(self.tempPath)
        
    # ============================================================================================== #

    def runProgram(self):
        self.clearVariables()
        self.getInputs()
        self.makeFolder()
        self.webProcess()
        self.setWallpaperImagesForCheckbox()
            
    # ============================================================================================== #

    def exitProgram(self):
        exit()

    # =============================================================================================== #