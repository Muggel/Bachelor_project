import edu.stanford.nlp.pipeline.Annotation;
import edu.stanford.nlp.pipeline.CoNLLUOutputter;
import edu.stanford.nlp.pipeline.StanfordCoreNLP;
import org.apache.log4j.BasicConfigurator;

import java.io.*;
import java.util.Date;
import java.util.Properties;

public class DepParse {

    public static void main(String[] args) {
        Date date = new Date();
        System.out.println("Started parsing: "+date.toString());

        BasicConfigurator.configure();

        // creates a StanfordCoreNLP object, with POS tagging, tokenization and ssplit
        Properties props = new Properties();
        props.setProperty("annotators", "tokenize, ssplit, pos, depparse");
        props.setProperty("threads", args[0]);
        props.setProperty("depparse.nthreads", args[0]);
        props.setProperty("outputFormat", "conllu");
        StanfordCoreNLP pipeline = new StanfordCoreNLP(props);

        File[] folder = new File(args[1]).listFiles();
        assert folder != null;
        BufferedReader reader;
        FileOutputStream fos;
        CoNLLUOutputter outputter = new CoNLLUOutputter();



        //Make dir
        File dir = new File("conllu_files");
        dir.mkdir();

        try {
            // Go through each text file in the folder
            for (File file : folder) {
                if (!file.getName().endsWith("txt")) {
                    continue;
                }
                System.out.println("Reading file: " + file.getName());
                reader = new BufferedReader(new FileReader(file));
                fos = new FileOutputStream(new File("conllu_files/"+file.getName()+".conllu"));

                String line = reader.readLine();

                // Go through each line in the file
                while (line != null) {
                    // Make a Document with the line in it, annotate it, and write to output
                    Annotation document = new Annotation(line);
                    pipeline.annotate(document);

                    outputter.print(document, fos, pipeline);

                    line = reader.readLine();
                }
                reader.close();
                fos.flush();
                fos.close();
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

}