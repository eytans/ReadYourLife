using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace DataComparer
{
    public class RecognitionRunner
    {

        private DirectoryInfo dir;
        private DirectoryInfo customOut;
        private DirectoryInfo defaultOut;
        private List<string> customDone;
        private List<string> defaultDone;
        private IRecogniser recogniser;

        private string NormalizeFileName(string name)
        {
            char[] fileName = name.ToLower().Where((char c) => c != ' ' && c != '-' && c != '_').ToArray();
            return Path.GetFileNameWithoutExtension(new String(fileName));
        }

        public RecognitionRunner(string dir, IRecogniser recogniser)
        {
            this.dir = new DirectoryInfo(dir);
            if (!this.dir.Exists)
                throw new System.ArgumentException("Directory must exist");

            this.customOut = new DirectoryInfo(Path.Combine(dir, "customout"));
            this.customOut.Create();
            this.customDone = this.customOut.EnumerateFiles().Select((FileInfo fi) => NormalizeFileName(fi.Name)).ToList();

            this.defaultOut = new DirectoryInfo(Path.Combine(dir, "defaultout"));
            this.defaultOut.Create();
            this.defaultDone = this.defaultOut.EnumerateFiles().Select((FileInfo fi) => NormalizeFileName(fi.Name)).ToList();

            this.recogniser = recogniser;
        }


        private ICollection<FileInfo> GetFilesRemaining(DirectoryInfo di)
        {
            return this.dir.EnumerateFiles().Where(
                (FileInfo fi) => 
                fi.Extension.Equals(".wav") && 
                !(di.EnumerateFiles().Select((FileInfo fiInner) => NormalizeFileName(fiInner.Name)).Contains(NormalizeFileName(fi.Name)))
                ).ToArray();
        }

        private ICollection<FileInfo> GetFilesRemainingForCustom()
        {
            return GetFilesRemaining(this.customOut);
        }

        private ICollection<FileInfo> GetFilesRemainingForDefault()
        {
            return GetFilesRemaining(this.defaultOut);
        }

        public void Run()
        {
            foreach(FileInfo fi in GetFilesRemainingForDefault())
            {
                string result = this.recogniser.RecogniseDefault(fi.FullName);
                string resultPath = Path.Combine(this.defaultOut.FullName, NormalizeFileName(fi.Name) + ".txt");
                File.WriteAllText(resultPath, result);
                this.defaultDone.Add(NormalizeFileName(fi.Name));
            }

            foreach (FileInfo fi in GetFilesRemainingForCustom())
            {
                string result = this.recogniser.RecogniseCustom(fi.FullName);
                string resultPath = Path.Combine(this.customOut.FullName, NormalizeFileName(fi.Name) + ".txt");
                File.WriteAllText(resultPath, result);
                this.customDone.Add(NormalizeFileName(fi.Name));
            }
        }
    }
}
