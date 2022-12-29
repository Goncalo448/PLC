from yacc import *
import sys


parser = build_parser()

if len(sys.argv) > 1:
    with open(sys.argv[1], 'r') as file:
        input = file.read()
        assembly = parser.parse(input)
        
        if len(sys.argv) > 2:
            with open(sys.argv[2], 'w') as output:
                output.write(assembly)
                print(f"{sys.argv[1]} compiled successfully!\nCheck the output in {sys.argv[2]}.")
        else:
            print(f"{sys.argv[1]} compiled successfully!")
