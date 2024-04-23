import pandas as pd
from src import file_reader  

working_dir = "data/bclxL_Unprot_1_2_CLPC_50mM_CaCl2/analysis/traj/"
psf_filename = "bclxL_Unprot_1_2_CLPC_50mM_CaCl2_from_VMD.psf"
Ca_prot_filename = "BclxL_Unprot_1_2_CLPC_50mM_CaCl2_Ca_prot.dat"
Ca_lipid_filename = "BclxL_Unprot_1_2_CLPC_50mM_CaCl2_Ca_lipid.dat"

psf_reader = file_reader.PSFReader(working_dir + psf_filename) 
psf_reader.open()
psf_df = psf_reader.get_data()

lipid_file_reader = file_reader.ContactFileReader(working_dir + Ca_lipid_filename)
lipid_file_reader.open()
lipid_df = lipid_file_reader.get_data()

prot_file_reader = file_reader.ContactFileReader(working_dir + Ca_prot_filename)
prot_file_reader.open()
prot_df = prot_file_reader.get_data()

prot_lipid_df = pd.merge(prot_df, lipid_df, 
                        on=["frame","Index 1"],
                        how = "inner", suffixes=('_prot', '_lipid'))       

prot_resid = psf_df.loc[prot_lipid_df['Index 2_prot'], 'resid']
lipid_resid = psf_df.loc[prot_lipid_df['Index 2_lipid'], 'resid']
Ca_resid = psf_df.loc[prot_lipid_df['Index 1'], 'resid']

prot_lipid_resid_df = pd.DataFrame({
                        'frame': prot_lipid_df['frame'],
                        'Ca_resid': Ca_resid.values,
                        'prot_resid': prot_resid.values,
                        'lipid_resid': lipid_resid.values
})
final_df= prot_lipid_resid_df.groupby(['Ca_resid', 'prot_resid']).size().reset_index()
final_df.rename(columns={0:"count"})
final_df.to_csv("results/Ca_prot_lipid_count.csv", index=False)