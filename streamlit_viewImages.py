import matplotlib.pyplot as plt
import numpy as np
import os
import streamlit as st
from skimage.color import hsv2rgb

st.title ("View Tifs App")

#Lists of parameters to chose from 
Lstains = (os.listdir ("E:\\Immunfluoreszenz\\rDRG_CCI_d7\\Tifs"))
Lrats = (os.listdir ("E:\\Immunfluoreszenz\\rDRG_CCI_d7\\Tifs\\1-NF_GFAP_Iba1"))
Ldrg = ["CL\\L4", "CL\\L5" , "IL\\L4" , "IL\\L5"]

#include selectboxes for each parameters on the sidebar 
staining = st.sidebar.selectbox ("Select a staining" , Lstains)
#rat = st.sidebar.selectbox ("Select a rat" , Lrats)
drg = st.sidebar.selectbox ("Select a DRG" , Ldrg)
ratnr = str (st.sidebar.slider ("Ratnumber" , 2 , 7))

#generate the path for the image (rootpath)
selectedpath = os.path.join ("E:\\Immunfluoreszenz\\rDRG_CCI_d7\\Tifs" , staining + "\\R" + ratnr , drg)
Lallsubdirs = os.listdir (selectedpath)
Lsubdir = [i  for i in Lallsubdirs if "_pred" not in i ] # List of available markers 

subdir = st.sidebar.selectbox ("Select a Marker" , Lsubdir)
subpath = os.path.join (selectedpath , subdir)

#List of filenames, chose image number by slider 
Lfiles = os.listdir (subpath)
fileanz = len (Lfiles)
filenr =st.sidebar.slider ("Select Image Number" , 1 , fileanz)

#final path, read image
imgpath = subpath + "\\" + format (filenr , "04d") + ".tif"
maskpath = os.path.join (subpath + "_pred\\masks\\" + format (filenr , "04d") + ".png")
st.write (imgpath)
st.write (maskpath)

img = plt.imread (imgpath)
img = (img - np.min(img))/np.ptp(img)

#Brightness and Contrast adjustments 
gain = st.sidebar.slider ( "Gain" , 0.0 , 3.0 , 1.0)
bias = st.sidebar.slider ( "Brightness" , 0.0 , 0.5 , 0.1)
img = np.clip ( img * gain + bias , 0 , 1)


try: 
    mask = plt.imread (maskpath)
    #insert mask, HSV colors
    mask_template = np.zeros([img.shape[0], img.shape[1], 3])
    mask_template[..., 2] = img
    mask_template[..., 1] = mask
    mask_template[..., 0] = 0.5
    overlay = hsv2rgb(mask_template)
    #insert checkboxes to select what to show
    right , left = st.sidebar.columns (2)
    img_mask = right.checkbox ("Overlay")
    showmask = left.checkbox ("Show mask") 
    #Scheme which image to show, dependent on checkboxes (Mask/ Image/ Overlay)
    if img_mask:
        if showmask: 
            colr , coll = st.columns (2)
            coll.image (overlay)
            colr.image (mask)
        else: 
            st.image (overlay)
    elif showmask : 
        colr , coll = st.columns (2)
        coll.image (img)
        colr.image (mask)
    else:
        st.image (img)
except :
    st.image (img)
