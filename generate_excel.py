import pandas as pd
from openpyxl import Workbook
from openpyxl.chart import ScatterChart, Reference, Series

# =========================
# Experimental Parameters
# =========================

area = 0.65973      # cm^2
pH = 14             # change if needed
reference = "HgHgO" # options: HgHgO or AgAgCl

if reference == "HgHgO":
    E0 = 0.098
elif reference == "AgAgCl":
    E0 = 0.197


# =========================
# Function to read .mpt
# =========================

def read_mpt(filepath):

    with open(filepath, "r", encoding="latin1") as f:
        lines = f.readlines()

    header_index = None
    for i, line in enumerate(lines):
        if "Ewe/V" in line and "<I>/mA" in line:
            header_index = i
            break

    headers = lines[header_index].strip().split("\t")

    df = pd.read_csv(
        filepath,
        sep="\t",
        names=headers,
        skiprows=header_index + 1,
        encoding="latin1",
        engine="python"
    )

    data = pd.DataFrame()

    potential = pd.to_numeric(df["Ewe/V"], errors="coerce")
    current = pd.to_numeric(df["<I>/mA"], errors="coerce")

    # Convert units
    data["E_RHE (V)"] = potential + E0 + 0.059*pH
    data["Current (mA)"] = current
    data["j (mA/cm^2)"] = current / area

    data = data.dropna()

    return data


# =========================
# File paths
# =========================

files = {

    "Bare_SS":
    "F/HER studies/bare SS_C02.mpt",

    "Modified_SS_5min":
    "F/HER studies/mSS 5 min HER after condn_C02.mpt",

    "Modified_SS_7min":
    "F/HER studies/mSS 7 min HER after condn_C02.mpt",

    "Pt_Acid":
    "F/pH study/Pt in acid_C02.mpt",

    "Pt_Base":
    "F/pH study/Pt in base_C02.mpt"
}


# =========================
# Create Excel workbook
# =========================

wb = Workbook()
wb.remove(wb.active)

for name, path in files.items():

    data = read_mpt(path)

    ws = wb.create_sheet(name)

    ws.append(["E_RHE (V)", "Current (mA)", "j (mA/cm^2)"])

    for i in range(len(data)):
        ws.append(list(data.iloc[i]))

    chart = ScatterChart()
    chart.title = f"HER Curve - {name}"

    chart.x_axis.title = "E (V vs RHE)"
    chart.y_axis.title = "j (mA cm^-2)"

    xvalues = Reference(ws, min_col=1, min_row=2, max_row=len(data)+1)
    yvalues = Reference(ws, min_col=3, min_row=2, max_row=len(data)+1)

    series = Series(yvalues, xvalues, title=name)
    chart.series.append(series)

    ws.add_chart(chart, "F2")


# Save workbook
wb.save("HER_LSV_Analysis.xlsx")

print("Excel file created: HER_LSV_Analysis.xlsx")