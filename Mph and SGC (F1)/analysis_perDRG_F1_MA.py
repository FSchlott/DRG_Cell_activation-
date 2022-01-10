import numpy as np

class GroupData:
    def __init__ (self, results_file , drg_side , anz_rats ): #json file with data from each image, IL/CL, number of rats
        self.results_file = results_file
        self.drg_side = drg_side

        self.name = "d7cci" + drg_side

        self.get_means_for_allrats (anz_rats)


    #adds the means of all drgs to a list
    def get_means_for_allrats (self, anz_rats):
        self.iba1_per_nra_allrats = [] 
        self.gfap_per_nra_allrats = []
        self.iba1_anz_allrats = []
        self.gfap_anz_allrats = []
        self.iba1_anz_per_nra_allrats = []
        self.iba1_vol_per_anz_allrats = []
        self.gfap_anz_per_nra_allrats = []
        self.gfap_vol_per_anz_allrats = []
        self.iba1_um_allrats = []
        self.neuronarea_um_allrats = []

        self.iba1_per_nra_all_allrats = []
        self.gfap_per_nra_all_allrats = []


        #group is either IL or CL  
        for drg in self.results_file:
            if self.drg_side in drg["group"]:
                self.get_means_perdrg (drg)


    #calculates the mean values per DRG   
    def get_means_perdrg (self, drg):
        iba1_anz_per_nra_L = []
        iba1_vol_per_anz_L = []
        gfap_anz_per_nra_L = []
        gfap_vol_per_anz_L = []

        #Calculates Area per Cell and Cells per Area from Json
        for neuronarea, iba1_anz , iba1_um, gfap_anz, gfap_um in zip (drg ["neuronarea"], drg ["iba1_anz"], drg ["iba1_um"], drg ["gfap_anz"], drg ["gfap_um"]):
            gfap_anz_per_nra = (gfap_anz / neuronarea)*1000
            iba1_anz_per_nra = (iba1_anz / neuronarea)*1000
            if iba1_anz > 0 : 
                iba1_vol_per_anz = iba1_um / iba1_anz
            else:
                iba1_vol_per_anz = 0
            if gfap_anz > 0:
                gfap_vol_per_anz = gfap_um / gfap_anz
            else:
                gfap_vol_per_anz = 0

            iba1_anz_per_nra_L.append (iba1_anz_per_nra)
            iba1_vol_per_anz_L.append (iba1_vol_per_anz)
            gfap_anz_per_nra_L.append (gfap_anz_per_nra)
            gfap_vol_per_anz_L.append (gfap_vol_per_anz)

        iba1_per_nra_L = []
        gfap_per_nra_L = []

        for iba1_per_nra, gfap_per_nra in zip (drg ["iba1_per_neuronricharea"], drg ["gfap_per_neuronricharea"]):
            iba1_per_nra_L.append (iba1_per_nra)
            gfap_per_nra_L.append (gfap_per_nra)

        for i in iba1_per_nra_L : #to generate a List with all values instead of a list of lists
            self.iba1_per_nra_all_allrats.append (i)
        for i in gfap_per_nra_L:
            self.gfap_per_nra_all_allrats.append (i)

        self.iba1_per_nra_allrats.append (np.mean(drg ["iba1_per_neuronricharea"]))
        self.gfap_per_nra_allrats.append (np.mean (drg ["gfap_per_neuronricharea"]))
        self.iba1_anz_allrats.append (np.mean (drg ["iba1_anz"]))   
        self.gfap_anz_allrats.append (np.mean (drg ["gfap_anz"]))
        self.iba1_anz_per_nra_allrats.append (np.mean (iba1_anz_per_nra_L))
        self.iba1_vol_per_anz_allrats.append (np.mean (iba1_vol_per_anz_L))
        self.gfap_anz_per_nra_allrats.append (np.mean (gfap_anz_per_nra_L))
        self.gfap_vol_per_anz_allrats.append (np.mean (gfap_vol_per_anz_L))
        self.iba1_um_allrats.append (np.mean (drg ["iba1_um"]))
        self.neuronarea_um_allrats.append (np.mean (drg ["neuronarea"]))





