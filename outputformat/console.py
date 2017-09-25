from outputformat.base import BaseOutput


class Console(BaseOutput):
    OPTION = 'console'

    def fact_output(self,  fact):
        # Import is here to avoid crash on parse time if tabulate is missing
        from tabulate import tabulate

        banner = fact.banner()
        if banner:
            print banner

        headers = self.get_fact_headings(fact)
        # result = ''
        table = [['Region'] + headers]
        # result = tabulate (table, headers)
        # Iterate over facts, sorted by region
        for region, fdata in sorted (fact.data.items(), key=lambda x: x[0]):
            if not fdata:
                continue
            ordered_facts = sorted(
                fdata, key=lambda f: [f.get(h) for h in headers])
            for row in ordered_facts:
                table.append([region or 'N/A'] + [str(row.get(el, 'N/A')) for el in headers])
            table.append([''] * (len(headers) + 1))
        result = tabulate(table, headers="firstrow") + '\n'
        return result
