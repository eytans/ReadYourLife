using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace DataComparer
{
    public interface IRecogniser
    {
        string RecogniseDefault(string fileName);
        string RecogniseCustom(string fileName);
    }
}
