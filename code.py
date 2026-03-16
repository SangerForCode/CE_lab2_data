import pandas as pd
import matplotlib.pyplot as plt


# -----------------------------
# Function to read EC-Lab .mpt
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
    data["Potential_V"] = pd.to_numeric(df["Ewe/V"], errors="coerce")
    data["Current_mA"] = pd.to_numeric(df["<I>/mA"], errors="coerce")

    data = data.dropna()

    return data


# -----------------------------
# File Paths
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
# Graph 1 — Bare SS
# -----------------------------

data = read_mpt(files["Bare SS"])

plt.figure(figsize=(8,6))
plt.plot(data["Potential_V"], data["Current_mA"], linewidth=1.5)

plt.xlabel("Potential (Ewe / V)")
plt.ylabel("Current (<I> / mA)")
plt.title("HER Curve — Bare Stainless Steel")

plt.grid(True)
plt.tight_layout()

plt.savefig("HER_Bare_SS.png", dpi=300)
plt.show()


# -----------------------------
# Graph 2 — Modified SS (5 min)
# -----------------------------

data = read_mpt(files["Modified SS 5 min"])

plt.figure(figsize=(8,6))
plt.plot(data["Potential_V"], data["Current_mA"], linewidth=1.5)

plt.xlabel("Potential (Ewe / V)")
plt.ylabel("Current (<I> / mA)")
plt.title("HER Curve — Modified SS (5 min conditioning)")

plt.grid(True)
plt.tight_layout()

plt.savefig("HER_Modified_SS_5min.png", dpi=300)
plt.show()


# -----------------------------
# Graph 3 — Modified SS (7 min)
# -----------------------------

data = read_mpt(files["Modified SS 7 min"])

plt.figure(figsize=(8,6))
plt.plot(data["Potential_V"], data["Current_mA"], linewidth=1.5)

plt.xlabel("Potential (Ewe / V)")
plt.ylabel("Current (<I> / mA)")
plt.title("HER Curve — Modified SS (7 min conditioning)")

plt.grid(True)
plt.tight_layout()

plt.savefig("HER_Modified_SS_7min.png", dpi=300)
plt.show()


# -----------------------------
# Graph 4 — pH Study (comparison)
# -----------------------------

acid = read_mpt(files["Pt Acid"])
base = read_mpt(files["Pt Base"])

plt.figure(figsize=(8,6))

plt.plot(acid["Potential_V"], acid["Current_mA"], label="Pt in Acid", linewidth=1.5)
plt.plot(base["Potential_V"], base["Current_mA"], label="Pt in Base", linewidth=1.5)

plt.xlabel("Potential (Ewe / V)")
plt.ylabel("Current (<I> / mA)")
plt.title("Effect of pH on HER (Pt Electrode)")

plt.grid(True)
plt.legend()

plt.tight_layout()

plt.savefig("HER_pH_comparison.png", dpi=300)
plt.show()