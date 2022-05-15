from pyrml import RMLConverter
from tqdm import tqdm
import os

# Create an instance of the class RMLConverter.
rml_converter = RMLConverter()

rml_file_path = os.path.join('mapping.ttl')
rdf_graph = rml_converter.convert(rml_file_path)

f = open("firmenregister.n3", "a")

# Print the triples contained into the RDF graph.
for s,p,o in tqdm(rdf_graph):
    line = "<" + str(s) + "> <" + str(p) + "> \"" + str(o) + "\" .\n"
    f.write(line)
