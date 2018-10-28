from logs import logDecorator as lD 
from lib.elasticDS import elasticDS as eDS
import json, pprint
import numpy as np
from tqdm import tqdm

import pandas as pd

from sklearn.linear_model import Lasso
from sklearn.model_selection import train_test_split

config = json.load(open('../config/config.json'))
logBase = config['logging']['logBase'] + '.modules.exampleElasticDS.exampleElasticDS'


@lD.log(logBase + '.getParameterTypes')
def getParameterTypes( logger, instance ):
    
    mapper = {
        type(2.0)   : 'double',
        type(2)     : 'integer',
        type('str') : 'text',
        type(True)  : 'boolean'
    }

    params = instance.get_params()
    paramTypes = []
    for p in params:
        t = type(params[p])
        if t not in mapper:
            logger.error('Unknown type definition for [{}]: {}'.format(p, t))
            logger.error('Needs to ne inserted manually ...')
            continue

        paramTypes.append( (p, mapper[t]) )

    return paramTypes

def fitModel_alpha(model, data):

    columns = data.columns
    Xcols   = [c for c in columns if c != 'result']
    ycols   = ['result']

    es = eDS.ElasticDS( 'lasso', newIndex=False)

    X = data[Xcols]
    y = data[ycols]

    Xtrain, Xvalid, ytrain, yvalid = train_test_split(X, y, test_size=0.2, random_state=1234)
    Xtrain, Xtest,  ytrain, ytest   = train_test_split(Xtrain.copy(), ytrain.copy(), test_size=0.2, random_state=1234)

    print(Xtrain.shape, ytrain.shape)
    print(Xtest.shape, ytest.shape)
    print(Xvalid.shape, yvalid.shape)

    for alpha in tqdm(np.logspace(-5, -1)):
        tqdm.write(f'alpha = {alpha}')

        model.set_params(alpha=alpha)
        model.fit(Xtrain, ytrain)

        trainAcc = model.score( Xtrain, ytrain )
        testAcc  = model.score( Xtest, ytest )
        validAcc = model.score( Xvalid, yvalid )

        # Insert data into ElasticStack
        # -----------------------------
        dataToInsert = {}

        params = model.get_params()
        for m in params:
            if m == 'alpha':
                dataToInsert[m] = np.log10(params[m])
            else:
                dataToInsert[m] = params[m]

        dataToInsert['headers']             = Xcols
        dataToInsert['accuracy_train']      = trainAcc
        dataToInsert['accuracy_test']       = testAcc 
        dataToInsert['accuracy_validation'] = validAcc
        dataToInsert['train_size']          = Xtrain.shape[0]

        es.writeData( dataToInsert )

    return

@lD.log(logBase + '.doSomething')
def testLinearModel(logger):
    '''print a line
    
    This function simply prints a single line
    
    Parameters
    ----------
    logger : {logging.Logger}
        The logger used for logging error information
    '''

    l          = Lasso(random_state=12345)
    paramTypes = getParameterTypes(l)
    data       = pd.read_csv('../data/raw_data/someData.csv')

    if False:
        e = eDS.ElasticDS( 'lasso', paramTypes, newIndex=False)

    fitModel_alpha(l, data)
            
    
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
    # print('We get a copy of the result dictionary over here ...')
    # pprint.pprint(resultsDict)

    testLinearModel()

    print('Getting out of exampleElasticDS')
    print('-'*30)

    return

