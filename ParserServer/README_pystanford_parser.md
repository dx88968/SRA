# pystanford_parser

### Compile
javac -cp .:stanford-parser.jar:py4j0.8.jar ParserServer.java

### Run
make sure the ParserServer.class, stanford-parser.jar,py4j0.8.jar and englishPCFG.ser.gz in the same fold.

java -cp .:stanford-parser.jar:py4j0.8.jar ParserServer

### Using
Just using pystanford_parser.py as normal python code. Make sure the ParserServer is running whenever using the pystanford_parser.py.