#!/usr/bin/python

import sys, getopt

import xml.etree.ElementTree as ET

from classes.Feature import *
from classes.Enum import *
from classes.Function import *
from classes.Extension import *
from classes.Type import *

from binding import *

from gen_bitfields import *
from gen_booleans import *
from gen_enums import *
from gen_values import *
from gen_types import *

from gen_extensions import *
from gen_functions import *

from gen_meta import *

def generate(inputfile, targetdir):

	tree       = ET.parse(inputfile)
	registry   = tree.getroot()

	types 	   = parseTypes(registry)

	features   = parseFeatures(registry)

	enums      = sorted(parseEnums(registry))
	extensions = sorted(parseExtensions(registry, features))

	functions  = sorted(parseFunctions(registry))

	includedir = targetdir + "/include/glbinding/"
	sourcedir  = targetdir + "/source/"


	genBitfields			    (enums,      includedir, "bitfield.h")
	genBooleans			   	    (enums,      includedir, "boolean.h")
	genEnums 			 		(enums,      includedir, "enum.h")
	genValues		   	        (enums,      includedir, "values.h")
	
	genTypes                    (types,      includedir, "types.h")  

	genExtensions			   	(extensions, includedir, "extension.h")

	genFunctions        	    (functions,  includedir, "functions.h")

	genFunctionObjects_h        (functions,  includedir, "FunctionObjects.h")
	genFunctionObjects_cpp      (functions,  sourcedir,  "FunctionObjects.cpp")
	genFunctionList             (functions,  sourcedir,  "FunctionObjects_Functions.cpp")
	
	genMetaStringsByEnum	    (enums,      sourcedir,  "Meta_StringsByEnum.cpp")
	genMetaEnumsByString	    (enums,      sourcedir,  "Meta_EnumsByString.cpp")

	genMetaStringsByExtension	(extensions, sourcedir,  "Meta_StringsByExtension.cpp")
	genMetaExtensionsByString	(extensions, sourcedir,  "Meta_ExtensionsByString.cpp")


def main(argv):
	try:
		opts, args = getopt.getopt(argv[1:], "s:d:", ["spec=", "directory="])
	except getopt.GetoptError:
		print("usage: %s -s <GL spec> [-d <output directory>]" % argv[0])
		sys.exit(1)
		
	targetdir = "."
	inputfile = None
	
	for opt, arg in opts:
		if opt in ("-s", "--spec"):
			inputfile = arg
			
		if opt in ("-d", "--directory"):
			targetdir = arg
			
	if inputfile == None:
		print("No GL spec file given")
		sys.exit(1)

	generate(inputfile, targetdir)

if __name__ == "__main__":
	main(sys.argv)
