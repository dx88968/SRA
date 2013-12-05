#NLP

##Running on our Server

We have depolied the code on an ubuntu server, you can upload the data via sftp to the server and run it.

  * sftp -P @aurora.cadmuxe.com 
  * ssh -p @aurora.cadmuxe.com
  * python Main.py dataset_type n-way train_data_path test_data_path output_file


##Running locally
#####Dependence
* java
* nltk with all data
  * python -m nltk.downloader all 
* py4j
  * pip install py4j
* pyenchant (enchant)
  * http://pythonhosted.org/pyenchant/
* numpy
* scipy

#####Runing


* ParserServer (in SRA/ParserServer)
  * (Mac/linux)  java -cp .:stanford-parser.jar:py4j0.8.jar ParserServer
  * (Windows)java -cp .;stanford-parser.jar;py4j0.8.jar ParserServer
* python Main.py dataset_type n-way train_data_path test_data_path output_file
  * example: python Main.py beetle 5 ../SemEval/train/beetle/Core/ ../SemEval/train/beetle/Core/ output