import eikon as ek
import pandas as pd

ek.set_app_key('02251fexxxxxxxxxxxxxxxxxxxxxxxxxxxxxfd2c')


constituents, err = ek.get_data(".FTSE", "TR.IndexConstituentRIC")

for company in constituents['Constituent RIC']:
    data, err = ek.get_data(company, ["TR.CompanyName", "TR.OfficerName(RNK=R1:R100)", "TR.OfficerTitle(RNK=R1:R100)"])
    data.to_csv("data/"+company+".csv")
