import numpy as np

class GroupData:
    def __init__ (self, results_file , drg_side , anz_rats ): #json file with data from each image, IL/CL, number of rats
        self.results_file = results_file
        self.drg_side = drg_side

        self.name = "d7cci" + drg_side
        #adds the means of all drgs to a list
        self.get_numbers_from_allrats (anz_rats)

    def get_numbers_from_allrats (self, anz_rats):
        self.nf_sizecounts_allrats = []
        self.binsizes = None
        self.ib4_sizecounts_allrats = []
        self.atf3_sizecounts_allrats = []

        #group is either IL or CL  
        for drg in self.results_file:
            if self.drg_side in drg["group"]:
                self.get_numbers_perdrg (drg)

    #calculates the mean values per DRG   
    def get_numbers_perdrg (self, drg): #see get_hist_data
        nf_sizecounts , ib4_sizecounts , atf3_sizecounts , binsizes = self.get_hist_data (drg)


        self.nf_sizecounts_allrats.append (np.mean(nf_sizecounts, axis = 0).tolist())
        self.binsizes = binsizes
        self.ib4_sizecounts_allrats.append (np.mean(ib4_sizecounts, axis = 0).tolist())
        self.atf3_sizecounts_allrats.append (np.mean(atf3_sizecounts, axis = 0).tolist())
        

    def get_hist_data (self, drg):
        nf_sizecounts = []
        ib4_sizecounts = []
        atf3_sizecounts = []
        for nf_sizes_px, nf_anz , ib4_sizes_px, atf3_sizes_px in zip (drg ["nf_sizes"], drg ["nf_anz"], drg ["ib4_sizes"], drg ["atf3_sizes"] ):
            if nf_anz > 0: #only collects data from images containing any neurons
                #get sizes in um^2 from px (-->  1 px^2 = 0.814um2)
                nf_sizes = np.array(nf_sizes_px)*0.814
                nf_sizes [nf_sizes>3000] = 3000
                ib4_sizes = np.array(ib4_sizes_px)*0.814
                ib4_sizes [ib4_sizes>3000] = 3000
                atf3_sizes = np.array(atf3_sizes_px)*0.814
                atf3_sizes [atf3_sizes>3000] = 3000
                #counts sizes in each size category (200um^2 bins)
                nf_counts, bins = np.histogram (nf_sizes, bins = 15 , range = (0, 3000))
                ib4_counts, bins = np.histogram (ib4_sizes, bins = 15 , range = (0, 3000))
                atf3_counts, bins = np.histogram (atf3_sizes, bins = 15 , range = (0, 3000))

                nf_counts_percent = nf_counts/nf_counts.sum()*100
                ib4_counts_percent = ib4_counts/nf_counts.sum()*100
                atf3_counts_percent = atf3_counts/nf_counts.sum()*100
                
                nf_sizecounts.append(nf_counts_percent.tolist())
                ib4_sizecounts.append(ib4_counts_percent.tolist())
                atf3_sizecounts.append(atf3_counts_percent.tolist())
        return nf_sizecounts , ib4_sizecounts , atf3_sizecounts , bins
