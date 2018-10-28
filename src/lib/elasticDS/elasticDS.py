from logs import logDecorator as lD
import json

config = json.load(open('../config/config.json'))
logBase = config['logging']['logBase'] + '.lib.elasticDS.elasticDS'

class ElasticDS:

    @lD.log(logBase + '.ElasticDS')
    def __init__(logger, self, indexName, hyperParams = None, headers = None, newIndex = True):
        '''Generates a new connection and index
        
        This class is used for generating a new class that will
        possibly generate a new index. When you want to start 
        a new type of algorithm, you will want to use this to
        generate a new index. The index will contain information
        about all hyperparameters. 
        
        Parameters
        ----------
        logger : {[type]}
            [description]
        self : {[type]}
            [description]
        hyperParams : {[type]}
            [description]
        others : {[type]}
            [description]
        newIndex : {bool}, optional
            [description] (the default is True, which [default_description])
        '''
        

        self.eDSconfig = json.load(open('../config/elasticDS.json'))
        self.es        = ElasticSearch(self.eDSconfig['server'])
        self.indexName = indexName

        if newIndex == False:
            assert hyperParams is not None, '`hyperParams` cannot be `None` for creating an index'
            assert headers is not None, '`headers` cannot be `None` for creating an index'
            
        if newIndex:
            logger.info(f'Generating a new index: {indexName}')

            # Generate the request body
            # --------------------------------------
            requestBody = {}
            requestBody['settings'] = eDSconfig['index_settings']
            mapping = {}
            for h, t in hyperparameters:
                mapping[h] = {
                    'index' : 'not_analyzed',
                    'type'  : t
                }
            mapping['headers'] = {
                'index' : 'not_analyzed',
                'type'  : 'string'
            }
            mapping['accuracy_train'] = {
                'index' : 'not_analyzed',
                'type'  : 'double'
            }
            mapping['accuracy_test'] = {
                'index' : 'not_analyzed',
                'type'  : 'double'
            }
            mapping['accuracy_validation'] = {
                'index' : 'not_analyzed',
                'type'  : 'double'
            }
            mapping['train_size'] = {
                'index' : 'not_analyzed',
                'type'  : 'integer'
            }

            requestBody['mappings']['example'] = mappings

            try:
                self.es.indices.create( index=self.indexName, body=requestBody)
            except Exception as e:
                logger.error('Unable to geenrate a new index: {}'.format(e))

        return