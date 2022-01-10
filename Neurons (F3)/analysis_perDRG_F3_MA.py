import numpy as np

class GroupData:
    def __init__ (self, results_file , drg_side , anz_rats ): #json file with data from each image, IL/CL, number of rats
        self.results_file = results_file
        self.drg_side = drg_side

        self.name = "d7cci" + drg_side
        #adds the means of all drgs to a list 
        self.get_means_for_allrats (anz_rats)


    
    def get_means_for_allrats (self, anz_rats):
        self.atf3_per_nf_allrats = [] 
        self.atf3_per_ib4_allrats = []
        self.ib4_per_nf_allrats = []
        self.ib4_per_atf3_allrats = []
        self.nf_anz_allrats = []
        self.atf3_anz_allrats = []        
        self.ib4_anz_allrats = []


        #group is either IL or CL   
        for drg in self.results_file:
            if self.drg_side in drg["group"]:
                self.get_means_perdrg (drg)

    #calculate mean per parameter list per DRG  
    def get_means_perdrg (self, drg): 
        self.atf3_per_nf_allrats.append (np.mean(drg ["atf3_per_nf"]))
        self.atf3_per_ib4_allrats.append (np.mean (drg ["atf3_per_ib4"]))
        self.ib4_per_nf_allrats.append (np.mean (drg ["ib4_per_nf"]))
        self.ib4_per_atf3_allrats.append (np.mean (drg ["ib4_per_atf3"]))
        self.nf_anz_allrats.append (np.mean (drg ["nf_anz"]))
        self.ib4_anz_allrats.append (np.mean (drg ["ib4_anz"]))
        self.atf3_anz_allrats.append (np.mean (drg ["atf3_anz"]))


