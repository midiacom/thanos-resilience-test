import pandas as pd
from datetime import datetime

for folder in [1, 2]:
    current_switch = {}
    counter = 1
    for switch in ['s1', 's2', 's3', 's4']:
        with open(f'logs{folder}/{switch}.log') as log:
            print(folder, switch)
            while True:
                time = log.readline().strip()
                if not time:
                    break
                time = time[4:].replace('-03', '').capitalize()
                time = time.replace('Dez', 'Dec')
                time = datetime.strptime(time, '%b %d %H:%M:%S %Y')
                log.readline()
                while True:
                    row = {'switch': switch, 'time': time}
                    last_pos = log.tell()
                    line = log.readline()
                    if not line:
                        break
                    if line[0] != ' ':
                        log.seek(last_pos)
                        break
                    line = line.strip()
                    line_head, line_tail = line.split(' actions')
                    for data in line_head.split(','):
                        data = data.strip()
                        try:
                            head, tail = data.split('=')
                            row[head] = tail
                        except ValueError:
                            row['dl_type'] = data
                    row['actions'] = line_tail[1:]
                    current_switch[counter] = row
                    counter += 1
    dataset = pd.DataFrame.from_dict(current_switch, "index")
    dataset.to_csv(f'logs{folder}/switches.csv')
