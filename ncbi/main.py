# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import eutilities


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    connection = eutilities.EutilsConnection(eutilities.NCBIDatabases.Nucleotides)
    id = connection.fetch_queries_ids(term='XM_537211', get_first=True)[0]
    result = connection.get_id_information(db_id=id)
    gene = result.gene
    print(gene)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
