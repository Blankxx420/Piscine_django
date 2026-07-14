from elem import Elem, Text
from elements import (
    Html, Head, Body, Title, Meta, Img, Table, Th, Tr, Td, 
    Ul, Ol, Li, H1, H2, P, Div, Span, Hr, Br
)

ALL_VALID_TAG = (
    Html, Head, Body, Title, Meta, Img, Table, Th, Tr, Td,
    Ul, Ol, Li, H1, H2, P, Div, Span, Hr, Br, Text
)

BLOCK_TYPES = (H1, H2, Div, Table, Ul, Ol, Span, Text)

class Page:

    def __init__(self, root):
        if not isinstance(root, Elem):
            raise TypeError("Instance is not subclass of Elem")
        else:
            self.root = root

    def _check_node(self, node):

        if not isinstance(node, ALL_VALID_TAG):
            return False
        if isinstance(node, Text):
            return True
        
        children = node.content

        if isinstance(node, Html):
            if len(children) != 2:
                return False
            if not isinstance(children[0], Head) or not isinstance(children[1], Body):
                return False
        
        elif isinstance(node, Head):
                if len(children) != 1 or not isinstance(children[0], Title):
                    return False
                
        elif isinstance(node, (Div, Body)):
            if len(children) != 1:
                return False
            elif all(isinstance(c, BLOCK_TYPES) for c in children):
                return False
            
        elif isinstance(node, (Title, H1, H2, Li, Th, Td)):
            if len(children) != 1 or type(children[0]) is not Text:
                return False
        
        elif isinstance(node, P):
            if not all(type(c) is Text for c in children):
                return False
        
        elif isinstance(node, Span):
            if not all(isinstance(c, (P, Text)) for c in children):
                return False

        elif isinstance(node, (Ol, Ul)):
            if len(children) != 1 or not all(isinstance(c, Li) for c in children):
                return False
        
        elif isinstance(node, Tr):
            if len(children) != 1:
                return False
            
            first_type = type(children[0])

            if first_type not in  (Th,Td):
                return False
            if not all(type(c) is first_type for c in children):
                return False
            
        elif isinstance(node, Table):
                if not all(isinstance(c, Tr) for c in children):
                    return False

        for child in node.content:
            if not self._check_node(child):
                return False
                
        return True


    def is_valid(self):
        return self._check_node(self.root)



        
    
            