from logs import logDecorator as lD
import json, pprint
from elasticsearch import Elasticsearch

config = json.load(open('../config/config.json'))
logBase = config['logging']['logBase'] + '.lib.elasticDS.elasticDS'

class ElasticDS:

    @lD.log(logBase + '.ElasticDS')
    def __init__(logger, self, indexName, hyperParams = None, newIndex = True):
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
        # self.es        = Elasticsearch([self.eDSconfig['server'],])
        self.es        = Elasticsearch()
        self.indexName = indexName

        if newIndex == True:
            assert hyperParams is not None, '`hyperParams` cannot be `None` for creating an index'
            
        if newIndex:
            logger.info(f'Generating a new index: {indexName}')

            # Generate the request body
            # --------------------------------------
            requestBody = {}
            requestBody['settings'] = self.eDSconfig['index_settings']
            requestBody['mappings'] = {"example":{}}
            mapping = {}
            for h, t in hyperParams:
                mapping[h] = {
                    #'index' : 'not_analyzed',
                    'type'  : t
                }
            mapping['headers'] = {
                # 'index' : 'not_analyzed',
                'type'  : 'text'
            }
            mapping['accuracy_train'] = {
                # 'index' : 'not_analyzed',
                'type'  : 'double'
            }
            mapping['accuracy_test'] = {
                # 'index' : 'not_analyzed',
                'type'  : 'double'
            }
            mapping['accuracy_validation'] = {
                # 'index' : 'not_analyzed',
                'type'  : 'double'
            }
            mapping['train_size'] = {
                # 'index' : 'not_analyzed',
                'type'  : 'integer'
            }

            requestBody['mappings']['example']['properties'] = mapping

            pprint.pprint(requestBody)

            try:
                self.es.indices.create( index=self.indexName, body=requestBody)
            except Exception as e:
                logger.error('Unable to geenrate a new index: {}'.format(e))

        return

    def writeData(self, data):

        self.es.index( 
            index    = self.indexName,
            doc_type = 'example',
            body     = data )

        return