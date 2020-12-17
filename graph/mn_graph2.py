import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns

dataset = pd.read_csv('logs2/switches.csv', index_col=0, parse_dates=['time'])
dataset = dataset.query('dl_type == "0x88ba"')
sns.set_theme(style="darkgrid")
sns.set_palette('mako', 4)
dataset = dataset.groupby(['time', 'switch']).sum()
sns.lineplot(
    x='time', y='n_packets', data=dataset,
    hue='switch', style='switch',
    legend='full'
)
plt.title('SV - exp2')
plt.show()
