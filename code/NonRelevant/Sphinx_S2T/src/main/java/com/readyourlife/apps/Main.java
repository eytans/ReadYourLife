package com.readyourlife.apps;

import java.io.*;
import java.net.URL;
import java.nio.charset.Charset;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Paths;

import edu.cmu.sphinx.api.Configuration;
import edu.cmu.sphinx.api.SpeechAligner;
import edu.cmu.sphinx.api.SpeechResult;
import edu.cmu.sphinx.api.StreamSpeechRecognizer;

import javax.print.DocFlavor;

public class Main {

    public static void main(String[] args) throws Exception {
        if (args.length != 3){
            System.out.println("Commend line arguments missing: <wav_filename> <output_filename> <lm_parameter>");
            return;
        }
        String wav_filename = args[0];
        String output_filename = args[1];
        String lm_parameter = args[2];

        Configuration configuration = new Configuration();

        // Set path to acoustic model (from phone to the feature vector with highest probability).
        configuration
                .setAcousticModelPath("resource:/edu/cmu/sphinx/models/en-us/en-us");
        // Set path to dictionary (from word to it's phones).
        configuration
                .setDictionaryPath("resource:/edu/cmu/sphinx/models/en-us/cmudict-en-us.dict");
        // Set language model.
        configuration
                .setLanguageModelPath(lm_parameter);

        StreamSpeechRecognizer recognizer = new StreamSpeechRecognizer(
                configuration);
        //Audio input file must be in one of these 2 formats:
        //RIFF (little-endian) data, WAVE audio, Microsoft PCM, 16 bit, mono 16000 Hz
        //RIFF (little-endian) data, WAVE audio, Microsoft PCM, 16 bit, mono 8000 Hz
        //InputStream stream = new FileInputStream(new File(output_filename));

        /*
        //if we want live speech (not from file) we will use:
        LiveSpeechRecognizer recognizer = new LiveSpeechRecognizer(configuration);
        // Start recognition process pruning previously cached data..
        recognizer.startRecognition(true);
        SpeechResult result = recognizer.getResult();
        // Pause recognition process. It can be resumed then with startRecognition(false).
        recognizer.stopRecognition();
        */

        InputStream stream = new FileInputStream(new File(wav_filename));
        recognizer.startRecognition(stream);
        SpeechResult result;

        //FileOutputStream output = new FileOutputStream(output_filename);

        FileWriter fw = new FileWriter(output_filename,false); //the true will append the new data

        while ((result = recognizer.getResult()) != null) {
            fw.write(result.getHypothesis() + " ");//appends the string to the file
            //output.write(result.getHypothesis())
        }
        recognizer.stopRecognition();
        fw.close();

        //FileInputStream true_teanscription_text = new FileInputStream(new File((true_transcription)));

        // If we want to align the speech recognition results with the original text
        //SpeechAligner aligner = new SpeechAligner(configuration);
       // recognizer.align(new URL(wav_filename), true_teanscription_text);

    }
}