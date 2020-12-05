using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading;
using Microsoft.ProjectOxford.SpeechRecognition;
using System.IO;

namespace DataComparer
{

    class Program
    {
        static void Main(string[] args)
        {
            DirectoryInfo baseDI = new DirectoryInfo(args[0]);
            Recogniser recogniser = new Recogniser();
            foreach(DirectoryInfo di in baseDI.EnumerateDirectories().ToList())
            {
                Console.WriteLine("Starting with dir: " + di.Name);
                new RecognitionRunner(di.FullName, recogniser).Run();
            }
        }
    }
}
