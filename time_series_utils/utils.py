def seasonal_plot(df, target, period, freq, ax=None):
    if ax is None:
        fig, ax = plt.subplots(figsize=(15, 8))
    ax.grid(True, lw=0.2)
    for i in df[period].unique():
        subset = df[df[period] == i]
        subset = subset.groupby(freq).mean()
        ax.plot(subset.index, subset[target], label=str(i), alpha=0.7)
    ax.set_title(f'Seasonal plot: {period}/{freq}')
    ax.legend(loc='best')

def plot_periodogram(ts, detrend='linear', ax=None):
    
    fs = pd.Timedelta("365D") / pd.Timedelta("1D")
    freqencies, spectrum = periodogram(
        ts,
        fs=fs,
        detrend=detrend,
        window="boxcar",
        scaling='spectrum',
    )
    if ax is None:
        _, ax = plt.subplots()
    ax.step(freqencies, spectrum, color="purple")
    ax.set_xscale("log")
    ax.set_xticks([1, 2, 4, 6, 12, 26, 52, 104])
    ax.set_xticklabels(
        [
            "Annual (1)",
            "Semiannual (2)",
            "Quarterly (4)",
            "Bimonthly (6)",
            "Monthly (12)",
            "Biweekly (26)",
            "Weekly (52)",
            "Semiweekly (104)",
        ],
        rotation=30,
    )
    ax.ticklabel_format(axis="y", style="sci", scilimits=(0, 0))
    ax.set_ylabel("Variance")
    ax.set_title("Periodogram")
    return ax


def make_leads(ts, leads, prefix = None):
    return pd.concat({
            f'{prefix}_lead_{i}': ts.shift(-i)
            for i in leads
        },
        axis=1)


def make_lags(ts, lags, lead_time=1):
    return pd.concat(
        {
            f'y_lag_{i}': ts.shift(i)
            for i in range(lead_time, lags + lead_time)
        },
        axis=1)

def make_multistep_target(ts, steps):
    return pd.concat(
        {f'y_step_{i + 1}': ts.shift(-i)
         for i in range(steps)},
        axis=1)