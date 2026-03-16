import pandas as pd
from openpyxl import Workbook
from openpyxl.chart import ScatterChart, Reference, Series

# ======================
# Experimental constants
# ======================

area = 0.65973
pH = 14
reference = "HgHgO"

if reference == "HgHgO":
    E0 = 0.098
else:
    E0 = 0.197


# ======================
# Read EC-Lab file
# ======================

def read_mpt(filepath):

    with open(filepath,"r",encoding="latin1") as f:
        lines = f.readlines()

    header = None
    for i,line in enumerate(lines):
        if "Ewe/V" in line and "<I>/mA" in line:
            header = i
            break

    headers = lines[header].strip().split("\t")

    df = pd.read_csv(
        filepath,
        sep="\t",
        names=headers,
        skiprows=header+1,
        encoding="latin1",
        engine="python"
    )

    potential = pd.to_numeric(df["Ewe/V"],errors="coerce")
    current = pd.to_numeric(df["<I>/mA"],errors="coerce")

    data = pd.DataFrame()

    data["E_RHE"] = potential + E0 + 0.059*pH
    data["j"] = current/area

    data = data.dropna()

    return data


# ======================
# File locations
# ======================

files = {

"bare_ss":"F/HER studies/bare SS_C02.mpt",

"mod_ss7":"F/HER studies/mSS 7 min HER after condn_C02.mpt",

"pt_acid":"F/pH study/Pt in acid_C02.mpt",

"pt_base":"F/pH study/Pt in base_C02.mpt"

}


data = {k:read_mpt(v) for k,v in files.items()}


# ======================
# Create Excel workbook
# ======================

wb = Workbook()
wb.remove(wb.active)


def make_sheet(sheet_name, datasets):

    ws = wb.create_sheet(sheet_name)

    col = 1

    chart = ScatterChart()
    chart.x_axis.title = "E (V vs RHE)"
    chart.y_axis.title = "j (mA cm^-2)"
    chart.title = sheet_name

    for name in datasets:

        df = data[name]

        ws.cell(row=1,column=col,value="E_RHE")
        ws.cell(row=1,column=col+1,value="j")

        for i in range(len(df)):
            ws.cell(row=i+2,column=col,value=df.iloc[i,0])
            ws.cell(row=i+2,column=col+1,value=df.iloc[i,1])

        xvalues = Reference(ws,min_col=col,min_row=2,max_row=len(df)+1)
        yvalues = Reference(ws,min_col=col+1,min_row=2,max_row=len(df)+1)

        series = Series(yvalues,xvalues,title=name)

        chart.series.append(series)

        col += 3

    ws.add_chart(chart,"H2")


# ======================
# Graph 1
# ======================

make_sheet(
"Graph1_Pt",
["pt_base","pt_acid"]
)


# ======================
# Graph 2
# ======================

make_sheet(
"Graph2_Pt",
["pt_base","pt_acid"]
)


# ======================
# Graph 3
# ======================

make_sheet(
"Graph3_SS_Pt",
["bare_ss","mod_ss7","pt_base"]
)


# ======================
# Graph 4
# ======================

make_sheet(
"Graph4_SS_Pt",
["bare_ss","mod_ss7","pt_base"]
)


wb.save("HER_Final_Graphs.xlsx")

print("Excel created: HER_Final_Graphs.xlsx")