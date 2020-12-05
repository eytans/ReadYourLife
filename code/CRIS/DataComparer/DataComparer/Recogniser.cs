using Microsoft.ProjectOxford.SpeechRecognition;
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading;
using System.Threading.Tasks;

namespace DataComparer
{
    public class Recogniser : IRecogniser
    {
        private string defaultPrimarySubscriptionKey = "abab2365943c4b23a92dfb460ac44ba9";
        private string defaultSecondarySubscriptionKey = "3ae4344adedc4bac9401bf9ea1c0a73b";

        private string customPrimarySubscriptionKey = "79ce811c1bad4e01801c8003d456ffea";
        private string customSecondarySubscriptionKey = "f96aae2c6343468f8c0a997d145804eb";
        private string customModelUrl = "https://d30d9b1853b149ffb19e24dbd1f322a8.api.cris.ai/ws/cris/speech/recognize?cid=5c082016-9d97-401a-b915-7ae96db6e191";

        private Semaphore sem;
        private string recognitionResult;

        private DataRecognitionClient defaultDataClient;
        private DataRecognitionClient customDataClient;

        private SpeechRecognitionMode mode = SpeechRecognitionMode.LongDictation;

        private string DefaultLocale
        {
            get { return "en-US"; }
        }

        public Recogniser()
        {
            sem = new Semaphore(0, 1);

            defaultDataClient = SpeechRecognitionServiceFactory.CreateDataClient(
                mode,
                DefaultLocale,
                defaultPrimarySubscriptionKey,
                defaultSecondarySubscriptionKey);
            defaultDataClient.OnResponseReceived += this.OnDataDictationResponseReceivedHandler;
            defaultDataClient.OnConversationError += OnConversationErrorHandler;

            customDataClient = SpeechRecognitionServiceFactory.CreateDataClient(
                mode,
                DefaultLocale,
                customPrimarySubscriptionKey,
                customSecondarySubscriptionKey,
                customModelUrl);
            customDataClient.OnResponseReceived += this.OnDataDictationResponseReceivedHandler;
        }

        private void OnConversationErrorHandler(object sender, SpeechErrorEventArgs e)
        {
            recognitionResult = null;
            sem.Release();
        }

        private void SendAudio(DataRecognitionClient dataClient, string fileName)
        {
            using (FileStream fileStream = new FileStream(fileName, FileMode.Open, FileAccess.Read))
            {
                // Note for wave files, we can just send data from the file right to the server.
                // In the case you are not an audio file in wave format, and instead you have just
                // raw data (for example audio coming over bluetooth), then before sending up any 
                // audio data, you must first send up an SpeechAudioFormat descriptor to describe 
                // the layout and format of your raw audio data via DataRecognitionClient's sendAudioFormat() method.
                int bytesRead = 0;
                byte[] buffer = new byte[10000];

                try
                {
                    do
                    {
                        // Get more Audio data to send into byte buffer.
                        bytesRead = fileStream.Read(buffer, 0, buffer.Length);

                        // Send of audio data to service. 
                        dataClient.SendAudio(buffer, bytesRead);
                    }
                    while (bytesRead > 0);
                }
                finally
                {
                    // We are done sending audio.  Final recognition results will arrive in OnResponseReceived event call.
                    dataClient.EndAudio();
                }
            }
        }

        private void OnDataDictationResponseReceivedHandler(object sender, SpeechResponseEventArgs e)
        {
            for (int i = 0; i < e.PhraseResponse.Results.Length; i++)
            {
                recognitionResult = e.PhraseResponse.Results[i].DisplayText;
                break;
            }
            sem.Release();
        }

        private string Recognise(DataRecognitionClient dataClient, string fileName)
        {
            int i = 0;
            recognitionResult = null;
            while(recognitionResult == null && i < 10)
            {
                SendAudio(dataClient, fileName);
                sem.WaitOne(300000);
                i++;
            }
            string temp = recognitionResult;
            recognitionResult = null;
            return temp;
        }

        public string RecogniseDefault(string fileName)
        {
            return Recognise(defaultDataClient, fileName);
        }

        public string RecogniseCustom(string fileName)
        {
            return Recognise(customDataClient, fileName);
        }
    }
}
