import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
from sys import argv

dataset = pd.read_csv('logs1/switches.csv', index_col=0, parse_dates=['time'])
protocol = argv[1].upper()
if protocol == 'SV':
    dataset = dataset.query('dl_type == "0x88ba"')
elif protocol == 'GOOSE':
    dataset = dataset.query('dl_type == "0x88b8"')
else:
    raise ValueError('Unknown protocol')
sns.set_theme(style="darkgrid")
sns.set_palette('mako', 4)
dataset = dataset.groupby(['time', 'switch']).sum()
sns.lineplot(
    x='time', y='n_packets', data=dataset,
    hue='switch', style='switch',
    legend='full'
)
plt.title(f'{protocol} (exp1)')
plt.show()
