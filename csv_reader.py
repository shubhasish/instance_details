import pandas as pd
import pickledb


csvDataframe = pd.read_csv("ri_details.csv")

type_dict = {x:None for x in set(csvDataframe['Instance Type'])}
writer = pd.ExcelWriter('trial.xlsx',engine='xlsxwriter')
#


environment_set = set(csvDataframe['Environment'])
db = pickledb.load('instancePickel',False)

for env in environment_set:
    db.set(env,[])


for rows in csvDataframe.iterrows():

    if rows[1]['State'] == "running":
        env = rows[1]['Environment']
        temp_data = db.get(env)
        temp_data.append(rows[1].tolist())
        db.set(env,temp_data)

    else:
        continue
for env in environment_set:
    name = "%s" % env

    df = db.get(env)
    dataframe = pd.DataFrame(index=None,columns=['Env','Name','State','Type'],data=db.get(env))
    dataframe.to_excel(writer,name)
writer.save()
# writer = pd.ExcelWriter('trial.xlsx',engine='xlsxwriter')
#
#
# type_dict = {x:None for x in set(csvDataframe['Instance Type'])}
#
# environment_set = set(csvDataframe['Environment'])
# db = pickledb.load('instancePickel',False)
# environment_dict = {x :type_dict for x in environment_set}
# for env in environment_set:
#     name = "%s"%env
#     df.to_excel(writer,name)
#
# writer.save()

# df = pd.DataFrame({'Data': [10, 20, 30, 20, 15, 30, 45]})
# writer = pd.ExcelWriter('trial.xlsx',engine='xlsxwriter')
#
#
# type_dict = {x:None for x in set(csvDataframe['Instance Type'])}
#
# environment_set = set(csvDataframe['Environment'])
# db = pickledb.load('instancePickel',False)
# environment_dict = {x :type_dict for x in environment_set}
# for env in environment_set:
#     name = "%s"%env
#     df.to_excel(writer,name)
#
# writer.save()
#db.set('type',type_set)
#db.set('state',state_set)

# for i,instance in enumerate(csvDataframe['Name']):
#     if csvDataframe['State'][i] == "running":
#         print csvDataframe['Environment'][i], instance
    #else:
