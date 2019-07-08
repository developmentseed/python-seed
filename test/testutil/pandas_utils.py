import datetime
import pandas as pd
import numpy as np
import tempfile
import os
def create_simple_series(columns,number_days):

    data = np.array([np.arange(number_days)] * len(columns)).T
    todays_date = datetime.datetime.now().date()
    index = pd.date_range(todays_date - datetime.timedelta(number_days), periods=number_days, freq='D')
    return pd.DataFrame(data,index=index,columns=columns)

def testit():
    columns = ['A','B','C']
    data = np.array([np.arange(10)] * 3).T
    todays_date = datetime.datetime.now().date()
    index = pd.date_range(todays_date - datetime.timedelta(10), periods=10, freq='D')
    df  = pd.DataFrame(data,index=index,columns=columns)

    data_path = tempfile.mkdtemp(prefix="util_test_")
    print("created temp dir {}".format(data_path))
    csvpath = os.path.join(data_path,"test.csv")
    df.to_csv(csvpath)

    df = pd.DataFrame.from_csv(csvpath)



if __name__ == '__main__':
    testit()

