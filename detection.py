"""
CME Detection using Isolation Forest
Author: Dinesh Sathvik

This script detects Coronal Mass Ejections (CMEs) from space weather CDF files
by analyzing proton flux in multiple energy bins and identifying anomalies.
"""

import sys
import pandas as pd
import matplotlib.pyplot as plt
from cdflib import CDF, cdfepoch
from sklearn.ensemble import IsolationForest


def load_cdf(file_path, bins):
    """Load CDF file and extract flux data for given energy bins."""
    cdf = CDF(file_path)
    epoch = cdf.varget("Epoch")
    timestamps = cdfepoch.to_datetime(epoch)
    flux = cdf.varget("PS_Inner_allspecies")

    flux_data = {}
    for bin_index in bins:
        bin_name = f"bin_{bin_index}"
        flux_data[bin_name] = flux[:, bin_index]

    df = pd.DataFrame(flux_data, index=timestamps)
    return df


def detect_anomalies(df, contamination=0.01):
    """Smooth data and detect anomalies using Isolation Forest."""
    df_smoothed = df.rolling(window=5, min_periods=1).mean()
    X = df_smoothed.values
    model = IsolationForest(contamination=contamination, random_state=42)
    model.fit(X)
    df_smoothed["anomaly"] = model.predict(X)
    return df_smoothed


def plot_results(df, bin_to_plot):
    """Plot flux for a given bin and highlight anomalies."""
    anomaly_times = df[df["anomaly"] == -1].index
    plt.figure(figsize=(14, 6))
    plt.plot(df.index, df[bin_to_plot], label=f"Flux ({bin_to_plot})", color="blue")
    plt.scatter(anomaly_times, df.loc[anomaly_times, bin_to_plot], color="red", label="Anomalies")
    plt.xlabel("Time")
    plt.ylabel("Flux")
    plt.title("Multivariate CME Detection (Isolation Forest, Bins 3–7)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python detection.py <path_to_cdf_file>")
        sys.exit(1)

    cdf_file = sys.argv[1]
    selected_bins = [3, 4, 5, 6, 7]

    print(f"Loading data from {cdf_file}...")
    df_multi = load_cdf(cdf_file, selected_bins)

    print("Detecting anomalies...")
    df_multi_analyzed = detect_anomalies(df_multi)

    print("Plotting results...")
    plot_results(df_multi_analyzed, "bin_5")
