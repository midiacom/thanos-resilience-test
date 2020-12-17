import matplotlib.pyplot as plt
import matplotlib.dates as dates
from matplotlib.dates import MO, TU, WE, TH, FR, SA, SU
import numpy as np
from numpy import absolute, mean, std
import pandas as pd
import datetime
import matplotlib.ticker as ticker

def plot(index, onos, ac, gui, ylabel):
    plt.rcParams['figure.figsize'] = 16, 4
    fig, ax = plt.subplots()

    ax.xaxis.set_major_formatter(dates.DateFormatter('Day\n%d'))
    ax.xaxis.set_minor_formatter(dates.DateFormatter('%Hh'))
    ax.xaxis.set_major_locator(dates.DayLocator())
    #ax.xaxis.set_minor_locator(dates.HourLocator(byhour=[6, 12, 18]))
    ax.xaxis.set_minor_locator(dates.HourLocator(byhour=[12]))

    ax.set_xmargin(.0)

    ax.set_ylabel(ylabel)

    # print(ax.get_yticks())

    #labels = [item.get_text() for item in ax.get_xticklabels()]
    #labels[1] = 'Testing'

    #ax.set_xticklabels(labels)

    #ax.xaxis.set_ticks(np.arange(0, len(index), len(index)/10))

    ax.plot(index, onos, label='ONOS')
    ax.plot(index, ac, label='AC')
    ax.plot(index, gui, label='GUI')

    #ax.plot(index, onos, label='app')
    #ax.plot(index, ac, label='gradle-wrapper')
    #ax.plot(index, gui, label='gradle')

    plt.grid(b=True, which='both', linestyle='dotted')

    ax.legend(loc="upper right")
    #plt.show()
    # plt.setp(ax.get_xmajorticklabels(), visible=False)
    plt.savefig("plots/plot_controller_" + ylabel + ".pdf", bbox_inches='tight')
    plt.clf()

df = pd.read_csv("logs/processed-teste2.csv", sep=";", header=0)
df['GUI-CPU%'] = df['GUI (app)-CPU%'] + df['GUI (java,GradleWrapperMain)-CPU%'] + df['GUI (java,gradle)-CPU%']
df['GUI-MEM%'] = df['GUI (app)-MEM%'] + df['GUI (java,GradleWrapperMain)-MEM%'] + df['GUI (java,gradle)-MEM%']

df['AC-CPU%'] = df['AC (app)-CPU%'] + df['AC (sudo,app)-CPU%']
df['AC-MEM%'] = df['AC (app)-MEM%'] + df['AC (sudo,app)-MEM%']

df['ONOS-CPU%'] = df['ONOS (karaf,java)-CPU%'] + df['ONOS (karaf,shell)-CPU%'] + df['ONOS (onos-service,shell)-CPU%']
df['ONOS-MEM%'] = df['ONOS (karaf,java)-MEM%'] + df['ONOS (karaf,shell)-MEM%'] + df['ONOS (onos-service,shell)-MEM%']
#print df.columns.values.tolist()
print df[['ONOS-CPU%', 'ONOS (karaf,java)-CPU%', 'ONOS (karaf,shell)-CPU%', 'ONOS (onos-service,shell)-CPU%']]
print df[['ONOS-MEM%', 'ONOS (karaf,java)-MEM%', 'ONOS (karaf,shell)-MEM%', 'ONOS (onos-service,shell)-MEM%']]

dateList = []
initial_day, initial_hour, initial_minute, initial_second = df['timestamp'].iloc[0].split(":")
initial_date = datetime.datetime(year=2020, month=12, day=int(initial_day)+1, hour=int(initial_hour), minute=int(initial_minute), second=int(initial_second))
for index in range(0,len(df['timestamp'])):
    day, hour, minute, second = df['timestamp'].iloc[index].split(":")
    date = datetime.datetime(year=2020, month=12, day=int(day)+1, hour=int(hour), minute=int(minute), second=int(second))
    elapsed = date - datetime.timedelta(hours=int(initial_hour),minutes=int(initial_minute),seconds=int(initial_second))
    dateList.append(elapsed)
    #dateList.append(date)


samples_to_plot = len(df['timestamp'])

#plot(dateList[:10], df['ONOS-CPU%'].iloc[:10], df['ONOS-MEM%'].iloc[:10], "ONOS Resource Utilization")

plot(dateList[:samples_to_plot], df['ONOS-CPU%'].iloc[:samples_to_plot], df['AC-CPU%'].iloc[:samples_to_plot], df['GUI-CPU%'].iloc[:samples_to_plot], "CPU Usage (%)")
plot(dateList[:samples_to_plot], df['ONOS-MEM%'].iloc[:samples_to_plot], df['AC-MEM%'].iloc[:samples_to_plot], df['GUI-MEM%'].iloc[:samples_to_plot], "MEM Usage (%)")

# plot(dateList[:samples_to_plot], df['GUI (app)-MEM%'].iloc[:samples_to_plot], df['GUI (java,GradleWrapperMain)-MEM%'].iloc[:samples_to_plot], df['GUI (java,gradle)-MEM%'].iloc[:samples_to_plot], "MEM Usage (%)")