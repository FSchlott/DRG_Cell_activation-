import numpy as np

class GroupData:
    def __init__ (self, results_file , drg_side , anz_rats ): #json file with data from each image, IL/CL, number of rats
        self.results_file = results_file
        self.drg_side = drg_side

        self.name = "d7cci" + drg_side
        #adds the means of all drgs to a list
        self.get_means_for_allrats (anz_rats)


    def get_means_for_allrats (self, anz_rats):
        self.abca1_area_allrats = [] 
        self.abca1_intensity_allrats = []
        self.abca1_intensity_per_area_allrats = []
        self.gs_area_allrats = []
        self.gs_intensity_allrats = []
        self.gs_intensity_per_area_allrats = []
        self.ib4_area_allrats = []
        self.ib4_intensity_allrats = []
        self.ib4_intensity_per_area_allrats = []
        self.abca1_only_area_allrats = []
        self.abca1_only_intensity_allrats = []
        self.abca1_only_intensity_per_area_allrats = []
        self.gs_only_area_allrats = []
        self.gs_only_intensity_allrats = []
        self.gs_only_intensity_per_area_allrats = []
        self.abca1_gs_ov_area_allrats = []
        self.abca1_gs_ov_intensity_allrats = []
        self.abca1_gs_ov_intensity_per_area_allrats = []
        self.gs_per_nra_allrats = []

        self.abca1_anz_allrats = []
        self.gs_anz_allrats = []
        self.ib4_anz_allrats = []
    
        self.gs_expressing_abca1_allrats = []
        self.abca1_expressing_gs_allrats = []

        ##group is either IL or CL 
        for drg in self.results_file:
            if self.drg_side in drg["group"]:
                self.get_means_perdrg (drg)

    ##calculates the mean values per DRG    
    def get_means_perdrg (self, drg):  
        self.abca1_area_allrats.append (np.mean(drg ["abca1_area"])) 
        self.abca1_intensity_allrats.append (np.mean(drg ["abca1_intensity"]))
        self.abca1_intensity_per_area_allrats.append (np.mean (drg ["abca1_intensity_per_area"]))
        self.gs_area_allrats.append (np.mean(drg ["gs_area"]))
        self.gs_intensity_allrats.append (np.mean(drg ["gs_intensity"]))
        self.gs_intensity_per_area_allrats.append (np.mean (drg ["gs_intensity_per_area"]))
        self.ib4_area_allrats.append (np.mean(drg ["ib4_intensity"]))
        self.ib4_intensity_allrats.append (np.mean(drg ["ib4_intensity"]))
        self.ib4_intensity_per_area_allrats.append (np.mean (drg ["ib4_intensity_per_area"]))
        self.abca1_only_intensity_allrats.append (np.mean(drg ["abca1_only_intensity"]))
        self.abca1_only_intensity_per_area_allrats.append (np.mean (drg ["abca1_only_intensity_per_area"]))
        self.abca1_gs_ov_intensity_allrats.append (np.mean(drg ["abca1_gs_ov_intensity"]))
        self.abca1_gs_ov_intensity_per_area_allrats.append (np.mean (drg ["abca1_gs_ov_intensity_per_area"]))

        self.abca1_anz_allrats.append (np.mean (drg["abca1_anz"]))
        self.gs_anz_allrats.append (np.mean (drg["gs_anz"]))
        self.ib4_anz_allrats.append (np.mean (drg["ib4_anz"]))

        self.gs_expressing_abca1_allrats.append (np.mean (drg ["gs_expressing_abca1"]))
        self.abca1_expressing_gs_allrats.append (np.mean (drg ["abca1_expressing_gs"]))
        
        self.gs_per_nra_allrats.append (np.mean(drg ["gs_per_nra"]))


