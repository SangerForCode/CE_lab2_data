import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ======================
# Experimental constants
# ======================

area = 0.65973        # cm^2
pH = 14               # change if needed
reference = "HgHgO"   # "HgHgO" or "AgAgCl"

if reference == "HgHgO":
    E0 = 0.098
else:
    E0 = 0.197

# ======================
# Read EC-Lab .mpt file
# ======================

def read_mpt(filepath):

    with open(filepath, "r", encoding="latin1") as f:
        lines = f.readlines()

    header = None
    for i, line in enumerate(lines):
        if "Ewe/V" in line and "<I>/mA" in line:
            header = i
            break

    headers = lines[header].strip().split("\t")

    df = pd.read_csv(
        filepath,
        sep="\t",
        names=headers,
        skiprows=header + 1,
        encoding="latin1",
        engine="python"
    )

    potential = pd.to_numeric(df["Ewe/V"], errors="coerce")
    current = pd.to_numeric(df["<I>/mA"], errors="coerce")

    data = pd.DataFrame()

    # Potential vs RHE
    data["E_RHE"] = potential + E0 + 0.059 * pH

    # Current density
    data["j_mA_cm2"] = current / area
    data["j_A_cm2"] = data["j_mA_cm2"] / 1000

    # Overpotential (HER, equilibrium 0 V vs RHE)
    data["eta"] = -data["E_RHE"]

    data = data.dropna()

    return data

# ======================
# File paths
# ======================

bare_ss = "F/HER studies/bare SS_C02.mpt"
mod_ss7 = "F/HER studies/mSS 7 min HER after condn_C02.mpt"
pt_acid = "F/pH study/Pt in acid_C02.mpt"
pt_base = "F/pH study/Pt in base_C02.mpt"

data_bare = read_mpt(bare_ss)
data_mod7 = read_mpt(mod_ss7)
data_acid = read_mpt(pt_acid)
data_base = read_mpt(pt_base)

# ======================
# Helper: Tafel fit
# ======================

def tafel_fit(data, label, tafel_window=(-6, -2)):
    """
    Fit η = a*log10(|j|) + b within log-current window.
    Returns logj, eta, fitted_line_x, fitted_line_y, log_i0.
    """
    j = np.abs(data["j_A_cm2"])
    logj = np.log10(j)

    eta = data["eta"]

    mask = (logj > tafel_window[0]) & (logj < tafel_window[1])
    x = logj[mask]
    y = eta[mask]

    coeff = np.polyfit(x, y, 1)
    slope, intercept = coeff

    x_fit = np.linspace(x.min(), 0, 200)
    y_fit = slope * x_fit + intercept

    # x-intercept (η=0)
    log_i0 = -intercept / slope

    return logj, eta, x_fit, y_fit, log_i0

# ======================
# Graph 1
# ======================

plt.figure(figsize=(7,5))

plt.plot(data_base["E_RHE"], data_base["j_mA_cm2"], label="Pt Base")
plt.plot(data_acid["E_RHE"], data_acid["j_mA_cm2"], label="Pt Acid")

plt.xlabel("E (V vs RHE)")
plt.ylabel("j (mA cm$^{-2}$)")
plt.title("Graph 1: Pt Base + Pt Acid")

plt.grid(True)
plt.legend()
plt.tight_layout()

plt.savefig("Graph1_Pt_Base_Acid.png", dpi=300)
plt.close()

# ======================
# Graph 2 (Tafel)
# ======================

plt.figure(figsize=(7,5))

for data,label in [(data_base,"Pt Base"),(data_acid,"Pt Acid")]:
    
    logj,eta,xfit,yfit,logi0 = tafel_fit(data,label)

    # plt.scatter(logj, eta, s=10, label=f"{label} data")
    plt.plot(xfit,yfit,"--",label=f"{label} fit")

    # plt.scatter(logi0,0,marker="x",s=80)

plt.xlabel("log j (A cm$^{-2}$)")
plt.ylabel("η (V)")
plt.title("Graph 2: Pt Base + Pt Acid (Tafel)")

plt.grid(True)
plt.legend()
plt.tight_layout()

plt.savefig("Graph2_Tafel_Pt.png", dpi=300)
plt.close()

# ======================
# Graph 3
# ======================

plt.figure(figsize=(7,5))

plt.plot(data_bare["E_RHE"], data_bare["j_mA_cm2"], label="Bare SS")
plt.plot(data_mod7["E_RHE"], data_mod7["j_mA_cm2"], label="Mod SS (7 min)")
plt.plot(data_base["E_RHE"], data_base["j_mA_cm2"], label="Pt Base")

plt.xlabel("E (V vs RHE)")
plt.ylabel("j (mA cm$^{-2}$)")
plt.title("Graph 3: Bare SS + Mod SS (7 min) + Pt Base")

plt.grid(True)
plt.legend()
plt.tight_layout()

plt.savefig("Graph3_SS_ModSS7_PtBase.png", dpi=300)
plt.close()

# ======================
# Graph 4 (Tafel)
# ======================

plt.figure(figsize=(7,5))

for data,label in [(data_bare,"Bare SS"),
                   (data_mod7,"Mod SS 7 min"),
                   (data_base,"Pt Base")]:
    
    logj,eta,xfit,yfit,logi0 = tafel_fit(data,label)

    # plt.scatter(logj, eta, s=10, label=f"{label} data")
    plt.plot(xfit,yfit,"--",label=f"{label} fit")

    # plt.scatter(logi0,0,marker="x",s=80)

plt.xlabel("log j (A cm$^{-2}$)")
plt.ylabel("η (V)")
plt.title("Graph 4: Bare SS + Mod SS (7 min) + Pt Base (Tafel)")

plt.grid(True)
plt.legend()
plt.tight_layout()

plt.savefig("Graph4_Tafel_SS_Pt.png", dpi=300)
plt.close()

print("All graphs saved.")