import matplotlib.pyplot as plt
import numpy as np
from tqdm.auto import tqdm
import os
from skimage import measure
from skimage.morphology import disk
from skimage.morphology import binary_dilation

class ImageData : 
    def __init__ (self, subdir):
        abca1mask_paths = os.path.join(subdir, 'abca1_pred/masks')
        gsmask_paths = os.path.join(subdir, 'gs_pred/masks')
        ib4mask_paths = os.path.join(subdir, 'ib4_pred/masks')  
        abca1img_paths = os.path.join(subdir, 'abca1')
        #intensities and area for each segmentation 
        self.abca1_area_L = []
        self.abca1_intensity_per_area_L = []
        self.gs_area_L = []
        self.gs_intensity_per_area_L = []
        self.ib4_area_L = []
        self.ib4_intensity_per_area_L = []
        self.abca1_only_area_L = []
        self.abca1_only_intensity_per_area_L = []
        self.gs_only_area_L = []
        self.gs_only_intensity_per_area_L = []
        self.abca1_gs_ov_area_L = []

        self.abca1_gs_ov_intensity_per_area_L = []

        self.abca1_anz_L = []
        self.abca1_sizes_L = []
        self.gs_anz_L = []
        self.gs_sizes_L = []
        self.ib4_anz_L = []
        self.ib4_sizes_L = []

        #percentage of gs cells (area) that are ABCA1 positive (area) / vice versa
        self.gs_expressing_abca1_L = []
        self.abca1_expressing_gs_L = []
        #area of gs pre neuronrich area
        self.gs_per_nra_L = []

        for abca1M_filename , gsM_filename , ib4M_filename, abca1I_filename in tqdm(zip(os.listdir(abca1mask_paths), os.listdir(gsmask_paths),
                                          os.listdir(ib4mask_paths), os.listdir(abca1img_paths))):
                                    
            abca1M = plt.imread (os.path.join (abca1mask_paths, abca1M_filename))
            gsM = plt.imread (os.path.join (gsmask_paths, gsM_filename))
            ib4M = plt.imread (os.path.join (ib4mask_paths, ib4M_filename))
            abca1I = plt.imread (os.path.join (abca1img_paths, abca1I_filename))

            #calculates overlaps / no overlap per segmentation
            abca1_sub_gs = abca1M - gsM
            abca1_add_gs = abca1M + gsM
            abca1_add_ib4 = abca1M + ib4M

            gs_only = (abca1_sub_gs == -1)*1
            abca1_gs_overlap = (abca1_add_gs == 2)*1
            abca1_only = abca1M - abca1_gs_overlap
            abca1_ib4_overlap = (abca1_add_ib4 == 2)*1
            abca1_only = abca1M - abca1_ib4_overlap

            #execute functions
            abca1_area, abca1_intensity_per_area = self.get_abca1_intensities (abca1I, abca1M)
            gs_area, gs_intensity_per_area = self.get_abca1_intensities (abca1I, gsM)
            ib4_area, ib4_intensity_per_area = self.get_abca1_intensities (abca1I, ib4M)
            abca1_only_area, abca1_only_intensity_per_area = self.get_abca1_intensities (abca1I, abca1_only)
            gs_only_area, gs_only_intensity_per_area = self.get_abca1_intensities (abca1I, gs_only)
            abca1_gs_ov_area, abca1_gs_ov_intensity_per_area = self.get_abca1_intensities (abca1I, abca1_gs_overlap)

            abca1_anz , abca1_sizes =  self.get_cellnum_sizes (abca1M)
            gs_anz, gs_sizes = self.get_cellnum_sizes (gsM)
            ib4_anz, ib4_sizes = self.get_cellnum_sizes (ib4M)

            gs_expressing_abca1 = self.get_overlap_percent (abca1_gs_overlap, gsM)
            abca1_expressing_gs = self.get_overlap_percent (abca1_gs_overlap, abca1M)

            gs_per_nra = self.quantify_per_neuronarea (abca1M, gsM)

            #add values to list
            self.abca1_area_L.append  (float (abca1_area))
            self.abca1_intensity_per_area_L.append  (float (abca1_intensity_per_area))
            self.gs_area_L.append  (float (gs_area))
            self.gs_intensity_per_area_L.append  (float (gs_intensity_per_area))
            self.ib4_area_L.append  (float (ib4_area))
            self.ib4_intensity_per_area_L.append  (float (ib4_intensity_per_area))
            self.abca1_only_area_L.append  (float (abca1_only_area))
            self.abca1_only_intensity_per_area_L.append  (float (abca1_only_intensity_per_area))
            self.gs_only_area_L.append  (float (gs_only_area))
            self.gs_only_intensity_per_area_L.append  (float (gs_only_intensity_per_area))
            self.abca1_gs_ov_area_L.append  (float (abca1_gs_ov_area))
            self.abca1_gs_ov_intensity_per_area_L.append  (float (abca1_gs_ov_intensity_per_area))

            self.abca1_anz_L.append (float (abca1_anz))
            self.abca1_sizes_L.append (abca1_sizes) 
            self.gs_anz_L.append (float (gs_anz))
            self.gs_sizes_L.append (gs_sizes)
            self.ib4_anz_L.append (float(ib4_anz))
            self.ib4_sizes_L.append (ib4_sizes)

            self.gs_expressing_abca1_L.append (float (gs_expressing_abca1))
            self.abca1_expressing_gs_L.append (float (abca1_expressing_gs))

            self.gs_per_nra_L.append (float (gs_per_nra))
        

    def get_abca1_intensities (self , abca1I, mask) :
         #turn segmentation to bool, confine measured abca1 image to segmentation area 
         pos_image = (mask >0) *abca1I
         #calculate intensity sum per defined area
         intensity_sum = np.sum (pos_image)
         #calculate area (sum)
         area = np.sum (mask)
         #calculate intensity per area:
         intensity_per_area = intensity_sum / area
         return area, intensity_per_area

    def get_cellnum_sizes (self, mask):
        #label each image feature, get numbers and sizes 
        cell_L = []
        labels , anz = measure.label (mask , return_num = True)
        props = measure.regionprops (labels)
          
        for i in range (anz): 
            cell_L.append (float (props[i].area))
        c_num = len (cell_L)
        return c_num , cell_L

    def get_overlap_percent (self, ovM, allM): 
        #ovM= overlap , e.g. GS / ABCA1; allM = segmentation of the whole reference segmentation 
        overlap_percent = (np.sum (ovM)/ np.sum (allM))*100
        return overlap_percent

    def quantify_per_neuronarea (self, abca1M, qM) :
        #dilate image on teh edges so that neuron area cannot exceed image 
        abca1M_dil = np.zeros([abca1M.shape[0]+40, abca1M.shape[1]+40])
        abca1M_dil[20:-20, 20:-20] = abca1M        

        qM_dilated = np.zeros([qM.shape[0]+40, qM.shape[1]+40])
        qM_dilated[20:-20, 20:-20] = qM
        #designate neuronrich area 
        shape = disk (20)
        neuronarea = binary_dilation (abca1M, shape)
        #restric segmentation to neuronrich area
        addM = qM + neuronarea
        overlap = (addM == 2)*1
        #calculate area
        qsum = np.sum (overlap)
        nra_size = np.sum (neuronarea)
        per_nra = (qsum/nra_size)*100
        return per_nra






