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

    N = 5000
    c = 5

    data = np.random.rand(N, c)
    print(data.shape)
    print(data[:10, :10])


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

