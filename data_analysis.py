import pandas as pd
import yaml as yl
import random

def main():
  df = pd.read_csv('https://docs.google.com/spreadsheets/d/e/2PACX-1vQrmXOPYzar8P-FId_oa2lfisX-T_NATGri6UGQ3yixy_JE5f4DqlKhXLkfstZrTaBnkZTq6mquWuvM/pub?gid=0&single=true&output=csv', skiprows = 1)
  connectors = df['Connector Name'].unique()
  all_connectors = {}
  all_cables = {}
  all_connections = []

  def find_connector(source, df):
    row = df.loc[df['PIN ID'] == source]
    return (row['Connector Name'], row['Pin Number'])

  colors = ['BK', 'BU', 'OG', 'VT', 'RD']

  pin_df = pd.DataFrame(columns=connectors)
  pin_connections = df[df['Source'].notna()]
  for index, row in pin_connections.iterrows():
    og_source = row['Source']
    og_connector = row['Connector Name']
    source = find_connector(og_source, df)
    temp_row = pd.DataFrame(columns=connectors)
    temp_row[og_connector] = [index]
    temp_row[source[0]] = [source[1]]
    pin_df = pin_df.append(temp_row, ignore_index=True)
    cable_name = 'W' + str(index)
    cable = { cable_name : {
                          'colors' : [random.choice(colors)],
                          'wirecount': 1
                          }
            }
    all_cables.update(cable)
    temp_val = [{og_connector : [row['Pin Number']]}, {cable_name : [1]}, {(source[0].iloc[0]) : [int(source[1])]}]
    all_connections.append(temp_val)

  for connector in connectors:
    temp = df[df['Connector Name'] == connector]
    pin_number = temp['Pin Number'].tolist()
    count = 0
    index = 1
    for x in pin_number:
      if type(x) == float:
        x = int(x)
        index += 1
      else:
        x = index + count
        count += 1
        index += 1
    pin_id = temp['PIN ID'].tolist()
    pin_name = temp['Pin Name']
    connect_add = { connector : { 
                                'pins' : pin_number,
                                'pinlabels' : pin_id,
                                'color' : random.choice(colors)
                              }
                }
    all_connectors.update(connect_add)

  dict_file = {'connectors' : all_connectors, 
              'cables' : all_cables, 
              'connections' : all_connections}
  file = open('data.yml', 'w')
  yl.dump(dict_file, file, default_flow_style=None)

  print('Data Pulled & Updated')

