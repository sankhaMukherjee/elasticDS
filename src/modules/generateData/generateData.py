from logs import logDecorator as lD 
import json, pprint
import pandas as pd
import numpy as np

config = json.load(open('../config/config.json'))
logBase = config['logging']['logBase'] + '.modules.generateData.generateData'


@lD.log(logBase + '.generateData')
def generateData(logger):
    '''print a line
    
    This function simply prints a single line
    
    Parameters
    ----------
    logger : {logging.Logger}
        The logger used for logging error information
    '''

    print('Generating some data ...')

    N = 5000
    c = 5

    data = np.random.rand(N, c)
    columns = ['column_{:05d}'.format(i) for i in range(c)]
    df = pd.DataFrame( data, columns=columns )
    
    df['result'] = np.random.rand() * 3

    for i in range(c):
        df['result'] += df['column_{:05d}'.format(i)] * np.random.rand() * 5

    print('Data Generated ...')
    print(df.head())

    print('Saving data in data/raw_data')
    df.to_csv('../data/raw_data/someData.csv', index=False)


    return

@lD.log(logBase + '.main')
def main(logger, resultsDict):
    '''main function for module1
    
    This function finishes all the tasks for the
    main function. This is a way in which a 
    particular module is going to be executed. 
    
    Parameters
    ----------
    logger : {logging.Logger}
        The logger used for logging error information
    resultsDict: {dict}
        A dintionary containing information about the 
        command line arguments. These can be used for
        overwriting command line arguments as needed.
    '''

    generateData()

    print('Getting out of generateData')
    print('-'*30)

    return

