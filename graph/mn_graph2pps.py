import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
import numpy as np

dataset = pd.read_csv('logs2/switches.csv', index_col=0, parse_dates=['time'])
dataset = dataset.query('dl_type == "0x88ba"')
sns.set_theme(style="darkgrid")
sns.set_palette('mako', 4)
dataset = dataset.groupby(['time', 'switch']).sum()
dataset.drop(columns=['n_bytes', 'send_flow_rem priority', 'dl_vlan'],
             inplace=True)
dataset['pps'] = np.nan
dataset.reset_index(inplace=True)
dataset.loc[0:2, 'pps'] = [0, 0, 0]
# dataset = dataset.head(2000)
for index in range(3, len(dataset)):
    dataset.loc[index, 'pps'] = (dataset.loc[index, 'n_packets'] - dataset.loc[index - 3, 'n_packets']) / 60
# dataset = dataset.tail(500)
print(dataset.to_string())
sns.lineplot(
    x='time', y='pps', data=dataset,
    hue='switch', style='switch',
    legend='full'
)
plt.title('SV - exp2')
plt.show()
