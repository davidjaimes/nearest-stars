from astropy import constants as c
from astropy import units as u
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


# Read fixed-width formatted (fwf) data file.
widths = [28, 12, 11, 8, 8, 9, 9, 10, 10, 9, 5, 11, 6, 9, 14, 10, 7, 6, 8, 7,
    8, 9, 9, 9, 6]
columns = ['DIST', 'Mv', 'BOL-LUM', 'RADIUS', 'Unnamed: 19', 'Teff']
df = pd.read_fwf('data/nearest-stars', widths=widths, usecols=columns)
df = df.drop([0, 1]).reset_index(drop=True)
df = df.rename(columns={'Unnamed: 19': 'Radunit'})

# Convert to number from string.
columns = ['Teff', 'Mv', 'DIST', 'RADIUS', 'BOL-LUM']
for col in columns:
    df[col] = df[col].str.replace(r'[a-zA-Z]', '', regex=True)
    df[col] = pd.to_numeric(df[col], errors='coerce')

# Radius conversion from Sun, Jupiter, and Earth.
w = df['Radunit'] == 'Rj'
df.loc[w, 'RADIUS'] /= 9.9604
w = df['Radunit'] == 'Re'
df.loc[w, 'RADIUS'] /= 109.18

# Temperature-Luminosity Relation lines.
t = np.linspace(250, 1e4) * u.K
r = np.logspace(-3, 3, 7) * u.R_sun
T, R = np.meshgrid(t, r)
coef = (4 * np.pi * c.sigma_sb).to('W K-4 Rsun-2')
L = (coef * pow(R, 2) * pow(T, 4)).to('Lsun')

# Plot Temperature-Luminosity Relation lines
plt.figure(figsize=(10, 6))
CS = plt.contour(T, L, R, levels=r, colors='C7', linestyles='-')
manual = [(9e3, 1e-5), (9e3, 1e-3), (9e3, 1e-1), (2.5e3, 1e-1), (2.5e3, 1e1),
    (2.5e3, 1e3)]
plt.clabel(CS, fmt = r'%.3g R$_{\odot}$', inline=True, manual=manual,
    fontsize=14)

# Plot data and contour lines
plt.scatter(df['Teff'], df['BOL-LUM'], s=1e3*df['RADIUS'], c=df['DIST'],
	zorder=2, alpha=1)
plt.scatter(5778, 1, s=100, c='red', label='Sun', zorder=3)
plt.xlabel(r'Temperature ($^\circ$K)', size=16)
plt.ylabel(r'Bol. Luminosity (L$_{\odot}$)', size=16)

# Plot options
plt.grid(zorder=3, ls=':')
plt.legend()
plt.xlim(1e4, 250)
plt.ylim(1e-8, 1e4)
plt.yscale('log')
plt.colorbar().set_label(label='Distance (light years)', size=16)
plt.clim(df.DIST.min(), 25)
plt.tight_layout()
plt.savefig('nearby-stars.png', dpi=300)