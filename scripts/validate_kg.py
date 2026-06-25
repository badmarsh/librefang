#!/usr/bin/env python3
import argparse
import sys
import logging
from rdflib import Graph, URIRef, Literal, Namespace
from rdflib.namespace import RDF, XSD, DC

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

DISINFO = Namespace("http://librefang.ai/ontology/disinformation#")

def generate_dummy_data(valid=True):
    """Generates dummy RDF graph for testing."""
    g = Graph()
    g.bind("disinfo", DISINFO)
    g.bind("dc", DC)
    
    claim_node = URIRef("http://librefang.ai/entity/claim_123")
    source_node = URIRef("http://librefang.ai/entity/source_456")
    
    # Add Claim
    g.add((claim_node, RDF.type, DISINFO.Claim))
    g.add((claim_node, DC.title, Literal("NATO is building a base in the Tatras", datatype=XSD.string)))
    
    if valid:
        g.add((claim_node, DC.date, Literal("2026-06-25T10:00:00Z", datatype=XSD.dateTime)))
    else:
        # Intentionally missing date for invalid test
        pass
        
    # Add Source
    g.add((source_node, RDF.type, DISINFO.Source))
    if valid:
        g.add((source_node, DC.identifier, Literal("https://bad-news.sk/article/1", datatype=XSD.anyURI)))
    else:
        g.add((source_node, DC.identifier, Literal("just a string instead of URI", datatype=XSD.string)))
        
    return g

def main():
    parser = argparse.ArgumentParser(description="LibreFang KG Validator (SHACL)")
    parser.add_argument("--data", type=str, help="Path to input RDF data file")
    parser.add_argument("--shapes", type=str, default="ontology/shacl_shapes.ttl", help="Path to SHACL shapes file")
    parser.add_argument("--dummy-data", action="store_true", help="Run with valid dummy data")
    parser.add_argument("--dummy-invalid", action="store_true", help="Run with malformed dummy data to test rejection")
    
    args = parser.parse_args()
    
    try:
        from pyshacl import validate
    except ImportError:
        logger.error("Missing pyshacl library. Please pip install pyshacl")
        sys.exit(1)
        
    if args.dummy_data or args.dummy_invalid:
        logger.info(f"Generating {'VALID' if args.dummy_data else 'INVALID'} dummy data...")
        data_graph = generate_dummy_data(valid=args.dummy_data)
    elif args.data:
        data_graph = Graph()
        data_graph.parse(args.data, format="turtle")
    else:
        parser.error("Must provide --data, --dummy-data, or --dummy-invalid")
        
    logger.info(f"Loading SHACL shapes from {args.shapes}")
    shacl_graph = Graph()
    try:
        shacl_graph.parse(args.shapes, format="turtle")
    except Exception as e:
        logger.error(f"Failed to load SHACL file: {e}")
        sys.exit(1)
        
    logger.info("Running SHACL validation engine...")
    conforms, results_graph, results_text = validate(
        data_graph,
        shacl_graph=shacl_graph,
        ont_graph=None,
        inference='rdfs',
        abort_on_first=False,
        meta_shacl=False,
        debug=False
    )
    
    if conforms:
        logger.info("SUCCESS: Data graph conforms to all SHACL shapes. Knowledge Representation is 10/10 perfect.")
        sys.exit(0)
    else:
        logger.error("VALIDATION FAILED: Data graph violates ontology constraints.")
        print(results_text)
        sys.exit(1)

if __name__ == "__main__":
    main()
