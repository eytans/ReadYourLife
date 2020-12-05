using Microsoft.VisualStudio.TestTools.UnitTesting;
using DataComparer;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using NSubstitute;
using System.IO;

namespace DataComparer.Tests
{
    [TestClass()]
    public class RecognitionRunnerTests
    {
        private IRecogniser recogniser;

        [TestInitialize()]
        public void SetUp()
        {
            recogniser = NSubstitute.Substitute.For<IRecogniser>();
            recogniser.RecogniseCustom(Arg.Any<string>()).Returns("hello");
            recogniser.RecogniseDefault(Arg.Any<string>()).Returns("Hello");
        }

        [TestMethod()]
        [DeploymentItem(@"../../data", "data")]
        public void RunGoesOverAllDirectoryTest()
        {
            RecognitionRunner runner = new RecognitionRunner("data", this.recogniser);
            runner.Run();
            recogniser.ReceivedWithAnyArgs(8).RecogniseCustom("");
            recogniser.ReceivedWithAnyArgs(8).RecogniseDefault("");
        }

        [TestMethod()]
        [DeploymentItem(@"../../data", "data")]
        public void RunOutputsTextFileTest()
        {
            RecognitionRunner runner = new RecognitionRunner("data", this.recogniser);
            runner.Run();
            DirectoryInfo dataDI = new DirectoryInfo("data");
            Assert.AreNotEqual(0, dataDI.EnumerateDirectories().Count());
            foreach(DirectoryInfo di in dataDI.EnumerateDirectories().ToList())
            {
                Assert.IsTrue(di.Exists);
                Assert.AreNotEqual(di.EnumerateFiles().Count(), 0);
                string simpleResult = File.ReadAllText(di.EnumerateFiles().First().FullName);
                Assert.AreNotEqual(simpleResult.Count(), 0);
            }
        }

        [TestMethod()]
        [DeploymentItem(@"../../data", "data")]
        public void RunOutputsValidNamesTest()
        {
            RecognitionRunner runner = new RecognitionRunner("data", this.recogniser);
            runner.Run();
            DirectoryInfo dataDI = new DirectoryInfo("data");
            foreach (DirectoryInfo di in dataDI.EnumerateDirectories().ToList())
            {
                Assert.IsTrue(di.Exists);
                string[] fileNames = di.EnumerateFiles().Select((FileInfo fi) => fi.Name).ToArray();
                Assert.IsTrue(fileNames.Contains("1introduction.txt"));
            }
        }
    }
}