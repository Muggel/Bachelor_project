import edu.stanford.nlp.ling.CoreLabel;
import edu.stanford.nlp.pipeline.Annotation;
import edu.stanford.nlp.pipeline.CoNLLUOutputter;
import edu.stanford.nlp.pipeline.CoreDocument;
import edu.stanford.nlp.pipeline.StanfordCoreNLP;
import me.tongfei.progressbar.ProgressBar;
import org.apache.log4j.BasicConfigurator;

import java.io.*;
import java.util.Arrays;
import java.util.List;
import java.util.Properties;

public class DepParse {

    public static void main(String[] args) {
        long startTime = System.currentTimeMillis();
        BasicConfigurator.configure();

        // creates a StanfordCoreNLP object, with POS tagging, tokenization and ssplit
        Properties props = new Properties();
        props.setProperty("annotators", "tokenize, ssplit, pos, depparse");
        props.setProperty("threads", "8");
        props.setProperty("depparse.nthreads", "8");
        props.setProperty("outputFormat", "conllu");
        StanfordCoreNLP pipeline = new StanfordCoreNLP(props);

        File[] folder = new File(args[0]).listFiles();
        assert folder != null;
        List<File> folderList = Arrays.asList(folder);
        BufferedReader reader;
        FileOutputStream fos;
        CoNLLUOutputter outputter = new CoNLLUOutputter();
        int counter = 0;


        //Make dir
        File dir = new File("conllu_files");
        dir.mkdir();

        try {
            // Go through each text file in the folder
            for (File file : ProgressBar.wrap(folderList, "Dependency Parsing")) {
                if (!file.getName().endsWith("txt")) {
                    continue;
                }

                reader = new BufferedReader(new FileReader(file));
                fos = new FileOutputStream(new File("conllu_files/conllu_data"+counter+".conllu"));

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
                counter++;
            }
        } catch (IOException e) {
            e.printStackTrace();
        }


        long endTime = System.currentTimeMillis();

        System.out.println("Running time: " + (endTime - startTime)/1000 + " seconds");
    }

}