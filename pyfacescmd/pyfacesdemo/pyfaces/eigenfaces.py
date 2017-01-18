from numpy import max
from numpy import zeros
from numpy import average
from numpy import dot
from numpy import asfarray
from numpy import sort
from numpy import trace
from numpy import argmin
from numpy.linalg import *

from os.path import isdir,join,normpath
from os import listdir,mkdir
from shutil import rmtree
import pickle
from math import sqrt

import imageops

class ImageError(Exception):
    pass

class DirError(Exception):
    pass 
class FaceBundle:
    def __init__(self,imglist,wd,ht,adjfaces,fspace,avgvals,evals):
        self.imglist=imglist
        self.wd=wd
        self.ht=ht
        self.adjfaces=adjfaces
        self.eigenfaces=fspace
        self.avgvals=avgvals
        self.evals=evals
        
class FaceRec:    
    def validateselectedimage(self,imgname):                     
        selectimg=imageops.XImage(imgname)
        selectwdth=selectimg._width
        selectht=selectimg._height        
        if((selectwdth!=self.bundle.wd) or (selectht!=self.bundle.ht)):
            raise ImageError("select image of correct size !")
        else:
            return selectimg
        
    def findmatchingimage(self,imagename,selectedfacesnum,thresholdvalue):        
        selectimg=self.validateselectedimage(imagename)
        inputfacepixels=selectimg._pixellist
        inputface=asfarray(inputfacepixels)
        pixlistmax=max(inputface)
        inputfacen=inputface/pixlistmax        
        inputface=inputfacen-self.bundle.avgvals
        usub=self.bundle.eigenfaces[:selectedfacesnum,:]
        input_wk=dot(usub,inputface.transpose()).transpose()        
        dist = ((self.weights-input_wk)**2).sum(axis=1)
        idx = argmin(dist)
        mindist=sqrt(dist[idx])
        result=""
        if mindist < thresholdvalue:
            result=self.bundle.imglist[idx]
        print "try reconstruction"
        self.reconstructfaces(selectedfacesnum)
        return mindist,result
        
    def doCalculations(self,dir,imglist,selectednumeigenfaces):                
        self.createFaceBundle(imglist);        
        egfaces=self.bundle.eigenfaces
        adjfaces=self.bundle.adjfaces
        self.weights=self.calculateWeights(egfaces,adjfaces,selectednumeigenfaces)
        
        #write to cache
        cachefile=join(dir,"saveddata.cache")
        f2=open(cachefile,"w")
        pickle.dump(self.bundle,f2)
        f2.close()
        
    def validateDirectory(self,imgfilenameslist):                
        if (len(imgfilenameslist)==0):
            print "folder empty!"
            raise DirError("folder empty!")
        imgfilelist=[]
        for z in imgfilenameslist:
            img=imageops.XImage(z)
            imgfilelist.append(img)        
        sampleimg=imgfilelist[0]
        imgwdth=sampleimg._width
        imght=sampleimg._height        
        #check if all images have same dimensions
        for x in imgfilelist:
            newwdth=x._width
            newht=x._height
            if((newwdth!=imgwdth) or (newht!=imght)):
                raise DirError("select folder with all images of equal dimensions !")
        return imgfilelist
    
    def calculateWeights(self,eigenfaces,adjfaces,selectedfacesnum):                       
        usub=eigenfaces[:selectedfacesnum,:]        
        wts=dot(usub,adjfaces.transpose()).transpose()                         
        return wts           
            
    def createFaceBundle(self,imglist):                
        imgfilelist=self.validateDirectory(imglist)        
        img=imgfilelist[0]
        imgwdth=img._width
        imght=img._height
        numpixels=imgwdth * imght
        numimgs=len(imgfilelist)               
        #trying to create a 2d array ,each row holds pixvalues of a single image
        facemat=zeros((numimgs,numpixels))               
        for i in range(numimgs):
            pixarray=asfarray(imgfilelist[i]._pixellist)
            pixarraymax=max(pixarray)
            pixarrayn=pixarray/pixarraymax                        
            facemat[i,:]=pixarrayn           
        
        #create average values ,one for each column(ie pixel)        
        avgvals=average(facemat,axis=0)        
        #make average faceimage in currentdir just for fun viewing..
        imageops.make_image(avgvals,"average.png",(imgwdth,imght))               
        #substract avg val from each orig val to get adjusted faces(phi of T&P)     
        adjfaces=facemat-avgvals        
                
        adjfaces_tr=adjfaces.transpose()
        
        L=dot(adjfaces , adjfaces_tr)

        evals1,evects1=eigh(L)
        #to use svd ,comment out the previous line and uncomment the next
        #evects1,evals1,vt=svd(L,0)        
        reversedevalueorder=evals1.argsort()[::-1]
        evects=evects1[:,reversedevalueorder]               
        evals=sort(evals1)[::-1]                
        #rows in u are eigenfaces        
        u=dot(adjfaces_tr,evects)
        u=u.transpose()               
        #NORMALISE rows of u
        for i in range(numimgs):
            ui=u[i]
            ui.shape=(imght,imgwdth)
            norm=trace(dot(ui.transpose(), ui))            
            u[i]=u[i]/norm        
        
        self.bundle=FaceBundle(imglist,imgwdth,imght,adjfaces,u,avgvals,evals)
        self.createEigenimages(u)# eigenface images
        
    
    def parsefolder(self,dirname,extn):                
        if not isdir(dirname): return
        imgfilenameslist=sorted([
            normpath(join(dirname, fname))
            for fname in listdir(dirname)
            if fname.lower().endswith('.'+extn)            
            ])        
        return imgfilenameslist
    
    def reconstructfaces(self,selectedfacesnum):        
        #reconstruct                  
        recondir='../reconfaces'
        newwt=zeros(self.weights.shape)
        eigenfaces=self.bundle.eigenfaces
        usub=eigenfaces[:selectedfacesnum,:]
        evals=self.bundle.evals
        evalssub=evals[:selectedfacesnum]        
        for i in range(len(self.weights)):
            for j in range(len(evalssub)):        
                newwt[i][j]=self.weights[i][j]*evalssub[j]        
        phinew=dot(newwt,usub)    
        
        xnew=phinew+self.bundle.avgvals
        if isdir(recondir):                             
            rmtree(recondir,True)
        mkdir(recondir)
        print "made:",recondir
        numimgs=len(self.bundle.imglist)
        for x in range(numimgs):
            imgname=recondir+"/reconphi"+str(x)+".png" 
            imgdata=phinew[x]           
            imageops.make_image(imgdata,imgname,(self.bundle.wd,self.bundle.ht),True)
            
        for x in range(numimgs):
            filename=recondir+"/reconx"+str(x)+".png"
            imgdata=xnew[x]
            imageops.make_image(imgdata,filename,(self.bundle.wd,self.bundle.ht),True)
    
    def createEigenimages(self,eigenspace):                
        egndir='../eigenfaces'        
        if isdir(egndir):                
            rmtree(egndir,True)               
        mkdir(egndir)            
        numimgs=len(self.bundle.imglist)
        for x in range(numimgs):
            imgname=egndir+"/eigenface"+str(x)+".png"            
            imageops.make_image(eigenspace[x],imgname,(self.bundle.wd,self.bundle.ht))
    
    def checkCache(self,dir,ext,imglist,selectedfacesnum,thrval):        
        cachefile=join(dir,"saveddata.cache")
        cache_changed=True
        try:
            f=open(cachefile)
        except IOError:
            print "no cache file"            
            self.doCalculations(dir,imglist,selectedfacesnum)
        else:
            print "cache file exists"
            self.bundle=pickle.load(f)            
            oldlist=self.bundle.imglist            
            if(imglist==oldlist):
                print 'both sets same'
                cache_changed=False
                eigenfaces=self.bundle.eigenfaces
                adjfaces=self.bundle.adjfaces                             
                self.weights=self.calculateWeights(eigenfaces,adjfaces,selectedfacesnum);
            if(cache_changed):
                print "folder changed!!"                
                self.doCalculations(dir,imglist,selectedfacesnum)
            f.close()
            
