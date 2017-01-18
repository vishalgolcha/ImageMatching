import pyfacesgui
import pyeigenfaces
from Tix import Tk
from os.path import basename
from string import split

class PyFaceController(object):
    def __init__(self):
        self.facerec=pyeigenfaces.FaceRec()
            
    def getExtension(self,fileName):
        parts = split(basename(fileName),'.')
        extension=parts[len(parts) - 1]
        return extension
    def validateSelection(self,fileName,directoryName,numOfEigenfaces,thresholdVal):
        if fileName is '':
            print 'validateSelection()::no file selected!!'
            error=pyfacesgui.NoFileSelectError('no file selected')
            self.updateResults(error)
        elif directoryName is '':
            print 'validateSelection()::no directory selected!!'
            error=pyfacesgui.NoDirSelectError('no directory selected')
            self.updateResults(error)
        else:
            extension=self.getExtension(fileName)            
            dirParser=pyeigenfaces.DirectoryParser(directoryName)
            imagefilenames=dirParser.parseDirectory(extension)            
            if(not self.facerec.isValid(numOfEigenfaces,len(imagefilenames))):
                numOfEigenfaces=len(imagefilenames)/2                                
            try:
                self.recogniseFace(imagefilenames,fileName,directoryName,numOfEigenfaces,thresholdVal)
            except Exception,inst:
                self.updateResults(inst,numOfEigenfaces)        
    
    def recogniseFace(self,imagefilenames,selectedFileName,selectedDirectory,numOfEigenfaces,thresholdVal):
        self.facerec.checkCache(selectedDirectory,imagefilenames,numOfEigenfaces)
        mindist,matchfile=self.facerec.findMatchingImage(selectedFileName,numOfEigenfaces,thresholdVal)
        self.processMatchResult(matchfile,mindist,numOfEigenfaces)        
    
    def processMatchResult(self,matchfile,mindist,numOfEigenfaces):
        if not matchfile:
            error=pyeigenfaces.NoMatchError('No match! try higher threshold')            
            self.updateResults(error,numOfEigenfaces)
        else:
            print "processMatchResult()::matches :"+matchfile+" dist :"+str(mindist)#            
            self.updateResults(None,numOfEigenfaces,matchfile,mindist) 
        
    def updateResults(self,error,numOfEigenfaces=0,matchfile='',mindist=0.0):
        self.myapp.updateDisplay(error,numOfEigenfaces,matchfile,mindist)        
        
if __name__ == "__main__":
    controller=PyFaceController()    
    root = Tk()
    root.wm_title("PyFaces")
    controller.myapp =pyfacesgui.PyFaceUI(root,controller)
    root.mainloop()
    
 
    
    
    
