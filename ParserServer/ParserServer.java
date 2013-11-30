//package mynlp.stanfordparser;

import java.util.Collection;
import java.util.List;
import java.io.StringReader;

import py4j.GatewayServer;
import edu.stanford.nlp.process.TokenizerFactory;
import edu.stanford.nlp.process.CoreLabelTokenFactory;
import edu.stanford.nlp.process.DocumentPreprocessor;
import edu.stanford.nlp.process.PTBTokenizer;
import edu.stanford.nlp.ling.CoreLabel;
import edu.stanford.nlp.ling.HasWord;
import edu.stanford.nlp.ling.Sentence;
import edu.stanford.nlp.trees.*;
import edu.stanford.nlp.parser.lexparser.LexicalizedParser;

class ParserServer {

  private LexicalizedParser lp;
  public static void main(String[] args) {
	  ParserServer ps = new ParserServer();
	  GatewayServer gatewayServer = new GatewayServer(new ParserServer());
      gatewayServer.start();
      System.out.println("Gateway Server Started");
  }
  
  public ParserServer(){
	  lp = LexicalizedParser.loadModel("englishPCFG.ser.gz");
  }


  public String parser(String sentence) {

	  String rtl = new String();
    Tree parse ;

    TokenizerFactory<CoreLabel> tokenizerFactory =
      PTBTokenizer.factory(new CoreLabelTokenFactory(), "");
    List<CoreLabel> rawWords2 =
      tokenizerFactory.getTokenizer(new StringReader(sentence)).tokenize();
    parse = lp.apply(rawWords2);


    rtl += parse.taggedYield();
    rtl += "@";


    
    TreebankLanguagePack tlp = new PennTreebankLanguagePack();
    GrammaticalStructureFactory gsf = tlp.grammaticalStructureFactory();
    
    GrammaticalStructure gs = gsf.newGrammaticalStructure(parse);
    Collection<TypedDependency> td = gs.typedDependenciesCollapsed();
    System.out.println(td);
    rtl += td.toString();
    
    return rtl;
  }
}
