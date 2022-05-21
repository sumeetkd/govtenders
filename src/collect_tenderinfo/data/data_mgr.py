import json
import os
import datetime

class data_entry:

    def __init__(self ,name):
        self.name = name
        self.data_dir = "data/raw/" + self.name
        self.filename = (datetime.datetime.now()).strftime('%Y%m%d') + '.json'
        self.data = self.load_latest()


    def load_latest(self):
        if not os.path.isdir(self.data_dir):
            return False
        else:
            for _ ,_ ,filenames in os.walk(self.data_dir):
                if len(filenames):
                    latest = max(filenames)
                    with open(os.path.join(self.data_dir ,latest)) as jsonfile:
                        data = json.load(jsonfile)
                    return data
                else:
                    return False


    def save_data(self ,tender_items):
        if not os.path.isdir(self.data_dir):
            os.mkdir(self.data_dir)
        filepath = os.path.join(self.data_dir ,self.filename)
        if self.data:
            self.data.extend(tender_items)
        else:
            self.data = tender_items
        with open(filepath,'w') as jsonfile:
            json.dump(self.data, jsonfile)
# [TODO] Keep only 5 copies at any point

    def check_unique(self, dictentry):
        if self.data:
            return (not (dictentry in self.data))
        else:
            return True




#    def populate(self ,dictentry ,dataframe):
#        captions = [item for item in dictentry]
#        if list(dataframe.columns) == captions:
#            if dataframe[captions[0]].count():
#                if dictentry['Tender ID'] not in dataframe['Tender ID'].values:
#                # Using Tender ID explicitly is not a good idea will have to change when other websites are included
#                # If there is a hash that can be used that would be great
#                    return True, dataframe.append(dictentry, ignore_index=True)
#                else:
#                    return False, dataframe
#            else:
#                return True, dataframe.append(dictentry, ignore_index=True)
#        else:
#            return False, dataframe


