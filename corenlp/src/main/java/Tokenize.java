import edu.stanford.nlp.ling.CoreLabel;
import edu.stanford.nlp.pipeline.CoreDocument;
import edu.stanford.nlp.pipeline.StanfordCoreNLP;
import me.tongfei.progressbar.ProgressBar;
import org.apache.log4j.BasicConfigurator;

import java.io.*;
import java.util.Arrays;
import java.util.List;
import java.util.Properties;

public class Tokenize {

    public static void main(String[] args) {
        long startTime = System.currentTimeMillis();
        BasicConfigurator.configure();

        // creates a StanfordCoreNLP object, with POS tagging, tokenization and ssplit
        Properties props = new Properties();
        props.setProperty("annotators", "tokenize, ssplit, pos");
        props.setProperty("threads", "8");
        props.setProperty("outputFormat", "text");
        StanfordCoreNLP pipeline = new StanfordCoreNLP(props);

        File[] folder = new File(args[0]).listFiles();
        assert folder != null;
        List<File> folderList = Arrays.asList(folder);
        BufferedReader reader;
        BufferedWriter writer;


        try {
            writer = new BufferedWriter(new FileWriter("tokenized_dataset"));

            // Go through each text file in the folder
            for (File file : ProgressBar.wrap(folderList, "Tokenizing files")) {
                if (!file.getName().endsWith("txt")) {
                    continue;
                }

                reader = new BufferedReader(new FileReader(file));
                /*reader = new BufferedReader(new InputStreamReader(
                        ProgressBar.wrap(new FileInputStream(file), "Reading file")
                ));*/
                String line = reader.readLine();

                // Go through each line in the file
                while (line != null) {
                    // Make a Document with the line in it, annotate it, and get the tokens
                    CoreDocument document = new CoreDocument(line);
                    pipeline.annotate(document);
                    List<CoreLabel> tokens = document.tokens();

                    // Write tokens to file with newlines after each sentence
                    for (CoreLabel token : tokens) {
                        String tokenValue = token.value();

                        writer.write(tokenValue + " ");
                        if (tokenValue.equals(".")) {
                            writer.write("\n");
                        }
                    }
                    line = reader.readLine();
                }
                reader.close();
            }
            writer.close();
        } catch (IOException e) {
            e.printStackTrace();
        }


        /*TODO: To make CoNLL-files, make an annotation instead of document, use an OutputStream as writer and feed these + pipeline to CoNLLUOutputter*/

        long endTime = System.currentTimeMillis();

        System.out.println("Running time: " + (endTime - startTime)/1000 + " seconds");
    }

}