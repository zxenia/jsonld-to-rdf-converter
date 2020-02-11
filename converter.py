import logging
import getopt
from sys import argv
from rdflib import Graph
import json
from rdflib.plugin import register, Serializer
register('json-ld', Serializer, 'rdflib_jsonld.serializer', 'JsonLDSerializer')


logger = logging.getLogger(__name__)

def main(argv):
    FORMAT = '%(message)s'
    logging.basicConfig(format=FORMAT)
    logging.getLogger().setLevel(logging.INFO)
    opts, args = getopt.getopt(argv, "", ["file=", "format="])
    jsonld_filename = ''
    output_format = None

    for opt, arg in opts:
        if opt == '--file':
            jsonld_filename = arg
        elif opt == '--format':
            output_format = arg

    if jsonld_filename == '':
        help()
        exit()

    with open(jsonld_filename) as json_file:
        jsonld_obj = json.load(json_file)
        if output_format:
            try:
                jsonld_to_rdf(jsonld_obj, jsonld_filename.split('.jsonld')[0], output_format)
            except Exception:
                available_serializers()
                exit()
        else:
            jsonld_to_rdf(jsonld_obj, jsonld_filename.split('.jsonld')[0])


def jsonld_to_rdf(jsonld_obj, filename, output_format=None):
    """

    :param jsonld_obj: json object with LD context
    :param output_format: rdf format to serialize to
    :return: data serialized in rdf triples
    """

    # Initiate a graph
    g = Graph().parse(data=json.dumps(jsonld_obj), format='json-ld')
    # Available formats for serialization and corresponding file extensions
    formats = {
        'pretty-xml': 'rdf',
        'n3': 'n3',
        'nt': 'nt',
        'trig': 'trig',
        'turtle': 'ttl',
        'xml': 'rdf'
    }
    if output_format:
        rdf_data = g.serialize(destination='{}.{}'.format(filename, formats[output_format]),
                               format=output_format)
    else:
        # By default serialize to rdf/xml
        rdf_data = g.serialize(destination='{}.rdf'.format(filename), format='pretty-xml')

    return rdf_data


def help():
    return logger.info('Usage: python converter.py --file=doc.jsonld [--format=turtle]')


def available_serializers():
    return logger.info('Available serializer formats are pretty-xml, n3, nt, trig, turtle, xml')


if __name__ == "__main__":
    main(argv[1:])
