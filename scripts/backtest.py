from __future__ import annotations
import itertools, warnings, datetime as dt, yfinance as yf
import pandas as pd, numpy as np, statsmodels.api as sm
from statsmodels.tsa.stattools import coint
import matplotlib.pyplot as plt

warnings.filterwarnings("ignore", category=FutureWarning)

TICKERS = [
    "XLK", "XLY", "XLV", "XLE", "XLF", "XLB", "XLU",
    "XLP", "XLRE", "IYR",
    "SPY", "QQQ", "DIA", "IWM", "EEM", "HYG",
]
START, END = "2013-01-01", "2025-05-01"
CAPITAL     = 1_000_000
TARGET_VOL  = 0.08
MAX_PAIRS   = 6
HALF_SPREAD = 0.00005
SLIP_COEF   = 0.1

print("⬇  Downloading daily closes …")
px = (
    yf.download(
        TICKERS, start=START, end=END,
        auto_adjust=True, progress=False
    )["Close"]
    .dropna(how="all")
)

px = px[[c for c in px.columns if px[c].count() > 252]]
print(f" Universe after data check: {list(px.columns)}")

def kalman_beta(y: pd.Series, x: pd.Series, R=1e-5, Q=1e-4) -> pd.Series:
    from pykalman import KalmanFilter

    obs_mat = x.values.reshape(-1, 1, 1)
    kf = KalmanFilter(
        transition_matrices=np.array([[1.0]]),
        observation_matrices=obs_mat,
        initial_state_mean=0.0,
        initial_state_covariance=1.0,
        observation_covariance=Q,
        transition_covariance=R / (1 - R) * np.eye(1),
    )
    state_means, _ = kf.filter(y.values)
    return pd.Series(state_means.ravel(), index=y.index)

def rolling_beta(y: pd.Series, x: pd.Series, win=60) -> pd.Series:
    beta = (
        y.rolling(win)
        .corr(x)
        * (y.rolling(win).std() / x.rolling(win).std())
    )
    return beta.ffill()

def half_life(spread: pd.Series) -> float:
    delta  = spread.diff().dropna()
    lagged = spread.shift(1).dropna()
    joined = pd.concat([delta, lagged], axis=1).dropna()
    if joined.empty:
        return np.inf
    y = joined.iloc[:, 0]
    X = sm.add_constant(joined.iloc[:, 1])
    beta = sm.OLS(y, X).fit().params.iloc[1]
    return (-np.log(2) / beta) if beta < 0 else np.inf

def annual_sharpe(pnl: pd.Series) -> float:
    if pnl.std() == 0:
        return np.nan
    return np.sqrt(252) * pnl.mean() / pnl.std()

print("\n  Scanning for cointegrated pairs …")
pairs: list[tuple[str, str, float]] = []
for a, b in itertools.combinations(px.columns, 2):
    s1, s2 = px[a].dropna(), px[b].dropna()
    common = s1.index.intersection(s2.index)
    if len(common) < 252:
        continue
    s1, s2 = np.log(s1.loc[common]), np.log(s2.loc[common])
    if s1.std() == 0 or s2.std() == 0:
        continue
    if s1.pct_change().corr(s2.pct_change()) < 0.8:
        continue
    pval = coint(s1, s2)[1]
    if pval < 0.05:
        pairs.append((a, b, pval))

print(f" {len(pairs)} pairs pass filters.")

def quick_sharpe(a: str, b: str) -> float:
    y, x = np.log(px[a]), np.log(px[b])
    try:
        beta = kalman_beta(y, x)
    except Exception:
        beta = rolling_beta(y, x, 60)
    spread = y - beta * x
    z = (spread - spread.rolling(120).mean()) / spread.rolling(120).std()
    sig = -np.sign(z)
    ret = sig.shift() * (
        px[a].pct_change().fillna(0) -
        beta * px[b].pct_change().fillna(0)
    )
    return annual_sharpe(ret)

ranked = sorted(pairs, key=lambda p: quick_sharpe(p[0], p[1]), reverse=True)
top_pairs = ranked[:MAX_PAIRS]
print(f"\n Trading these {len(top_pairs)} pairs:", [p[:2] for p in top_pairs])

all_pnl = pd.Series(0, index=px.index)

for a, b, _ in top_pairs:
    y, x = np.log(px[a]), np.log(px[b])
    try:
        beta = kalman_beta(y, x)
    except Exception:
        beta = rolling_beta(y, x, 60)

    spread = y - beta * x
    hl = half_life(spread)
    z_win = int(min(max(hl * 3, 60), 240))

    z = (spread - spread.rolling(z_win).mean()) / spread.rolling(z_win).std()

    open_band  = z.abs().rolling(252).quantile(0.95).shift()
    close_band = z.abs().rolling(252).quantile(0.50).shift()

    long_entry  = z < -open_band
    short_entry = z >  open_band
    flat_rule   = z.abs() < close_band

    sig = pd.Series(0, index=z.index)
    sig[long_entry]  =  1
    sig[short_entry] = -1
    sig = sig.ffill()
    sig[flat_rule]   = 0

    day_sigma = spread.diff().abs().rolling(21).mean().clip(lower=1e-6)
    n_pairs   = len(top_pairs)
    risk_unit = TARGET_VOL / np.sqrt(n_pairs)
    w = risk_unit / (day_sigma * np.sqrt(252))
    notional = (CAPITAL * w).clip(upper=CAPITAL * 0.20)

    pnl = (
        notional.shift() * sig.shift() * px[a].pct_change().fillna(0) +
        -notional.shift() * beta * sig.shift() * px[b].pct_change().fillna(0)
    )

    share_a = (notional / px[a]).abs()
    share_b = (notional * beta / px[b]).abs()
    adv_a   = share_a.rolling(21).mean().fillna(share_a) * 20
    adv_b   = share_b.rolling(21).mean().fillna(share_b) * 20
    vol_frac_a = (share_a / adv_a).clip(upper=1)
    vol_frac_b = (share_b / adv_b).clip(upper=1)

    tcost = (
        (HALF_SPREAD + SLIP_COEF * vol_frac_a ** 2) * share_a.diff().abs().fillna(0) +
        (HALF_SPREAD + SLIP_COEF * vol_frac_b ** 2) * share_b.diff().abs().fillna(0)
    )

    pnl -= tcost
    all_pnl = all_pnl.add(pnl, fill_value=0)

equity = (1 + all_pnl.fillna(0) / CAPITAL).cumprod()
sharpe = annual_sharpe(all_pnl)

print(f"\n  Portfolio Sharpe : {sharpe:.2f}")
print(f"Total return        : {(equity.iloc[-1] - 1):.1%}"
      f"  over {(equity.index[-1]-equity.index[0]).days/365:.1f} yrs")

ax = equity.plot(
    title=f'Pairs-portfolio equity curve  –  Sharpe {sharpe:.2f}',
    figsize=(11, 4), lw=1.4
)
ax.grid(ls=":")
plt.tight_layout()
plt.show()
