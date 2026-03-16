import pandas as pd
from openpyxl import Workbook
from openpyxl.chart import ScatterChart, Reference, Series


# -----------------------------
# Read EC-Lab .mpt files
# -----------------------------
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
    data["Potential (V)"] = pd.to_numeric(df["Ewe/V"], errors="coerce")
    data["Current (mA)"] = pd.to_numeric(df["<I>/mA"], errors="coerce")

    data = data.dropna()

    return data


# -----------------------------
# File paths (your structure)
# -----------------------------

files = {

    "Bare SS":
    "F/HER studies/bare SS_C02.mpt",

    "Modified SS 5 min":
    "F/HER studies/mSS 5 min HER after condn_C02.mpt",

    "Modified SS 7 min":
    "F/HER studies/mSS 7 min HER after condn_C02.mpt",

    "Pt Acid":
    "F/pH study/Pt in acid_C02.mpt",

    "Pt Base":
    "F/pH study/Pt in base_C02.mpt"
}


# -----------------------------
# Create Excel Workbook
# -----------------------------

wb = Workbook()
wb.remove(wb.active)


for name, path in files.items():

    data = read_mpt(path)

    ws = wb.create_sheet(title=name)

    # Write headers
    ws.append(["Potential (V)", "Current (mA)"])

    # Write data
    for i in range(len(data)):
        ws.append([data.iloc[i,0], data.iloc[i,1]])

    # Create scatter chart
    chart = ScatterChart()
    chart.title = f"HER Curve - {name}"
    chart.x_axis.title = "Potential (V)"
    chart.y_axis.title = "Current (mA)"

    xvalues = Reference(ws, min_col=1, min_row=2, max_row=len(data)+1)
    yvalues = Reference(ws, min_col=2, min_row=2, max_row=len(data)+1)

    series = Series(yvalues, xvalues, title=name)

    chart.series.append(series)

    ws.add_chart(chart, "E2")


# Save Excel file
wb.save("HER_Analysis.xlsx")

print("Excel file created: HER_Analysis.xlsx")