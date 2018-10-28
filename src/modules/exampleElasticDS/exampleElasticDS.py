from logs import logDecorator as lD 
from lib.elasticDS import elasticDS as eDS
import json, pprint

from sklearn.linear_model import Lasso

config = json.load(open('../config/config.json'))
logBase = config['logging']['logBase'] + '.modules.exampleElasticDS.exampleElasticDS'


@lD.log(logBase + '.doSomething')
def testLinearModel(logger):
    '''print a line
    
    This function simply prints a single line
    
    Parameters
    ----------
    logger : {logging.Logger}
        The logger used for logging error information
    '''

    l = Lasso()

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

    print('='*30)
    print('Main function of exampleElasticDS')
    print('='*30)
    print('We get a copy of the result dictionary over here ...')
    pprint.pprint(resultsDict)

    testLinearModel()

    print('Getting out of exampleElasticDS')
    print('-'*30)

    return

