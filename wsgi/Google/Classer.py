import Search
import sys

class TypeIdentifier:
    def getTypeByTF(self, TF):
        return Search.get_field_by_tf(TF)
        
    def getTypeByQuery(self, query):
        return Search.get_field_by_query(query)
        
    def contains(self, type1, type2):
        return Search.get_relavance(type1, type2)


