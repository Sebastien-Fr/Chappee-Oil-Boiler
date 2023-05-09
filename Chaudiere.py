# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
import time
from PyQt5 import QtCore,QtWidgets,QtGui
from PyQt5.QtCore import pyqtSlot,QTime,QTimer
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QMainWindow,QFrame,QApplication, QAction, qApp, QTextEdit, QPushButton,QHBoxLayout, QWidget, QVBoxLayout,QToolTip, QLineEdit, QLabel, QCheckBox, QComboBox
import sys
import threading
import glob
from pymodbus.server.asynchronous  import StartTcpServer
from pymodbus.datastore import ModbusSequentialDataBlock
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
from twisted.internet.task import LoopingCall
from pymodbus.pdu import ModbusRequest
import logging
from logging.handlers import RotatingFileHandler
import datetime
from datetime import timedelta
from datetime import date
from datetime import datetime

#############################      logger    ################################
logger = logging.getLogger('Chaudiere')
logger.setLevel(logging.DEBUG)
fh= RotatingFileHandler('Chaudiere.log',maxBytes=1000000, backupCount=5)
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)

################################     GUI     ###################################
class ApplicationWindow(QMainWindow):
    init=True
    def __init__(self):
         super().__init__()
         self.setupUi()
         
    ########## BuTTON VALUES to PLC  ##############
    logger.info('start GUI')     
    def WriteState(self,button):
            logger.info(button)
            if button=="ECS":
                if self.state[0]==1:
                    self.state[0]=0
                    self.ButtonECS.setStyleSheet("QPushButton""{""background-color : white;""}")
                else:
                    self.state[0]=1
                    self.ButtonECS.setStyleSheet("QPushButton""{""background-color : green;" "}")
                logger.info(self.state[0]) 
            if button=="CHAUFF":
                if self.state[1]==1:
                    self.state[1]=0
                    self.ButtonChauff.setStyleSheet("QPushButton""{""background-color : white;""}")
                else:
                    self.state[1]=1
                    self.ButtonChauff.setStyleSheet("QPushButton""{""background-color : green;" "}")
                logger.info(self.state[1])     
            if button=="MARCH":           
                if self.state[2]==1:
                    self.state[2]=0
                    self.ButtonMarche.setStyleSheet("QPushButton""{""background-color : white;""}")
                else:
                    self.state[2]=1
                    self.ButtonMarche.setStyleSheet("QPushButton""{""background-color : green;" "}")
                logger.info(self.state[2])
            if button=="POELE":           
                if self.state[3]==1:
                    self.state[3]=0
                    self.ButtonPoele.setStyleSheet("QPushButton""{""background-color : white;""}")
                else:
                    self.state[3]=1
                    self.ButtonPoele.setStyleSheet("QPushButton""{""background-color : green;" "}")
                logger.info(self.state[3])
                
            api.button=self.state     
    ############# SLIDERS VALUES to PLC ############               
    def writesliders(self,slider):
         logger.info(slider)
         if slider=="slidCsChaufNuit":
            self.sliders[0]=self.slidCsChaufNuit.value()
            logger.info(self.sliders[0])
         if slider=="slidCsChaufJour":
            self.sliders[1]=self.slidCsChaufJour.value()
            logger.info(self.sliders[1])
         if slider=="slidCsECS":
            self.sliders[2]=self.slidCsECS.value()
            logger.info(self.sliders[2])
         if slider=="slidCsArret":
            self.sliders[3]=self.slidCsArret.value()
            logger.info(self.sliders[3])
         if slider=="slidCsMarche":
            self.sliders[4]=self.slidCsMarche.value()
            logger.info(self.sliders[4])
         api.Sliders=self.sliders         
    ############# Time to PLC ######################       
    def writeTime(self,Timer):
         logger.info(Timer)
         if Timer=="timeECSDeb":
            self.Heures[0]=self.timeECSDeb.dateTime().toString('h:m')
            logger.info(self.Heures[0]) 
         if Timer=="timeECSFin":
            self.Heures[1]=self.timeECSFin.dateTime().toString('h:m')
            logger.info(self.Heures[1]) 
         if Timer=="timeChauffJour":
            self.Heures[2]=self.timeChauffJour.dateTime().toString('h:m')
            logger.info(self.Heures[2]) 
         if Timer=="timeChauffNuit":
            self.Heures[3]=self.timeChauffNuit.dateTime().toString('h:m')
            logger.info(self.Heures[3])
         api.Heures=self.Heures     
    ###### GUI   #########
         
    def setupUi(self):
        self.setObjectName("MainWindow")
        self.resize(912, 708)
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 912, 22))
        self.menubar.setObjectName("menubar")
        self.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)
        ###frames###
        self.frame = QFrame(self)
        self.frame.setGeometry(QtCore.QRect(10, 80, 191, 581))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.frame_2 = QtWidgets.QFrame(self.centralwidget)
        self.frame_2.setGeometry(QtCore.QRect(210, 80, 191, 581))
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.frame_3 = QtWidgets.QFrame(self.centralwidget)
        self.frame_3.setGeometry(QtCore.QRect(410, 80, 191, 581))
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.frame_4 = QtWidgets.QFrame(self.centralwidget)
        self.frame_4.setGeometry(QtCore.QRect(610, 80, 281, 581))
        self.frame_4.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")
        ###Time edit###
        self.timeChauffJour = QtWidgets.QTimeEdit(self.frame)
        self.timeChauffJour.setGeometry(QtCore.QRect(10, 60, 151, 41))
        self.timeChauffJour.setObjectName("timeChauffJour")
        self.timeChauffNuit = QtWidgets.QTimeEdit(self.frame)
        self.timeChauffNuit.setGeometry(QtCore.QRect(10, 310, 151, 41))
        self.timeChauffNuit.setObjectName("timeChauffNuit")
        self.timeECSDeb = QtWidgets.QTimeEdit(self.frame_2)
        self.timeECSDeb.setGeometry(QtCore.QRect(30, 310, 141, 41))
        self.timeECSDeb.setObjectName("timeECSDeb") 
        self.timeECSFin = QtWidgets.QTimeEdit(self.frame_2)
        self.timeECSFin.setGeometry(QtCore.QRect(30, 400, 141, 41))
        self.timeECSFin.setObjectName("timeECSFin")
        #buttons
        self.ButtonMarche = QtWidgets.QPushButton(self.frame_3)
        self.ButtonMarche.setGeometry(QtCore.QRect(10, 500, 171, 61))
        self.ButtonMarche.setObjectName("ButtonMarche")
        self.ButtonPoele = QtWidgets.QPushButton(self.frame_3)
        self.ButtonPoele.setGeometry(QtCore.QRect(10, 430, 171, 61))
        self.ButtonPoele.setObjectName("ButtonPoele")
        self.ButtonECS = QtWidgets.QPushButton(self.frame_2)
        self.ButtonECS.setGeometry(QtCore.QRect(10, 500, 171, 61))
        self.ButtonECS.setObjectName("ButtonECS")
        self.ButtonChauff = QtWidgets.QPushButton(self.frame)
        self.ButtonChauff.setGeometry(QtCore.QRect(10, 500, 171, 61))
        self.ButtonChauff.setObjectName("ButtonChauff")
        #sliders
        self.slidCsArret = QtWidgets.QSlider(self.frame_3)
        self.slidCsArret.setGeometry(QtCore.QRect(10, 230, 160, 22))
        self.slidCsArret.setOrientation(QtCore.Qt.Horizontal)
        self.slidCsArret.setObjectName("slidCsArret")
        self.slidCsMarche = QtWidgets.QSlider(self.frame_3)
        self.slidCsMarche.setGeometry(QtCore.QRect(10, 400, 160, 22))
        self.slidCsMarche.setOrientation(QtCore.Qt.Horizontal)
        self.slidCsMarche.setObjectName("slidCsMarche")
        self.slidCsECS = QtWidgets.QSlider(self.frame_2)
        self.slidCsECS.setGeometry(QtCore.QRect(20, 230, 160, 22))
        self.slidCsECS.setOrientation(QtCore.Qt.Horizontal)
        self.slidCsECS.setObjectName("slidCsECS")
        self.slidCsChaufNuit = QtWidgets.QSlider(self.frame)
        self.slidCsChaufNuit.setGeometry(QtCore.QRect(10, 440, 160, 22))
        self.slidCsChaufNuit.setOrientation(QtCore.Qt.Horizontal)
        self.slidCsChaufNuit.setObjectName("slidCsChaufNuit")
        self.slidCsChaufJour = QtWidgets.QSlider(self.frame)
        self.slidCsChaufJour.setGeometry(QtCore.QRect(10, 220, 160, 22))
        self.slidCsChaufJour.setOrientation(QtCore.Qt.Horizontal)
        self.slidCsChaufJour.setObjectName("slidCsChaufJour")
        ###labels#####
        self.label_3 = QtWidgets.QLabel(self.frame_3)
        self.label_3.setGeometry(QtCore.QRect(60, 20, 60, 16))
        self.label_3.setObjectName("label_3")
        self.label_5 = QtWidgets.QLabel(self.frame_2)
        self.label_5.setGeometry(QtCore.QRect(80, 370, 31, 16))
        self.label_5.setObjectName("label_5")
        self.label_7 = QtWidgets.QLabel(self.frame)
        self.label_7.setGeometry(QtCore.QRect(50, 20, 71, 16))
        self.label_7.setObjectName("label_7")
        self.label_2 = QtWidgets.QLabel(self.frame)
        self.label_2.setGeometry(QtCore.QRect(10, 110, 161, 21))
        self.label_2.setObjectName("label_2")
        self.label_6 = QtWidgets.QLabel(self.frame)
        self.label_6.setGeometry(QtCore.QRect(10, 260, 161, 31))
        self.label_6.setObjectName("label_6")
        self.label_8 = QtWidgets.QLabel(self.frame_2)
        self.label_8.setGeometry(QtCore.QRect(30, 10, 141, 31))
        self.label_8.setObjectName("label_8")
        self.label = QtWidgets.QLabel(self.frame_2)
        self.label.setGeometry(QtCore.QRect(40, 100, 111, 31))
        self.label.setObjectName("label")
        self.label_4 = QtWidgets.QLabel(self.frame_2)
        self.label_4.setGeometry(QtCore.QRect(70, 280, 41, 16))
        self.label_4.setObjectName("label_4")
        self.label_9 = QtWidgets.QLabel(self.frame_3)
        self.label_9.setGeometry(QtCore.QRect(40, 110, 101, 16))
        self.label_9.setObjectName("label_9")
        self.label_10 = QtWidgets.QLabel(self.frame_3)
        self.label_10.setGeometry(QtCore.QRect(30, 280, 111, 20))
        self.label_10.setObjectName("label_10")
        self.label_11 = QtWidgets.QLabel(self.frame_4)
        self.label_11.setGeometry(QtCore.QRect(90, 20, 91, 16))
        self.label_11.setObjectName("label_11")
        self.label_12 = QtWidgets.QLabel(self.frame_4)
        self.label_12.setGeometry(QtCore.QRect(110, 50, 60, 16))
        self.label_12.setObjectName("label_12")
        self.label_13 = QtWidgets.QLabel(self.frame_4)
        self.label_13.setGeometry(QtCore.QRect(110, 170, 60, 16))
        self.label_13.setObjectName("label_13")
        self.label_14 = QtWidgets.QLabel(self.frame_4)
        self.label_14.setGeometry(QtCore.QRect(120, 290, 41, 16))
        self.label_14.setObjectName("label_14")
        self.label_15 = QtWidgets.QLabel(self.centralwidget)
        self.label_15.setGeometry(QtCore.QRect(400, 10, 151, 31))
        self.label_15.setObjectName("label_15")
        self.label_16 = QtWidgets.QLabel(self.frame_4)
        self.label_16.setGeometry(QtCore.QRect(120, 420, 41, 16))
        self.label_16.setObjectName("label_16")
        """status labels"""
        self.label_18 = QtWidgets.QLabel(self.centralwidget)
        self.label_18.setGeometry(QtCore.QRect(310, 40, 41, 31))
        self.label_18.setObjectName("label_18")
        self.label_19 = QtWidgets.QLabel(self.centralwidget)
        self.label_19.setGeometry(QtCore.QRect(440, 40, 41, 31))
        self.label_19.setObjectName("label_19")
        self.label_20 = QtWidgets.QLabel(self.centralwidget)
        self.label_20.setGeometry(QtCore.QRect(370, 40, 41, 31))
        self.label_20.setObjectName("label_20")
        self.label_21 = QtWidgets.QLabel(self.centralwidget)
        self.label_21.setGeometry(QtCore.QRect(520, 40, 41, 31))
        self.label_21.setObjectName("label_21")
        self.label_22 = QtWidgets.QLabel(self.centralwidget)
        self.label_22.setGeometry(QtCore.QRect(590, 40, 41, 31))
        self.label_22.setObjectName("label_22")
        ######lcd ####
        self.lcdCsCHjour = QtWidgets.QLCDNumber(self.frame)
        self.lcdCsCHjour.setGeometry(QtCore.QRect(20, 150, 131, 51))
        self.lcdCsCHjour.setObjectName("lcdCsCHjour")
        self.lcdCsCHNuit = QtWidgets.QLCDNumber(self.frame)
        self.lcdCsCHNuit.setGeometry(QtCore.QRect(20, 370, 131, 51))
        self.lcdCsCHNuit.setObjectName("lcdCsCHNuit")
        self.lcdCsECS = QtWidgets.QLCDNumber(self.frame_2)
        self.lcdCsECS.setGeometry(QtCore.QRect(30, 150, 131, 51))
        self.lcdCsECS.setObjectName("lcdCsECS")
        self.lcdCsArret = QtWidgets.QLCDNumber(self.frame_3)
        self.lcdCsArret.setGeometry(QtCore.QRect(20, 150, 131, 51))
        self.lcdCsArret.setObjectName("lcdCsArret")
        self.lcdCsMarche = QtWidgets.QLCDNumber(self.frame_3)
        self.lcdCsMarche.setGeometry(QtCore.QRect(30, 330, 131, 51))
        self.lcdCsMarche.setObjectName("lcdCsMarche")
        ##lcd temps
        self.lcdECS = QtWidgets.QLCDNumber(self.frame_4)
        self.lcdECS.setGeometry(QtCore.QRect(50, 70, 171, 71))
        self.lcdECS.setSmallDecimalPoint(True)
        self.lcdECS.setObjectName("lcdECS")
        self.lcdReseau = QtWidgets.QLCDNumber(self.frame_4)
        self.lcdReseau.setGeometry(QtCore.QRect(60, 190, 161, 71))
        self.lcdReseau.setSmallDecimalPoint(True)
        self.lcdReseau.setObjectName("lcdReseau")
        self.lcdCorp = QtWidgets.QLCDNumber(self.frame_4)
        self.lcdCorp.setGeometry(QtCore.QRect(60, 310, 161, 71))
        self.lcdCorp.setSmallDecimalPoint(True)
        self.lcdCorp.setObjectName("lcdCorp")
        self.lcdCouloir = QtWidgets.QLCDNumber(self.frame_4)
        self.lcdCouloir.setGeometry(QtCore.QRect(60, 450, 161, 71))
        self.lcdCouloir.setObjectName("lcdCouloir")
 
        """Heure"""
        self.Lcdhour = QtWidgets.QLCDNumber(self.centralwidget)
        self.Lcdhour.setGeometry(QtCore.QRect(690, 20, 131, 31))
        self.Lcdhour.setSmallDecimalPoint(True)
        self.Lcdhour.setDigitCount(5)
        self.Lcdhour.setObjectName("Lcdhour")
        
        def UpdateClock():
            self.Lcdhour.display(datetime.now().strftime("%H:%M"))
            
            
        timer = QTimer(self)
        timer.timeout.connect(lambda:UpdateClock())
        timer.start(5000) # update every 30 second
            
        """ LOGO """
        self.label_17 = QtWidgets.QLabel(self.centralwidget)
        self.label_17.setGeometry(QtCore.QRect(10, 10, 171, 51))
        self.label_17.setText("")
        self.label_17.setPixmap(QtGui.QPixmap("chappee_logo.png"))
        self.label_17.setScaledContents(True)
        self.label_17.setObjectName("label_17")

        """ slider to LCD """
        self.slidCsChaufNuit.valueChanged['int'].connect(self.lcdCsCHNuit.display)
        self.slidCsChaufJour.valueChanged['int'].connect(self.lcdCsCHjour.display)
        self.slidCsECS.valueChanged['int'].connect(self.lcdCsECS.display)
        self.slidCsArret.valueChanged['int'].connect(self.lcdCsArret.display)
        self.slidCsMarche.valueChanged['int'].connect(self.lcdCsMarche.display)
        QtCore.QMetaObject.connectSlotsByName(self)

        """Buttons"""
        self.ButtonECS.clicked.connect(lambda:self.WriteState("ECS"))
        self.ButtonChauff.clicked.connect(lambda:self.WriteState("CHAUFF"))
        self.ButtonMarche.clicked.connect(lambda:self.WriteState("MARCH"))
        self.ButtonPoele.clicked.connect(lambda:self.WriteState("POELE"))
        
        ##########     sliders        ###############
        """ write values to array  """    
        self.slidCsChaufNuit.valueChanged['int'].connect(lambda:self.writesliders("slidCsChaufNuit"))
        self.slidCsChaufJour.valueChanged['int'].connect(lambda:self.writesliders("slidCsChaufJour"))
        self.slidCsECS.valueChanged['int'].connect(lambda:self.writesliders("slidCsECS"))
        self.slidCsArret.valueChanged['int'].connect(lambda:self.writesliders("slidCsArret"))
        self.slidCsMarche.valueChanged['int'].connect(lambda:self.writesliders("slidCsMarche"))
         
        ########### Times  #################
        """ write values to array  """    
        self.timeECSDeb.timeChanged.connect(lambda:self.writeTime("timeECSDeb"))
        self.timeECSFin.timeChanged.connect(lambda:self.writeTime("timeECSFin"))
        self.timeChauffJour.timeChanged.connect(lambda:self.writeTime("timeChauffJour"))
        self.timeChauffNuit.timeChanged.connect(lambda:self.writeTime("timeChauffNuit"))
       
           
        def retranslateUi():
            _translate = QtCore.QCoreApplication.translate
            self.setWindowTitle(_translate("MainWindow", "Chaudiere"))
            self.label_7.setText(_translate("MainWindow", "Chauffage"))
            self.label_2.setText(_translate("MainWindow", "Consigne Chauffage Jour"))
            self.label_6.setText(_translate("MainWindow", "Consigne Chauffage Nuit"))
            self.ButtonChauff.setText(_translate("MainWindow", "MARCHE CHAUFFAGE"))
            self.label_8.setText(_translate("MainWindow", "Eau Chaude Sanitaire"))
            self.label.setText(_translate("MainWindow", "Consigne Ballon"))
            self.label_4.setText(_translate("MainWindow", "Debut"))
            self.label_5.setText(_translate("MainWindow", "Fin"))
            self.ButtonECS.setText(_translate("MainWindow", "MARCHE ECS"))
            self.label_3.setText(_translate("MainWindow", "General"))
            self.ButtonMarche.setText(_translate("MainWindow", "Marche Chaudiere"))
            self.label_9.setText(_translate("MainWindow", "Consigne Arret"))
            self.label_10.setText(_translate("MainWindow", "Consigne Marche"))
            self.label_12.setText(_translate("MainWindow", "Ballon"))
            self.label_11.setText(_translate("MainWindow", "Temperatures"))
            self.label_13.setText(_translate("MainWindow", "Reseau"))
            self.label_14.setText(_translate("MainWindow", "Corps"))
            self.label_16.setText(_translate("MainWindow", "Couloir"))
            self.label_15.setText(_translate("MainWindow", "CHAUDIERE STATUS"))
            self.label_18.setText(_translate("MainWindow", "SYS"))
            self.label_19.setText(_translate("MainWindow", "C.ECS"))
            self.label_20.setText(_translate("MainWindow", "MAIN"))
            self.label_21.setText(_translate("MainWindow", "C.CH"))
            self.label_22.setText(_translate("MainWindow", "C.POE"))
            self.ButtonPoele.setText(_translate("MainWindow", "MARCHE POELE"))
      
        retranslateUi()
     
        #self.Go=True
        ##########        first start init default values         #######################
        if self.init==True:
            
            #[ECS,Chauffage,chaudiere,poele]
            #if State =0  pushbutton ->ON
            self.state=[0,1,0,0]
            #[chauffage nuit,chauffage jour,ECS,Chaudiere off,Chaudiere on]
            self.sliders=[15,20,55,83,38]
            self.Heures=['6:00','20:00','8:30','20:30']
            
            """  default hours values     """
            self.timeECSDeb.setTime(QTime(9,30))
            self.timeECSFin.setTime(QTime(20,30))
            self.timeChauffJour.setTime(QTime(6,30))
            self.timeChauffNuit.setTime(QTime(20,00))

            """  default temp values     """
            self.slidCsChaufNuit.setValue(15)
            self.slidCsChaufJour.setValue(19)
            self.slidCsECS.setValue(55)
            self.slidCsArret.setValue(85)
            self.slidCsMarche.setValue(38)
            
            """ default buttons values"""
            self.WriteState("ECS")
            self.WriteState("CHAUFF")
            self.WriteState("MARCH")
            self.WriteState("POELE")
            
            self.init=False
             
        self.show()
        
#####################################################################################
"""partie one wire 3*ds18b20"""
class ds18b20(threading.Thread):
    def __init__(self,nom = 'ds18b20'):
      threading.Thread.__init__(self)
      self.nom=nom
      self.terminated = False
      self.Temp=[0,0,0,0]
    def run(self):
                    time.sleep(1)
                    logger.info('Start Reading ds18B20')
                    temp=['1','2','3','4']
                    base_dir = '/sys/bus/w1/devices/'
                    device_folders = glob.glob(base_dir + '28*')

                    while True:
                          #print (self.Temp)
                          time.sleep(1)
                          def get_data_points():
                            for sensors in range (4): # number of sensors
                                device_file=device_folders[sensors]+ '/w1_slave'
                                temp[sensors] = read_temp(device_file)
                                if not (temp[sensors]is None):
                                    self.Temp[sensors]=temp[sensors]
                                #print (self.Temp[sensors])    
                            return  self.Temp
                        
                          def read_temp_raw(device_file): 
                                f = open(device_file, 'r')
                                lines = f.readlines()
                                f.close()
                                return lines
                          
                          def read_temp(device_file): # checks the temp recieved for errors
                                lines = read_temp_raw(device_file)
                                if lines != []:
                                    if lines[0] != "":
                                        while lines[0].strip()[-3:] != 'YES':
                                            time.sleep(0.2)
                                            lines = read_temp_raw(device_file)

                                        equals_pos = lines[1].find('t=')
                                        if equals_pos != -1:
                                            temp_string = lines[1][equals_pos+2:]
                                            # set proper decimal place for C
                                            temp = float(temp_string) / 1000.0
                                            # Round temp to 2 decimal points
                                            temp = round(temp, 1)
                                            if temp>120 or temp<0:
                                                temp2=100
                                            else:
                                                temp2=temp
                                        return temp2
                                else:
                                     get_data_points()
                                     
                          get_data_points()
                          ######### value to GUI   ############
                          application.lcdECS.display(self.Temp[0])
                          application.lcdReseau.display(self.Temp[2])
                          application.lcdCorp.display(self.Temp[3])
                          application.lcdCouloir.display(self.Temp[1])
              
    def stop(self):
              self._stopevent.set()
#######################################    PLC         ##############################################
class Plc(threading.Thread):
      def __init__(self,nom = 'Plc'):
          threading.Thread.__init__(self)
          self.nom=nom
          self.terminated = False
          self.button=[0,0,0,0]
          self.Sliders=[0,0,0,0,0]
          self.Heures=["0:00","0:00","0:00","0:00"]
          self.ordreEcs=0
          self.ordreChauffage=0
          self.ordreCirculPoele=0
          self.output=[0,0,0,0,0,0,0,0]
          self.init=0
          
      def run(self):
                logger.info('Start PLC')
                time.sleep(1)
                #*******************gpio**********************
                GPIO.setmode(GPIO.BCM)
                #ignore les msg d'alarme 
                GPIO.setwarnings(False)
                
                #entree
                GPIO.setup(1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
                GPIO.setup(7, GPIO.IN, pull_up_down=GPIO.PUD_UP)
                GPIO.setup(8, GPIO.IN, pull_up_down=GPIO.PUD_UP)
                GPIO.setup(25, GPIO.IN, pull_up_down=GPIO.PUD_UP)

                #sorties 
                GPIO.setup(5, GPIO.OUT)
                GPIO.setup(6, GPIO.OUT)
                GPIO.setup(13, GPIO.OUT)
                GPIO.setup(16, GPIO.OUT)
                GPIO.setup(19, GPIO.OUT)
                GPIO.setup(20, GPIO.OUT)
                GPIO.setup(21, GPIO.OUT)
                GPIO.setup(26, GPIO.OUT)

                
                
                #####################   read input      ##################### 
                def ReadInput():
                    add=[1,7,8,25]#adresses gpio input
                    Lenght=len (add)
                    Input=[0]*Lenght
                    for i in range (0,Lenght):
                        Input[i]=GPIO.input(add[i])
                    return Input[0:Lenght]

                ########################    maincode    ######################
                def MainCode(Input):
                
                    if self.init == 0:
                        SousTension= 0
                        CirculECS=0
                        CirculChauff=0
                        CirculPoele=0
                        self.memo=0
                        self.memo2=0
                        self.f_on=False
                        self.f_off=False
                        self.f_on2=False
                        self.f_off2=False
                        self.init=1
                        
                        
                    """mnemoniques"""
                    #buttons
                    ButtonEcs=self.button[0]
                    ButtonChauffage=self.button[1]
                    ButtonMarche=self.button[2]
                    ButtonPoele=self.button[3]
                    #Temp ds18B20
                    TempEcs=onewire.Temp[0]
                    TempsRes=onewire.Temp[2]
                    TempsCorps=onewire.Temp[3]
                    TempsHome=onewire.Temp[1]
            
                    #Hours
                    CsHEcsOn= datetime.strptime(self.Heures[0], "%H:%M").strftime("%H:%M")
                    CsHEcsOff=datetime.strptime(self.Heures[1], "%H:%M").strftime("%H:%M")
                    CsHChJour=datetime.strptime(self.Heures[2], "%H:%M").strftime("%H:%M")
                    CsHChNuit=datetime.strptime(self.Heures[3], "%H:%M").strftime("%H:%M")
                    Now=datetime.now().strftime("%H:%M")
                    #Temps
                    CsChauffN=self.Sliders[0]
                    CsChauffJ=self.Sliders[1]
                    CsEcsOff=self.Sliders[2]
                    CsStop=self.Sliders[3]
                    CsEcsOn=self.Sliders[4]
                    
                    """consigne chauff"""
                    if Now >= CsHChJour and Now < CsHChNuit :
                       Cschauff=CsChauffJ
                    else:
                       Cschauff=CsChauffN
                       
                    """mise sous tension """
                    if ButtonMarche==True: #marche chaudiere
                        """ECS"""
                        if (ButtonEcs and Now>=CsHEcsOn and Now<=CsHEcsOff): #marche ECS
                            if TempEcs<CsEcsOff and TempEcs!= 0:
                                self.ordreEcs=True
                                
                            if TempEcs>CsEcsOff:#Temp atteinte
                                self.ordreEcs=False
                        else:
                            self.ordreEcs=False
                        
                        """chauffage fioul"""    
                        if (ButtonChauffage ==True and TempsHome<Cschauff): #Marche Chauffage
                            self.ordreChauffage=True
                        else:
                            self.ordreChauffage=False        
                    else:
                        self.ordreChauffage=False
                        self.ordreEcs=False
                        
                    """circulateur poele"""        
                    if TempsRes > 70 or ButtonPoele :
                        self.ordreCirculPoele=True
                    else:
                        self.ordreCirculPoele=False
                        
                    """Memo 1 cycle ecs"""
                    if ((TempEcs > CsEcsOff) and not self.ordreChauffage) or (TempsCorps > CsStop) :#stop
                        self.memo= False
                        if self.f_on2 == False:
                           self.f_on2 = True
                                     
                    if TempEcs < CsEcsOn: #start 
                        self.memo =True
                        if self.f_on2 == True:
                           self.f_on2 = False
                    
                    
                    """Memo 1 cycle chauffage"""
                    if not self.ordreChauffage or (TempsCorps > CsStop) :#stop
                        self.memo2= False
                        
                    if TempsRes < CsEcsOn and self.ordreChauffage: #start 
                        self.memo2 =True
         
                    """  POST """
                    SousTension= ((self.ordreEcs and  self.memo) or (self.ordreChauffage and self.memo2)) and TempsCorps < CsStop  
                    CirculECS=self.ordreEcs and TempsCorps > TempEcs+1
                    CirculChauff=self.ordreChauffage and not self.ordreEcs #priorité ECS
                    CirculPoele=self.ordreCirculPoele #and not self.ordreChauffage and not CirculChauff#Priorité Chauff fioul
                    time.sleep(1)
                    
                    """debug"""
                    print('TempEcs:',TempEcs, ' TempsRes:',TempsRes,' TempsCorps:',TempsCorps,' CirculPoele:',CirculPoele,' CirculChauff:',CirculChauff,' CirculECS:',CirculECS,' SousTension:',SousTension)
                    #print(TempEcs , CsEcsOff ,CsEcsOn,TempsRes,TempsCorps,CsStop,self.memo,self.memo2,CirculPoele,CirculChauff,CirculECS,SousTension)
                    
                    """Sorties"""
                    self.output=[SousTension,CirculECS,CirculChauff,CirculPoele,0,0,0,0]
                    #print (self.output)
                    
                    if self.output[0]==True:
                            application.label_20.setStyleSheet('color: green')
                    else:
                            application.label_20.setStyleSheet('color: dark')
                    if self.output[1]==True:
                            application.label_19.setStyleSheet('color: green')
                    else:
                            application.label_19.setStyleSheet('color: dark')
                    if self.output[2]==True:
                            application.label_21.setStyleSheet('color: green')
                    else:
                            application.label_21.setStyleSheet('color: dark') 
                    if self.output[3]==True:
                            application.label_22.setStyleSheet('color: green')
                    else:
                            application.label_22.setStyleSheet('color: dark')
                    return self.output

                #######################      Write output      ###################
                def WriteOutput(Output):
                     add=[5,6,13,16,19,20,21,26]#adresses gpio output
                     Lenght=len (add)
                     for i in range (0,Lenght):
                        GPIO.output(add[i],not Output[i])
                           
                     return Output[0:Lenght]
                     
                ######### mainloop    PLC #########
                try:
                    while True:
                        Input=ReadInput()#lit les entrees
                        Output=MainCode(Input)#code principal
                        WriteOutput(Output)#ecrit les sorties
                        #print (Output)
                        time.sleep(0.01)#Pause
                 
                except KeyboardInterrupt:
                    print("Quitting")
                    GPIO.cleanup()
                    
      def stop(self):
                 self._stopevent.set()    
    
"""**************************partie modbus avec pymodbus installé************************"""
class modbus(threading.Thread):
    def __init__(self,nom = 'modbus'):
      threading.Thread.__init__(self)
      self.nom=nom
      self.terminated = False
    
    def run(self):
            time.sleep(2) 
            logger.info('Start Modbus')
            """**************declare le nb de mots ***********************"""
            store = ModbusSlaveContext(
                di = ModbusSequentialDataBlock(0, [0]*100),
                co = ModbusSequentialDataBlock(0, [0]*100),
                hr = ModbusSequentialDataBlock(0, [0]*100),
                ir = ModbusSequentialDataBlock(0, [0]*100))
            context = ModbusServerContext(slaves=store, single=True)

            """**************************ecrit les entrees dans le module modbus************************"""
            def signed(value):
                packval =struct.pack('<h',value)
                return struct.unpack('<H',packval)[0]
            
            def updating_writer(a):
                #print (int (onewire.Temp[0]*10))
                context  = a[0]
                register = 3
                slave_id = 0
                address  = 10 # mot w10 
                values = [(int (onewire.Temp[0]*10)),(int(onewire.Temp[1]*10)),(int(onewire.Temp[2]*10)),(int(onewire.Temp[3]*10)),(int(api.output[0])),
                          (int(api.output[1])),(int(api.output[2])),(int(api.output[3]))]
                  
                context[slave_id].setValues(register,address,values)
                #print (values)
            """*********lit les valeurs du module modbus ************************"""
            def read_context(a):
                 context  = a[0]
                 register = 3
                 slave_id = 0
                 address  = 30 # mot w30 
                 value = context[slave_id].getValues(register,address,10)
                 
            read = LoopingCall(f=read_context, a=(context,))
            read.start(.2)
            write = LoopingCall(f=updating_writer, a=(context,))
            write.start(.2)
            StartTcpServer(context)
    
    def stop(self):
                 self._stopevent.set()
#####################################################################################
"""partie sys"""
class systeme(threading.Thread):
    def __init__(self,nom = 'sys'):
      threading.Thread.__init__(self)
      self.nom=nom
      self.terminated = True
    def run(self):
                    time.sleep(3)
                    logger.info('sys')
                    listestr=['','','','','','','','','','','','',]
                    threads=['MainThread','ds18b20','Plc','modbus','systeme']#,if run with idle'SockThread']
                    
                    time.sleep(5)
                    #enumere les threads alive
                    while True:
                        output_list=[]
                        liste=threading.enumerate()
                        if liste != []:
                            Nb=len(liste)
                            nb=len(threads)
                            #test si tous les threads sont vivants
                            if Nb< 5:
                                application.label_18.setStyleSheet('color: red')
                                logger.info('all threads are not started Nb:'+str(Nb))
                                for i in range (0,Nb):
                                     listestr[i]=(str(liste[i]))   
                                for j in range (0,Nb):
                                    for k in range (0,nb):
                                        thread= listestr[j].find(threads[k])
                                        if thread != -1:
                                            output_list.append(threads[k])
                                #print(output_list)
                                #print(set(threads).difference(set(output_list)))
                                logger.info ((set(threads).difference(set(output_list))))            
                            else:
                                application.label_18.setStyleSheet('color: green')

                        QtCore.QCoreApplication.processEvents()
                        time.sleep(5)
                        
    def stop(self):
              self._stopevent.set()

#######################################################################                
if __name__ == '__main__':
    logger.info('Starting Main')
    onewire = ds18b20()
    surveillance=systeme()
    api=Plc()
    mod = modbus()
    """Temp""" 
    onewire.start()
    """sys"""
    surveillance.start()
    """PLC"""
    api.start()
    """Modbus"""
    mod.start()
    """prevent freeze"""
    QtCore.QCoreApplication.processEvents()
    """Gui"""
    # create pyqt5 app 
    app = QApplication(sys.argv)
    # create the instance of our Window 
    application = ApplicationWindow()
    # start the app
    sys.exit(app.exec_())



    
    
    
    
   
    
    
    



    
