import pandas as pd
from matplotlib import pyplot as plt, rc
import seaborn as sns
import numpy as np
from matplotlib.dates import DateFormatter


rc('savefig', format='pdf')
rc('figure', figsize=[7, 5])
plt.subplots_adjust(top=1,
                    left=0.1, right=1,
                    bottom=0.13)

dataset = pd.read_csv('logs3/switches.csv', index_col=0, parse_dates=['time'])
dataset = dataset.query('dl_type == "0x88ba"')
sns.set_theme(style="darkgrid")
sns.set_palette('mako', 4)
dataset = dataset.groupby(['time', 'switch']).sum()
dataset.drop(columns=['n_bytes', 'send_flow_rem priority', 'dl_vlan'],
             inplace=True)
dataset['pps'] = np.nan
dataset.reset_index(inplace=True)
dataset.loc[0:2, 'pps'] = [0, 0, 0]
dataset = dataset.head(113)
for index in range(3, len(dataset)):
    dataset.loc[index, 'pps'] = (dataset.loc[index, 'n_packets']
                                 - dataset.loc[index - 3, 'n_packets']) / 60
dataset = dataset.tail(65)
dataset.switch = dataset.switch.apply(lambda x: x.replace('s', 'Switch '))
plot = sns.lineplot(
    x='time', y='pps', data=dataset,
    hue='switch', style='switch',
    hue_order=['Switch 1', 'Switch 2', 'Switch 4'],
    style_order=['Switch 2', 'Switch 1', 'Switch 4'],
    markers=[',', 'D', '.'],
    legend='full'
)
# plt.title('SV - exp3')

ax = plt.gca()
handles, labels = ax.get_legend_handles_labels()
ax.legend(handles=handles, labels=labels)
# for texts, switch in zip(plot.legend_.texts, ['Switch 1', 'Switch 2', 'Switch 4']):
#     texts.set_text(switch)
plt.yticks(np.arange(0, 4801, 1600))
plt.ylabel('Quadros por Segundo')
plt.xlabel('Tempo')

hfmt = DateFormatter('Dia %d\n%H:%M')
ax.xaxis.set_major_formatter(hfmt)
plt.setp(ax.get_xticklabels())
# plt.setp(ax.get_xticklabels(), rotation=45, ha='right')

plt.savefig('graph3_zoom.pdf')
# plt.show()
