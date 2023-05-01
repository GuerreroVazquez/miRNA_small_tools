from Bio.KEGG.KGML.KGML_parser import read
from Bio.KEGG.KGML.KGML_pathway import Entry

pathway = read(open('resources/hsa04933.xml', 'r'))


def main():

    print(len(pathway.entries))
    print(len(pathway.reactions))
    entry = Entry()
    entry.add_component("gato")
    # entry.pathway = pathway

    pathway.add_component()


def add_mirna(mirna, gene, pathway):
    """
        This function will add the An edge between all the genes 'gene' in the network 'pathway' to a new node
         (if dosen't exist) 'mirna' or to an existent one 'mirna'

    """
    create_entry(id,name, type)
    entry = Entry(7, "cat", 1)
    pathway.add_entry(mirna)
    pathway.add_relation()



if __name__ == "__main__":
    main()