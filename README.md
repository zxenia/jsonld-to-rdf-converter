# jsonld-to-rdf converter

## Overview

Command line tool that takes jsonld file and converts it to one of the rdf formats.
Based on [rdflib](https://github.com/RDFLib/rdflib) and [rdflib-jsonld](https://github.com/RDFLib/rdflib-jsonld).

Available serializer formats are pretty-xml, n3, nt, trig, turtle, xml.

Usage:

`pip install -r requirements.txt`

`python converter.py --file=doc.jsonld [--format=ttl]`

By default converts to rdf/xml if output format is not specified.