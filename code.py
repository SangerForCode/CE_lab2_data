import pandas as pd
import matplotlib.pyplot as plt

# ============================
# Experimental Parameters
# ============================

area = 0.65973   # cm^2
pH = 14          # CHANGE according to your electrolyte

reference = "HgHgO"  # options: "AgAgCl" or "HgHgO"

if reference == "AgAgCl":
    E0 = 0.197
elif reference == "HgHgO":
    E0 = 0.098


# ============================
# Read EC-Lab .mpt
# ============================

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

    # Potential vs RHE
    data["E_RHE"] = pd.to_numeric(df["Ewe/V"], errors="coerce") + E0 + 0.059*pH

    # Current density
    current = pd.to_numeric(df["<I>/mA"], errors="coerce")

    data["j_mA_cm2"] = current / area

    data = data.dropna()

    return data


# ============================
# File Paths
# ============================

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


# ============================
# Plot HER curves
# ============================

plt.figure(figsize=(8,6))

for name in files:

    data = read_mpt(files[name])

    plt.plot(
        data["E_RHE"],
        data["j_mA_cm2"],
        linewidth=2,
        label=name
    )


plt.xlabel("E (V vs RHE)", fontsize=13)
plt.ylabel("j (mA cm$^{-2}$)", fontsize=13)

plt.title("Hydrogen Evolution Reaction (HER)", fontsize=14)

plt.grid(True)
plt.legend()

plt.tight_layout()

plt.savefig("HER_current_density.png", dpi=300)

plt.show()