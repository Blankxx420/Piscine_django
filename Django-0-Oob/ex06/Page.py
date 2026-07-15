from elem import Elem, Text
from elements import (
    Html, Head, Body, Title, Meta, Img, Table, Th, Tr, Td, 
    Ul, Ol, Li, H1, H2, P, Div, Span, Hr, Br
)

ALL_VALID_TAG = (
    Html, Head, Body, Title, Meta, Img, Table, Th, Tr, Td,
    Ul, Ol, Li, H1, H2, P, Div, Span, Hr, Br, Text
)

BLOCK_TYPES = (H1, H2, Div, Table, Ul, Ol, Span, P, Text)

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

        elif isinstance(node, (Body, Div)):
            if not all(isinstance(c, BLOCK_TYPES) for c in children):
                return False

        elif isinstance(node, (Title, H1, H2, Li, Th, Td)):
            if len(children) != 1 or type(children[0]) is not Text:
                return False

        elif isinstance(node, P):
            if not all(type(c) is Text for c in children):
                return False

        elif isinstance(node, Span):
            if not all(isinstance(c, (Text, P)) for c in children):
                return False

        elif isinstance(node, (Ul, Ol)):
            if len(children) < 1 or not all(isinstance(c, Li) for c in children):
                return False

        elif isinstance(node, Tr):
            if len(children) < 1:
                return False
            first_type = type(children[0])
            if first_type not in (Th, Td):
                return False
            if not all(type(c) is first_type for c in children):
                return False

        elif isinstance(node, Table):
            if not all(isinstance(c, Tr) for c in children):
                return False

        for child in children:
            if not self._check_node(child):
                return False

        return True

    def is_valid(self):
        return self._check_node(self.root)

    def __str__(self):
        html_structure = ""
        if isinstance(self.root, Html):
            html_structure += "<!DOCTYPE html>\n"
        html_structure += str(self.root)
        return html_structure
    
    def write_to_file(self, filename):
        with open(filename, "w") as f:
            f.write(str(self))


if __name__ == "__main__":
    print("=== STARTING HTML VALIDATOR TESTS ===\n")

    print("--- Testing VALID structures ---")
    
    minimal_html = Html([
        Head([Title(Text("My awesome title"))]),
        Body([H1(Text("Welcome!")), P(Text("This is a paragraph."))])
    ])
    page_ok = Page(minimal_html)
    print(f"Minimal structure valid? {page_ok.is_valid()} (Expected: True)")

    complex_html = Html([
        Head([Title(Text("Complex Page"))]),
        Body([
            Div([
                H2(Text("My list")),
                Ul([
                    Li(Text("First element")),
                    Li(Text("Second element"))
                ]),
                Table([
                    Tr([Th(Text("Header 1")), Th(Text("Header 2"))]),
                    Tr([Td(Text("Value 1")), Td(Text("Value 2"))])
                ])
            ])
        ])
    ])
    page_complex = Page(complex_html)
    print(f"Complex structure valid? {page_complex.is_valid()} (Expected: True)")


    print("\n--- Testing INVALID structures ---")

    class Foo(Elem):
        def __init__(self):
            super().__init__('foo')
    
    try:
        invalid_type = Page(Foo())
        print(f"Unknown tag 'foo' valid? {invalid_type.is_valid()} (Expected: False)")
    except Exception as e:
        print(f"Error caught during Foo init: {e}")

    bad_html_order = Html([
        Body([H1(Text("No head!"))])
    ])
    print(f"Html without Head valid? {Page(bad_html_order).is_valid()} (Expected: False)")

    bad_head = Html([
        Head([
            Title(Text("Title 1")),
            Title(Text("Title 2"))
        ]),
        Body([P(Text("Text"))])
    ])
    print(f"Head with two titles valid? {Page(bad_head).is_valid()} (Expected: False)")

    bad_body = Html([
        Head([Title(Text("Title"))]),
        Body([
            Div([
                Head([Title(Text("Head inside Div?!"))])
            ])
        ])
    ])
    print(f"Head nested inside Div valid? {Page(bad_body).is_valid()} (Expected: False)")

    bad_title = Html([
        Head([
            Title([Text("Title"), P(Text("Forbidden paragraph here"))])
        ]),
        Body([P(Text("Text"))])
    ])
    print(f"Title containing P valid? {Page(bad_title).is_valid()} (Expected: False)")

    empty_list = Html([
        Head([Title(Text("Title"))]),
        Body([
            Ul([])
        ])
    ])
    print(f"Empty Ul list valid? {Page(empty_list).is_valid()} (Expected: False)")

    mixed_tr = Html([
        Head([Title(Text("Title"))]),
        Body([
            Table([
                Tr([Th(Text("Header")), Td(Text("Data"))])
            ])
        ])
    ])
    print(f"Mixed Th/Td row valid? {Page(mixed_tr).is_valid()} (Expected: False)")


    print("\n--- Testing HTML rendering & Files ---")
    
    print("Testing print output (Doctype expected):")
    print(page_ok)
    
    just_a_div = Page(Div([H1(Text("Single Title"))]))
    print("\nTesting print output without Doctype (Root is a Div):")
    print(just_a_div)

    filename = "test_output.html"
    page_ok.write_to_file(filename)
    print(f"\n[OK] File '{filename}' successfully generated.")