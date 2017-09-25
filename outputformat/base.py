"""
Base output formatter class that should be inherited
by all of the custom formatters
"""


class BaseOutput (object):

    def __init__(self):
        self.facts = []

    def read_fact(self, fact):
        self.facts.append(fact)

    def get_fact_headings(self, fact):
        """
        Iterate over all of the data elements in the fact
        and extract the Keys from the dictionary ones
        """
        result = set()
        for region, datalist in fact.data.items():
            for element in datalist:
                if hasattr(element, 'keys') and callable(element.keys):
                    result.update(element.keys())
        # Sort all possible headings
        ordered_headings = getattr(fact, 'ORDERED_HEADINGS', [])
        if ordered_headings:
            hlist = []
            # First add the ordered headings that were requested
            hlist = [h for h in ordered_headings if h in result]
            # Extend the list with the leftovers sorted alphabetically
            hlist.extend(sorted(list(result - set(hlist))))
        else:
            # Simple sorting by name to keep the output consistent
            hlist = sorted(list(result))
        return hlist

    def all_output(self):
        """
        Generates the output of every fact in self.facts
        """
        result = ''
        for fact in self.facts:
            # result += '<!-- *%s* -->\n' % fact.NAME.upper()
            result += self.fact_output(fact) + '\n'
        return result
