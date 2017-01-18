
from Tix import ExFileSelectBox,DirSelectBox
from Tkinter import *
from tkFont import Font
from os.path import join,basename

import ImageTk

#constants
txt_width=4
txt_height=1
button_width=6
button_padx="2m"
button_pady="1m"
label_padx="2m"

txtframe_padx="3m"
txtframe_pady="2m"
txtframe_ipadx="3m"
txtframe_ipady="1m"

class PyFaceUI(object):
    def __init__(self,parent,controller):
        self.controller=controller
        self.makeFrames(parent)
        self.makeLabels()
        self.thrctrlv=DoubleVar()
        self.fspctrlv=IntVar()
        self.makeTextFields()
        self.setInitialValues()
        self.makeCanvases()
        self.makeButtons()
        self.makeSelectionWidgets()
        self.msgfont=Font(family="Times", weight="bold")         

    def makeFrames(self,parent):
        self.myParent = parent   
        self.mainframe = Frame(parent,background="grey")
        self.mainframe.pack(fill=BOTH,expand=YES)
        
        self.leftFrame=Frame(self.mainframe,background="grey",borderwidth=5,relief=RIDGE,height=3000,width=2000)
        self.leftFrame.pack(side=LEFT,fill=BOTH,expand=YES)
        self.imgSelectFrame=Frame(self.leftFrame,background="grey",borderwidth=5,height=1000,width=400)
        self.imgSelectFrame.pack(side=TOP,fill=BOTH,expand=YES)
        self.dirSelectFrame=Frame(self.leftFrame,background="grey",borderwidth=5,height=1000,width=400)
        self.dirSelectFrame.pack(side=TOP,fill=BOTH,expand=YES)
        self.rtFrame=Frame(self.mainframe,background="grey",borderwidth=5,relief=RIDGE,height=3000,width=2000)
        self.rtFrame.pack(side=LEFT,fill=BOTH,expand=YES,padx=txtframe_padx,pady=txtframe_pady,ipadx=txtframe_ipadx ,ipady=txtframe_ipady)
        self.entryFrame=Frame(self.rtFrame,background="grey",borderwidth=5,height=200,width=50)
        self.entryFrame.pack(side=TOP,fill=BOTH,expand=YES)
        self.canvFrame=Frame(self.rtFrame,background="black",borderwidth=5,height=350,width=450)
        self.canvFrame.pack(side=TOP,fill=BOTH,expand=YES)
        self.resultFrame=Frame(self.rtFrame,background="black",borderwidth=5,height=100,width=450)
        self.resultFrame.pack(side=TOP,fill=BOTH,expand=YES)        
        self.btnFrame=Frame(self.rtFrame,background="grey",borderwidth=5,height=100,width=450)
        self.btnFrame.pack(side=TOP,fill=BOTH,expand=YES)
        
    def makeLabels(self):
        self.imgSelLabel=Label(self.imgSelectFrame,text="Select image to check")
        self.imgSelLabel.pack(side=LEFT)        
        self.dirSelLabel=Label(self.dirSelectFrame,text="Select folder of images")
        self.dirSelLabel.pack(side=LEFT)
        self.thresholdLabel=Label(self.entryFrame,text="Threshold:",padx=label_padx)
        self.thresholdLabel.grid(row=0,column=0)
        self.eigenfacesLabel=Label(self.entryFrame,text=" Eigenfaces:  ")
        self.eigenfacesLabel.grid(row=1,column=0) 
    
    def makeTextFields(self):
        self.thresholdTxt=Entry(self.entryFrame,width=txt_width,textvariable=self.thrctrlv)
        self.thresholdTxt.grid(row=0,column=1)
        self.eigenfacesTxt=Entry(self.entryFrame,width=txt_width,textvariable=self.fspctrlv)
        self.eigenfacesTxt.grid(row=1,column=1)
        
    def makeCanvases(self):
        self.canvorig=Canvas(self.canvFrame,relief=RIDGE,width=140,height=200)
        self.canvorig.pack(side=LEFT)
        self.canvresult=Canvas(self.canvFrame,relief=RIDGE,width=140,height=200)
        self.canvresult.pack(side=RIGHT)        
        self.resultdisplay=Canvas(self.resultFrame,background="grey",relief=RAISED,width=280,height=100)
        self.resultdisplay.grid(row=2,column=2)
        
    def makeButtons(self):
        self.okButton = Button(self.btnFrame)
        self.okButton.configure(width=button_width,text="Match",command=self.okButtonClick,padx=button_padx,pady=button_pady,anchor=W,disabledforeground="tan")        
        self.okButton.pack(side=LEFT )
        self.qtButton = Button(self.btnFrame)
        self.qtButton.configure(width=button_width,text="Quit",command=self.quitButtonClick,padx=button_padx,pady=button_pady,anchor=E)       
        self.qtButton.pack(side=RIGHT )
        
    def makeSelectionWidgets(self):        
        self.imgsel=ExFileSelectBox(self.imgSelectFrame)        
        self.imgsel.pack(side=LEFT)
        self.dirsel=DirSelectBox(self.dirSelectFrame) 
        self.dirsel.pack(side=LEFT)        
        
    
    def displayResultImage(self):
        self.canvresult.delete(ALL)
        self.canvresult.create_image(70, 100, image=self.resimg)

    def displayResultMessage(self, message, msgcolor):
        self.resultdisplay.delete(ALL)
        self.resultdisplay.create_text(1, 40, anchor=W, text=message, fill=msgcolor, font=self.msgfont, width=280)

    def getNumberOfEigenfaces(self):
        txt = self.eigenfacesTxt.get()
        selectedEigenFaces = int(txt)
        return selectedEigenFaces

    def getThresholdValue(self):
        txt = self.thresholdTxt.get()
        thresholdvalue = float(txt)
        return thresholdvalue

    def getSelectedDirectoryName(self):
        selectedDirectoryName = self.dirsel.cget("value")
        return selectedDirectoryName

    def getSelectedFileName(self):           
        selectedFileName = self.imgsel.cget("value")      
        self.imgsel.selection_clear()
        return selectedFileName

    def clearAllCanvas(self):
        self.canvorig.delete(ALL)
        self.canvresult.delete(ALL)
        self.resultdisplay.delete(ALL)        
    
    def okButtonClick(self):
        self.okButton.configure(state=DISABLED)
        self.clearAllCanvas()        
        selectedFileName = self.getSelectedFileName()
        selectedDirectoryName = self.getSelectedDirectoryName()
        thresholdvalue = self.getThresholdValue()
        selectedEigenFaces = self.getNumberOfEigenfaces() 
        self.showSelectedImage(selectedFileName)       
        self.controller.validateSelection(selectedFileName,selectedDirectoryName,selectedEigenFaces,thresholdvalue)
        
                
    def showSelectedImage(self,imageName):        
        if(not imageName is ''):        
            self.selimg=ImageTk.PhotoImage(file=imageName)
            self.selimgtag=self.canvorig.create_image(70,100,image=self.selimg)
            self.canvorig.update_idletasks()
                
    def setInitialValues(self):
        self.fspctrlv.set(6)
        self.thrctrlv.set(2.0)    
    
    def updateDisplay(self,error,numOfEigenfaces,matchfile,mindist):
        if error:
            print 'updateDisplay()::error'
            message=error.message
            msgcolor='red'
        else:
            print 'updateDisplay()::NO error'
            matchfilename=basename(matchfile)            
            message="matches "+matchfilename+" at distance ="+str(mindist)
            msgcolor='blue'
            try:
                self.resimg=ImageTk.PhotoImage(file=matchfile)
            except Exception, inst:
                print 'failed to create PhotoImage'
                print inst.message
            else:
                self.displayResultImage()
        self.setNumOfEigenfaces(numOfEigenfaces)
        self.displayResultMessage(message, msgcolor)
        self.okButton.configure(state=NORMAL)      
              
    def setNumOfEigenfaces(self,numOfEigenfaces):
        self.fspctrlv.set(numOfEigenfaces)        
        self.eigenfacesTxt.update_idletasks()        
            
    def quitButtonClick(self):
        self.myParent.destroy()
                
class NoFileSelectError(Exception):
    pass

class NoDirSelectError(Exception):
    pass

