using Microsoft.VisualStudio.TestTools.UnitTesting;
using DataComparer;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace DataComparer.Tests
{
    [TestClass()]
    public class RecogniserTests
    {
        private Recogniser rec;

        [TestInitialize()]
        public void SetUp()
        {
            rec = new Recogniser();
        }

        [TestMethod()]
        [DeploymentItem("../../eric.wav", "TestData")]
        public void RecogniseDefaultTest()
        {
            string result = rec.RecogniseDefault("TestData/eric.wav");
            Assert.AreNotEqual(null, result);
            Assert.AreNotEqual("", result);
        }

        [TestMethod()]
        [DeploymentItem("../../eric.wav", "TestData")]
        public void RecogniseCustomTest()
        {
            string result = rec.RecogniseCustom("TestData/eric.wav");
            Assert.AreNotEqual(null, result);
            Assert.AreNotEqual("", result);
        }
    }
}