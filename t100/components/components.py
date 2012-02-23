from t100.core import base_components as bc

class Source(bc.Source):
    """ Source accept two parameters:
            creation_tax_expression: is an expression that returns the probability 
                of an event be created in a time t
            execution_time_expression: is an expression that return the timestamp
                of the created event
    """

