from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QFile, QTextStream
from PyQt5.QtGui import QCursor, QIntValidator
import re
import os
import shutil
import pathlib
import datetime
import math
import subprocess
import webbrowser
import sys
import dummyfiles
from BRAM import Ui_MainWindow
from diagrams import Diagrams

class window(QtWidgets.QMainWindow):
    def __init__(self):
        super(window,self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        ##################connections#############
        self.ui.pushButton_7.clicked.connect(self.get_started)
        self.ui.pushButton_8.clicked.connect(self.back)
        self.ui.pushButton_22.clicked.connect(self.back)
        self.ui.pushButton_30.clicked.connect(self.back)
        self.ui.pushButton_32.clicked.connect(self.back)
        self.ui.pushButton_24.clicked.connect(lambda:self.select_technology('SKY130'))
        self.ui.pushButton_19.clicked.connect(lambda:self.select_technology('TSMC28'))
        self.ui.pushButton_21.clicked.connect(lambda:self.select_technology('TSMC65'))
        self.ui.pushButton.clicked.connect(self.blockRamPath)
        self.ui.pushButton_2.clicked.connect(self.next)
        self.ui.pushButton_23.clicked.connect(lambda:self.LearnMore('https://skywater-pdk.readthedocs.io/en/main/'))
        self.ui.pushButton_18.clicked.connect(lambda:self.LearnMore('https://www.tsmc.com/english/dedicatedFoundry/technology/logic/l_28nm'))
        self.ui.pushButton_20.clicked.connect(lambda:self.LearnMore('https://www.tsmc.com/english/dedicatedFoundry/technology/logic/l_65nm'))
        self.ui.radioButton.setChecked(True)
        self.ui.pushButton_33.setEnabled(False)
        self.ui.pushButton_33.clicked.connect(self.Generate)
        self.brpath=''
        self.ui.memoryDepthLineEdit_2.editingFinished.connect(self.Addrw)
        self.ui.addressWidthLineEdit.textEdited.connect(self.memdchange)
        self.defaultName=''
        self.ui.checkBox_4.stateChanged.connect(self.inputName)
        self.ui.pushButton_6.clicked.connect(self.Compile)
        self.ui.pushButton_5.clicked.connect(self.aboutMerl)
        self.ui.pushButton_3.clicked.connect(self.UserManual)
        menu_items = [
            'Simulate',
            'Verify'
        ]
        menu =QMenu()
        menu.triggered.connect(lambda x:self.fnc(x.text()))
        self.add_menu(menu_items,menu)
        self.ui.toolButton.setMenu(menu)
        #########validators#################
        self.ui.numbeOfReadPortsLineEdit.setValidator(QIntValidator())
        self.ui.numberOfWritePortsLineEdit.setValidator(QIntValidator())
        self.ui.numberOfAddressPortsLineEdit.setValidator(QIntValidator())
        self.ui.memoryDepthLineEdit.setValidator(QIntValidator())
        self.ui.dataWidthLineEdit.setValidator(QIntValidator())
        self.ui.addressPortLineEdit.setValidator(QIntValidator())
        self.ui.numberOfReadPortsLineEdit.setValidator(QIntValidator())
        self.ui.numberOfWritePortsLineEdit_2.setValidator(QIntValidator())
        #self.lineEdit_84.setValidator(QIntValidator())
        self.ui.memoryDepthLineEdit_2.setValidator(QIntValidator())
        self.ui.dataWidthLineEdit_2.setValidator(QIntValidator())
        self.ui.addressWidthLineEdit.setValidator(QIntValidator())
        








    def get_started(self):
        self.ui.stackedWidget.setCurrentIndex(1)

    def back(self):
        ind=int(self.ui.stackedWidget.currentIndex())
        if ind == 2:
            self.ui.lineEdit.clear()
            self.ui.numbeOfReadPortsLineEdit.clear()
            self.ui.numberOfWritePortsLineEdit.clear()
            self.ui.numberOfAddressPortsLineEdit.clear()
            self.ui.memoryDepthLineEdit.clear()
            self.ui.dataWidthLineEdit.clear()
            self.ui.addressPortLineEdit.clear()
        self.ui.stackedWidget.setCurrentIndex(ind-1)
    
    def select_technology(self,tech):
        self.ui.label_31.setText(f'TECHNOLOGY {tech}nm')
        self.technology = tech
        self.ui.stackedWidget.setCurrentIndex(2)
    
    def blockRamPath(self):
        technology=self.technology
        if technology == "":
            popup=QMessageBox()
            popup.setText("Please Select Technology")
            popup.setStandardButtons(QMessageBox.Ok)
            popup.setIcon(QMessageBox.Critical)
            popup.exec_()
            return
        filename = QFileDialog.getOpenFileName(None,"Select Block Ram File")
        self.ui.lineEdit.setText(filename[0])
        self.brpath=filename[0]
        if self.brpath == '':
            return
        if technology != 'other' and technology.lower() not in self.brpath.lower():
            popup=QMessageBox()
            popup.setText("Model does not match the selected Technology")
            popup.setStandardButtons(QMessageBox.Ok)
            popup.setIcon(QMessageBox.Critical)
            popup.exec_()
        with open (filename[0],'r') as f:
                content = f.read()
        pattern = re.compile(r'parameter (.*)\s*=\s*(\"\"|.*)(;|,)')
        matches = pattern.finditer(content)
        pattern2 = re.compile(r'parameter (.*)\s*=\s*(.*)\s+\)')
        matches2 = pattern2.finditer(content)
        params=[]
        for i in matches:
                params.append(i.group(1).strip())
                exec((i.group(1).strip()+' = '+i.group(2).strip()),globals())
        for i in matches2:
                params.append(i.group(1).strip())
                exec(i.group(1).strip()+' = '+i.group(2).strip(),globals())
        if 'DATA_WIDTH' in params:
                self.ui.dataWidthLineEdit.setText(str(DATA_WIDTH))
                if self.ui.dataWidthLineEdit.text().strip() !='':   
                    self.ui.dataWidthLineEdit.setEnabled(False)
                    self.ui.dataWidthLineEdit.setCursor(QtGui.QCursor(QtCore.Qt.ForbiddenCursor))

        if 'ADDR_WIDTH' in params:
                self.ui.addressPortLineEdit.setText(str(ADDR_WIDTH))
                if self.ui.addressPortLineEdit.text().strip() !='':   
                    self.ui.addressPortLineEdit.setEnabled(False)
                    self.ui.addressPortLineEdit.setCursor(QtGui.QCursor(QtCore.Qt.ForbiddenCursor))
        if 'RAM_DEPTH' in params:
                self.ui.memoryDepthLineEdit.setText(str(RAM_DEPTH))
                if self.ui.memoryDepthLineEdit.text().strip() !='':   
                    self.ui.memoryDepthLineEdit.setEnabled(False)
                    self.ui.memoryDepthLineEdit.setCursor(QtGui.QCursor(QtCore.Qt.ForbiddenCursor))
        elif 'MEMD' in params:
                self.ui.memoryDepthLineEdit.setText(str(MEMD))
                if self.ui.memoryDepthLineEdit.text().strip() !='':   
                    self.ui.memoryDepthLineEdit.setEnabled(False)
                    self.ui.memoryDepthLineEdit.setCursor(QtGui.QCursor(QtCore.Qt.ForbiddenCursor))
        if 'nRPORTS' in params:
                self.ui.numbeOfReadPortsLineEdit.setText(str(nRPORTS))
                if self.ui.numbeOfReadPortsLineEdit.text().strip() !='':   
                    self.ui.numbeOfReadPortsLineEdit.setEnabled(False)
                    self.ui.numbeOfReadPortsLineEdit.setCursor(QtGui.QCursor(QtCore.Qt.ForbiddenCursor))
        if 'nWPORTS' in params:
                self.ui.numberOfWritePortsLineEdit.setText(str(nWPORTS))
                if self.ui.numberOfWritePortsLineEdit.text().strip() !='':   
                    self.ui.numberOfWritePortsLineEdit.setEnabled(False)
                    self.ui.numberOfWritePortsLineEdit.setCursor(QtGui.QCursor(QtCore.Qt.ForbiddenCursor))
    
    def next(self):
        if (self.ui.lineEdit.text().strip() != '') and (self.ui.dataWidthLineEdit.text().strip()!='')and (self.ui.memoryDepthLineEdit.text().strip()!= '')and (self.ui.numberOfWritePortsLineEdit.text().strip() !='') and (self.ui.addressPortLineEdit.text().strip() !='') and (self.ui.numbeOfReadPortsLineEdit.text().strip() !=''):
             self.ui.stackedWidget.setCurrentIndex(3)
            
        else:
           popup=QMessageBox()
           popup.setText("Please Enter All Inputs")
           popup.setStandardButtons(QMessageBox.Ok)
           popup.setIcon(QMessageBox.Critical)
           popup.exec_()

    def LearnMore(self,url):
        webbrowser.open(url)


    def Addrw(self):
        try: 
            addrw=str(int(math.log2(int(self.ui.memoryDepthLineEdit_2.text()))))
        except:
            popup=QMessageBox()
            popup.setText("Invalid Memory depth")
            popup.setStandardButtons(QMessageBox.Ok)
            popup.setIcon(QMessageBox.Critical)
            popup.exec_()
            self.ui.memoryDepthLineEdit_2.clear()
        if self.ui.memoryDepthLineEdit_2.text().strip != self.ui.addressWidthLineEdit.text().strip:
            self.ui.addressWidthLineEdit.setText(addrw)

    def memdchange(self):
        try:
            addrw=str(2**int(self.ui.addressWidthLineEdit.text()))
            self.ui.memoryDepthLineEdit_2.setText(addrw)
        except:
            popup=QMessageBox()
            popup.setText("Invalid Address Width")
            popup.setStandardButtons(QMessageBox.Ok)
            popup.setIcon(QMessageBox.Critical)
            popup.exec_()
            self.ui.addressWidthLineEdit.clear()
                

    def Compile(self):
        if (self.ui.numberOfReadPortsLineEdit.text().strip() != '') and (self.ui.numberOfWritePortsLineEdit_2.text().strip() != '') and (self.ui.memoryDepthLineEdit_2.text().strip() != '') and (self.ui.dataWidthLineEdit_2.text().strip() != '') and (self.ui.addressWidthLineEdit.text().strip() != ''):
            compile=True
        else:
            popup=QMessageBox()
            popup.setText("Please enter all Inputs")
            popup.setStandardButtons(QMessageBox.Ok)
            popup.setIcon(QMessageBox.Critical)
            popup.exec_()
            self.ui.pushButton_33.setEnabled(False)
            compile=False
            return
        if (self.ui.checkBox_3.isChecked() is True) or (self.ui.checkBox_4.isChecked() is True) or (self.ui.checkBox_15.isChecked() is True) or (self.ui.checkBox_16.isChecked() is True):
            compile=True
        else:
            popup=QMessageBox()
            popup.setText("No checkbox selected")
            popup.setStandardButtons(QMessageBox.Ok)
            popup.setIcon(QMessageBox.Critical)
            popup.exec_()
            self.ui.pushButton_33.setEnabled(False)
            compile=False
            return
        if eval(self.ui.memoryDepthLineEdit.text()) >  eval(self.ui.memoryDepthLineEdit_2.text()):
            compile=False
            popup=QMessageBox()
            popup.setText("Invalid Specification")
            popup.setInformativeText("Base Ram size is bigger than Output specification")
            popup.setStandardButtons(QMessageBox.Ok)
            popup.setIcon(QMessageBox.Critical)
            popup.exec_()
        if eval(self.ui.dataWidthLineEdit.text()) >  eval(self.ui.dataWidthLineEdit_2.text()):
            compile=False
            popup=QMessageBox()
            popup.setText("Invalid Specification")
            popup.setInformativeText("Base Ram width is bigger than Output specification")
            popup.setStandardButtons(QMessageBox.Ok)
            popup.setIcon(QMessageBox.Critical)
            popup.exec_()
        if compile == True:
            ######for bank#######
            a=str(self.ui.numbeOfReadPortsLineEdit.text())
            self.ui.label_12.setText(a)
            a=str(self.ui.numberOfWritePortsLineEdit.text())
            self.ui.label_13.setText(a)
            a=str(self.ui.memoryDepthLineEdit.text())
            self.ui.label_14.setText(a)
            a=str(self.ui.addressPortLineEdit.text())
            self.ui.label_16.setText(a)
            ######for output####
            a=str(self.ui.numberOfReadPortsLineEdit.text())
            self.ui.label_2.setText(a)
            a=str(self.ui.numberOfWritePortsLineEdit_2.text())
            self.ui.label_3.setText(a)
            a=str(self.ui.memoryDepthLineEdit_2.text())
            self.ui.label_4.setText(a)
            a=str(self.ui.dataWidthLineEdit_2.text())
            self.ui.label_6.setText(a)
            a=str(self.ui.addressWidthLineEdit.text())
            self.ui.label_5.setText(a)
            
            banks=int(self.ui.memoryDepthLineEdit_2.text())//int(self.ui.memoryDepthLineEdit.text())
            fixed=int(self.ui.dataWidthLineEdit_2.text())//int(self.ui.dataWidthLineEdit.text())
            
            if self.ui.radioButton.isChecked() is True:
                banks = banks * fixed 
                
            now = datetime.datetime.now()
            nwports = int(self.ui.numberOfWritePortsLineEdit_2.text())
            nrports = int(self.ui.numberOfReadPortsLineEdit.text())
            brams= (nwports*((nwports-1)+nrports))*banks
            
            n1=self.ui.label_2.text()
            n2=self.ui.label_3.text()
            brn=pathlib.Path(self.brpath).name

            if '.v' in brn:
                brn= brn[:-2]
            
            elif '.sv' in brn:
                brn = brn[:-3]
            if int(n1)==1 and int(n2)==1:
               # self.outfn=brn+"_"+self.lineEdit_66.text()+"x"+self.lineEdit_67.text()+'_1rw_'+now.strftime("%Y-%m-%d_%H-%M-%S")
               self.outfn="ram_"+self.ui.label_4.text()+"x"+self.ui.label_6.text()+'_1rw_'+now.strftime("%Y-%m-%d_%H-%M-%S")
            else:
               # self.outfn=brn+"_"+self.lineEdit_66.text()+"x"+self.lineEdit_67.text()+'_'+n1+'r'+n2+'w_'+now.strftime("%Y-%m-%d_%H-%M-%S")
               self.outfn="ram_"+self.ui.label_4.text()+"x"+self.ui.label_6.text()+'_'+n1+'r'+n2+'w_'+now.strftime("%Y-%m-%d_%H-%M-%S")
            
            self.outpath=pathlib.Path(__file__).parents[1].joinpath("output",self.outfn)
            self.ui.label_9.setText(str(self.outpath))
            self.ui.label_7.setText(str(banks))
            self.ui.label_8.setText(str(brams))
            self.ui.pushButton_33.setEnabled(True)
            inp_size=int(self.ui.memoryDepthLineEdit.text())//(32*8)
            out_size=int(self.ui.memoryDepthLineEdit_2.text())//(32*8)
            inp_width=int(self.ui.dataWidthLineEdit.text())
            out_width=int(self.ui.dataWidthLineEdit_2.text())
            r=int(self.ui.numberOfReadPortsLineEdit.text())
            w=int(self.ui.numberOfWritePortsLineEdit_2.text())
            diag=Diagrams(inp_size,out_size,inp_width,out_width,r,w)
            self.ui.stackedWidget.setCurrentIndex(4)
            diag.showDiag()
    def Generate(self):
        pathlib.Path(self.outpath).mkdir(parents=True,exist_ok=True)
        brn=pathlib.Path(self.brpath).name
        brext=''
        if '.v' in brn:
            brext=brn[-2:]
            brn= brn[:-2]
            
        elif '.sv' in brn:
            brext = brn[-3:]
            brn = brn[:-3]
            
        out=0
        rw=False
        nr1w=False
        nrnw=False
        if int(self.ui.label_2.text())==1 and int(self.ui.label_3.text())==1:
            modelp=pathlib.Path(__file__).parent.absolute().joinpath("dummy",'ram_dummy_1rw.v')
            tbp=pathlib.Path(__file__).parent.absolute().joinpath("dummy",'ram_dummy_1rw_tb.v')

            model=dummyfiles.ram_dummy_1rw()
            tb=dummyfiles.ram_dummy_1rw_tb()
            #outmn=brn+"_generated_"+self.lineEdit_66.text()+"x"+self.lineEdit_67.text()+'_1rw.v'
            #outtbn=brn+"_generated_"+self.lineEdit_66.text()+"x"+self.lineEdit_67.text()+'_1rw_tb.v'
            outmn="ram_generated_"+self.ui.label_4.text()+"x"+self.ui.label_6.text()+'_1rw.v'
            outtbn="ram_generated_"+self.ui.label_4.text()+"x"+self.ui.label_6.text()+'_1rw_tb.v'
            rw=True
        elif int(self.ui.label_2.text())>1 and int(self.ui.label_3.text())==1:
            modelp=pathlib.Path(__file__).parent.absolute().joinpath("dummy",'ram_dummy_nr1w.v')
            tbp=pathlib.Path(__file__).parent.absolute().joinpath("dummy",'ram_dummy_nr1w_tb.v')
            model1rw=pathlib.Path(__file__).parent.absolute().joinpath("dummy",'ram_dummy_1rw.v')
            
            model=dummyfiles.ram_dummy_nr1w()
            modelrw=dummyfiles.ram_dummy_1rw()
            tb=dummyfiles.ram_dummy_nr1w_tb()

            n=self.ui.label_2.text()
            #outmn=brn+"_generated_"+self.lineEdit_66.text()+"x"+self.lineEdit_67.text()+'_'+n+'r1w.v'
            #outtbn=brn+"_generated_"+self.lineEdit_66.text()+"x"+self.lineEdit_67.text()+'_'+n+'r1w_tb.v'
            #gen1rwoutn=brn+"_generated_"+self.lineEdit_66.text()+"x"+self.lineEdit_67.text()+'_1rw.v'
            outmn="ram_generated_"+self.ui.label_4.text()+"x"+self.ui.label_6.text()+'_'+n+'r1w.v'
            outtbn="ram_generated_"+self.ui.label_4.text()+"x"+self.ui.label_6.text()+'_'+n+'r1w_tb.v'
            gen1rwoutn="ram_generated_"+self.ui.label_4.text()+"x"+self.ui.label_6.text()+'_1rw.v'
            gen1rwout=pathlib.Path(self.outpath).joinpath(gen1rwoutn)
            nr1w=True
        elif int(self.ui.label_3.text())>1:
            modelp=pathlib.Path(__file__).parent.absolute().joinpath("dummy",'ram_dummy_nrnw.v')
            tbp=pathlib.Path(__file__).parent.absolute().joinpath("dummy",'ram_dummy_nrnw_tb.v')
            model1rw=pathlib.Path(__file__).parent.absolute().joinpath("dummy",'ram_dummy_1rw.v')
            modelnr1w=pathlib.Path(__file__).parent.absolute().joinpath("dummy",'ram_dummy_nr1w.v')
            
            model=dummyfiles.ram_dummy_nrnw()
            modelrw=dummyfiles.ram_dummy_1rw()
            modelnrw=dummyfiles.ram_dummy_nr1w()
            tb=dummyfiles.ram_dummy_nrnw_tb()

            n1=self.ui.label_2.text()
            n2=self.ui.label_3.text()
            #outmn=brn+"_generated_"+self.lineEdit_66.text()+"x"+self.lineEdit_67.text()+'_'+n1+'r'+n2+'w.v'
            #outtbn=brn+"_generated_"+self.lineEdit_66.text()+"x"+self.lineEdit_67.text()+'_'+n1+'r'+n2+'w_tb.v'
            #gen1rwoutn=brn+"_generated_"+self.lineEdit_66.text()+"x"+self.lineEdit_67.text()+'_1rw.v'
            outmn="ram_generated_"+self.ui.label_4.text()+"x"+self.ui.label_6.text()+'_'+n1+'r'+n2+'w.v'
            outtbn="ram_generated_"+self.ui.label_4.text()+"x"+self.ui.label_6.text()+'_'+n1+'r'+n2+'w_tb.v'
            gen1rwoutn="ram_generated_"+self.ui.label_4.text()+"x"+self.ui.label_6.text()+'_1rw.v'
            gen1rwout=pathlib.Path(self.outpath).joinpath(gen1rwoutn)
            #gennr1woutn=brn+"_generated_"+self.lineEdit_66.text()+"x"+self.lineEdit_67.text()+'_'+n1+'r1w.v'
            gennr1woutn="ram_generated_"+self.ui.label_4.text()+"x"+self.ui.label_6.text()+'_'+n1+'r1w.v'
            gennr1wout=pathlib.Path(self.outpath).joinpath(gennr1woutn)
            nrnw=True
        utilsoutp=pathlib.Path(self.outpath).joinpath('utils.vh')
        utilsp=pathlib.Path(__file__).parent.absolute().joinpath("dummy",'utils.vh')
        makep=pathlib.Path(__file__).parent.absolute().joinpath("dummy",'Makefile')
        makeoutp=pathlib.Path(self.outpath).joinpath('Makefile')
        outputmp=pathlib.Path(self.outpath).joinpath(outmn)
        outputtbp=pathlib.Path(self.outpath).joinpath(outtbn)
       
        # with open (makep,'r') as f:
        #         mak = f.read()
        mak=dummyfiles.MakeFile()
        with open (makeoutp,'w') as f:
                f.writelines(mak.format(pathlib.Path(self.brpath).name,pathlib.Path(self.brpath).name))
                
        if self.ui.checkBox_15.isChecked() == True:
            out+=1
            
            # with open (modelp,'r') as f:
            #     model = f.read()
            if rw is True:
                with open (outputmp,'w') as f:
                    f.writelines(model.format((int(self.ui.label_6.text())//int(self.ui.dataWidthLineEdit.text()))*4,self.ui.label_4.text(),self.ui.label_6.text(),self.ui.memoryDepthLineEdit.text(),self.ui.label_5.text(),self.ui.dataWidthLineEdit.text(),int(self.ui.radioButton.isChecked()),brn,brn))
            elif nr1w is True:
                # with open (model1rw,'r') as f:
                #     modelrw = f.read()
                with open (outputmp,'w') as f:
                    f.writelines(model.format((int(self.ui.label_6.text())//int(self.ui.dataWidthLineEdit.text()))*4,self.ui.label_4.text(),self.ui.label_6.text(),self.ui.label_2.text(),self.ui.memoryDepthLineEdit.text(),self.ui.label_5.text()))
                with open (gen1rwout,'w') as f:
                    f.writelines(modelrw.format((int(self.ui.label_6.text())//int(self.ui.dataWidthLineEdit.text()))*4,self.ui.label_4.text(),self.ui.label_6.text(),self.ui.memoryDepthLineEdit.text(),self.ui.label_5.text(),self.ui.dataWidthLineEdit.text(),int(self.ui.radioButton.isChecked()),brn,brn))
            elif nrnw is True:
                # with open (model1rw,'r') as f:
                #     modelrw = f.read()
                # with open (modelnr1w,'r') as f:
                #     modelnrw = f.read()
                with open (outputmp,'w') as f:
                    f.writelines(model.format((int(self.ui.label_6.text())//int(self.ui.dataWidthLineEdit.text()))*4,self.ui.label_4.text(),self.ui.label_6.text(),self.ui.label_2.text(),self.ui.label_3.text(),self.ui.memoryDepthLineEdit.text(),self.ui.label_5.text()))
                with open (gennr1wout,'w') as f:
                    f.writelines(modelnrw.format((int(self.ui.label_6.text())//int(self.ui.dataWidthLineEdit.text()))*4,self.ui.label_4.text(),self.ui.label_6.text(),self.ui.label_2.text(),self.ui.memoryDepthLineEdit.text(),self.ui.label_5.text()))
                with open (gen1rwout,'w') as f:
                    f.writelines(modelrw.format((int(self.ui.label_6.text())//int(self.ui.dataWidthLineEdit.text()))*4,self.ui.label_4.text(),self.ui.label_6.text(),self.ui.memoryDepthLineEdit.text(),self.ui.label_5.text(),self.ui.dataWidthLineEdit.text(),int(self.ui.radioButton.isChecked()),brn,brn))

        if self.ui.checkBox_16.isChecked() == True:
            out+=1
            # with open (tbp,'r') as f:
            #     tb = f.read()
            if rw is True:
                with open (outputtbp,'w') as f:
                    f.writelines(tb.format((int(self.ui.label_6.text())//int(self.ui.dataWidthLineEdit.text()))*4,self.ui.label_4.text(),self.ui.label_6.text(),self.ui.memoryDepthLineEdit.text(),self.ui.label_5.text()))
            elif nr1w is True:
                with open (outputtbp,'w') as f:
                    f.writelines(tb.format((int(self.ui.label_6.text())//int(self.ui.dataWidthLineEdit.text()))*4,self.ui.label_4.text(),self.ui.label_6.text(),self.ui.label_2.text(),self.ui.memoryDepthLineEdit.text(),self.ui.label_5.text()))
            elif nrnw is True:
                with open (outputtbp,'w') as f:
                    f.writelines(tb.format((int(self.ui.label_6.text())//int(self.ui.dataWidthLineEdit.text()))*4,self.ui.label_4.text(),self.ui.label_6.text(),self.ui.label_3.text(),self.ui.label_2.text(),self.ui.memoryDepthLineEdit.text(),self.ui.label_5.text()))
            #shutil.copy(makep, makeoutp)
        if self.ui.checkBox_4.isChecked() == True:
            out+=1
            synthp=pathlib.Path(__file__).parent.absolute().joinpath("dummy",'synth.tcl')
            synthoutp=pathlib.Path(self.outpath).joinpath('synth.tcl')
            synth=dummyfiles.sythtcl()
            # with open (synthp,'r') as f:
            #     synth=f.read()
            if rw is True:
                top = "ram_generic_1rw"
            elif nr1w is True:
                top = "ram_generic_nr1w"
            elif nrnw is True:
                top = 'ram_generic_nrnw'
            with open (synthoutp,'w') as f:
                f.writelines(synth.format(self.defaultName,top))
                     
        # shutil.copy(utilsp, utilsoutp)
        brout=pathlib.Path(self.outpath).joinpath(brn+brext)
        shutil.copy(self.brpath,brout)
        with open(utilsoutp,'w') as f:
            f.writelines(dummyfiles.utilsvh())

        
        popup=QMessageBox()
        if out>0:
            popup.setText("Outputs generated")
            popup.setStandardButtons(QMessageBox.Ok)
            popup.exec_()
            out = 0 
            if self.ui.checkBox_16.isChecked() == True and self.ui.checkBox_15.isChecked() == True:
                popup.setText("Do you want to run the simulation script?")
                popup.setStandardButtons(QMessageBox.Yes|QMessageBox.No)
                popup.setIcon(QMessageBox.Question)
                simulate=popup.exec_()
                if simulate == QMessageBox.Yes:
                    subprocess.run('make',cwd=pathlib.Path(self.outpath))
                    simpath=pathlib.Path(self.outpath).joinpath('sim.txt')
                    self.verification(simpath)
        else :
            popup.setText("No checkbox selected")
            popup.setStandardButtons(QMessageBox.Ok)
            popup.setIcon(QMessageBox.Critical)
            popup.exec_()
    
    def inputName(self,state):
        if self.ui.checkBox_4.isChecked() == True:
            name, okPressed = QInputDialog.getText(self, "FPGA name","Enter FPGA name:", QLineEdit.Normal, self.defaultName)
            if okPressed:
                self.defaultName = name
            else:
                self.ui.checkBox_4.setCheckState(0)
    def verification(self,simpath):
        with open(simpath,'r') as f:
            content = f.readlines()
        l=0
        fail=[]
        faildetail="Failed at:"
        for i in content:
            l+=1
            if l>6:
                s=re.split(' +',i)
                if s[-2] == 'fail':
                    fail.append(l)
        failed=False
        p=(l-6)-len(fail)
        popup=QMessageBox()
        if len(fail)>0:
            popup.setText("Verification Failed")
            popup.setWindowTitle("Verification")
            popup.setStandardButtons(QMessageBox.Ok)
            popup.setIcon(QMessageBox.Critical)
            popup.setInformativeText('Test cycles Passed: {}\nTest cycles Failed: {}'.format(p,len(fail)))
            for i in fail:
                faildetail+='\nline, {}'.format(i)
            popup.setDetailedText(faildetail)
            popup.exec_()
        else:
            popup.setText("Verification Passed")
            popup.setWindowTitle("Verification")
            popup.setStandardButtons(QMessageBox.Ok)
            popup.setIcon(QMessageBox.Information)
            popup.setInformativeText('Test cycles Passed: {}'.format(p))
            popup.exec_()
    
    def simulation(self):
        filename = QFileDialog.getExistingDirectory(None,"Select Block Ram Folder")
        #print(pathlib.Path(filename).joinpath('Makefile').is_file())
        if pathlib.Path(filename).joinpath('Makefile').is_file():
            subprocess.run('make',cwd=pathlib.Path(filename))
            simpath=pathlib.Path(filename).joinpath('sim.txt')
            popup=QMessageBox()
            popup.setText("Simulation Completed")
            popup.setWindowTitle("Simulation")
            popup.setStandardButtons(QMessageBox.Ok)
            popup.exec_()
            self.verification(simpath)
        else:
            popup=QMessageBox()
            popup.setText("No simulation script found")
            popup.setStandardButtons(QMessageBox.Ok)
            popup.setIcon(QMessageBox.Critical)
            popup.exec_()
    def verify(self):
        filename=QFileDialog.getOpenFileName(None,"Select Sim.txt file")
        try:
            self.verification(filename[0])
        except:
            popup=QMessageBox()
            popup.setText("No Sim.txt found")
            popup.setStandardButtons(QMessageBox.Ok)
            popup.setIcon(QMessageBox.Critical)
            popup.exec_()
    def add_menu(self,data,menu_obj):
        if isinstance(data,list):
                for element in data:
                    print("element",element)
                    self.add_menu(element,menu_obj)
        else:
                action = menu_obj.addAction(data)
                action.setIconVisibleInMenu(False)
    
    def fnc(self,x):
        if x == 'Simulate':
            print("sim")
            self.simulation()
        if x == 'Verify':
            print("ver")
            self.verify()
    def aboutMerl(self):
        webbrowser.open('https://merledupk.org/')
    def UserManual(self):
        webbrowser.open_new(str(pathlib.Path(__file__).parent.absolute().joinpath('Block_RAM_Generator_User_Guide.pdf')))


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    application = window()
    application.showMaximized()
    sys.exit(app.exec())

    # def changeWin():
    #         label.hide()
    #         MainWindow.show()
    # import sys
    # app = QtWidgets.QApplication(sys.argv)
    # MainWindow = QtWidgets.QMainWindow()
    # file = QFile(":/light.qss")
    # file.open(QFile.ReadOnly | QFile.Text)
    # stream = QTextStream(file)
    # app.setStyleSheet(stream.readAll())
    # ui = Ui_MainWindow()
    # ui.setupUi(MainWindow)
    # label = QtWidgets.QLabel()
    # pixmap = QtGui.QPixmap(str(pathlib.Path(__file__).parent.absolute().joinpath('splash2.png')))
    # label.setPixmap(pixmap)
    # label.setWindowFlags(QtCore.Qt.SplashScreen| QtCore.Qt.FramelessWindowHint)
    # label.setScaledContents(True)
    # label.show()
    # QtCore.QTimer.singleShot(2000,changeWin)
    # resolution = QDesktopWidget().screenGeometry()
    # MainWindow.move(int((resolution.width() / 2) - (MainWindow.frameSize().width() / 2)),int((resolution.height() / 2) - (MainWindow.frameSize().height() / 2)))
    # sys.exit(app.exec_())
