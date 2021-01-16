import pandas as pd
from matplotlib import pyplot as plt, rc
from matplotlib.dates import DateFormatter
import seaborn as sns
import numpy as np


rc('savefig', format='pdf')
rc('figure', figsize=[7, 5])
plt.subplots_adjust(top=1,
                    left=0.095, right=1,
                    bottom=0.2)

dataset = pd.read_csv('logs3/switches.csv', index_col=0, parse_dates=['time'])
dataset = dataset.query('dl_type == "0x88ba"')
sns.set_theme(style="darkgrid")
sns.set_palette('mako', 4)
dataset = dataset.groupby(['time', 'switch']).sum()
dataset['new_time'] = dataset.index.get_level_values(0)

plot = sns.lineplot(
    x='new_time', y='n_packets', data=dataset,
    hue='switch', style='switch',
    legend='full'
)

ax = plt.gca()

handles, labels = ax.get_legend_handles_labels()
ax.legend(handles=handles, labels=labels)
# plt.yticks(np.arange(0, 4801, 1600))
plt.ylabel('Quadros ($x10^9$)')
hfmt = DateFormatter('%d/%m/%Y')
ax.xaxis.set_major_formatter(hfmt)
plt.setp(ax.get_xticklabels(), rotation=45, ha='right')
plt.xlabel('Tempo')

plt.savefig('graph3.pdf')
# plt.show()
