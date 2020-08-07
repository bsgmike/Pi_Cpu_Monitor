import pandas as pd
import time
df = pd.DataFrame({'count': [1],
                   'timestamp': [pd.datetime.now()]})

def addRow(df):
    newRow = pd.DataFrame({'count': [1],
                       'timestamp': [pd.datetime.now()]})
    time.sleep(1)
    # df.append(newRow)
    return(df.append(newRow, ignore_index=True))

# print(df)

df = addRow(df)
df = addRow(df)
df = addRow(df)
df = addRow(df)
print(df)
df = df.reindex()
df = df.drop([0])
print(df)
