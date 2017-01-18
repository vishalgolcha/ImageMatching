import  sys
from string import split
from os.path import basename
import eigenfaces


class PyFaces:
    def __init__(self,testimg,imgsdir,egfnum,thrsh):
        self.testimg=testimg
        self.imgsdir=imgsdir
        self.threshold=thrsh
        self.egfnum=egfnum        
        parts = split(basename(testimg),'.')
        extn=parts[len(parts) - 1]
        print "to match:",self.testimg," to all ",extn," images in directory:",imgsdir        
        self.facet= eigenfaces.FaceRec()
        self.egfnum=self.set_selected_eigenfaces_count(self.egfnum,extn)
        print "number of eigenfaces used:",self.egfnum
        self.facet.checkCache(self.imgsdir,extn,self.imgnamelist,self.egfnum,self.threshold)
        mindist,matchfile=self.facet.findmatchingimage(self.testimg,self.egfnum,self.threshold)
        if mindist < 1e-10:
            mindist=0
        if not matchfile:
            print "NOMATCH! try higher threshold"
        else:
            print "matches :"+matchfile+" dist :"+str(mindist)
            
    def set_selected_eigenfaces_count(self,selected_eigenfaces_count,ext):        
        #call eigenfaces.parsefolder() and get imagenamelist        
        self.imgnamelist=self.facet.parsefolder(self.imgsdir,ext)                    
        numimgs=len(self.imgnamelist)        
        if(selected_eigenfaces_count >= numimgs  or selected_eigenfaces_count == 0):
            selected_eigenfaces_count=numimgs/2    
        return selected_eigenfaces_count
        
        
##if __name__ == "__main__":
##    import time
##    try:
##        start = time.time()
##        argsnum=len(sys.argv)
##        print "args:",argsnum
##        if(argsnum<5):
##            print "usage:python pyfaces.py imgname dirname numofeigenfaces threshold "
##            sys.exit(2)                
##        imgname=sys.argv[1]
##        dirname=sys.argv[2]
##        egfaces=int(sys.argv[3])
##        thrshld=float(sys.argv[4])
##        pyf=PyFaces(imgname,dirname,egfaces,thrshld)
##        end = time.time()
##        print 'took :',(end-start),'secs'
##    except Exception,detail:
##        print detail.args
##        print "usage:python pyfaces.py imgname dirname numofeigenfaces threshold "
