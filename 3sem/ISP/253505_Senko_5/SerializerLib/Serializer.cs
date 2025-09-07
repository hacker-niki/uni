using System.Collections.Generic;
using System.IO;
using System.Text.Json;
using System.Xml.Linq;
using System.Xml.Serialization;
using _253505_Senko.Domain;

namespace SerializerLib
{
    public class Serializer : ISerializer
    {
        public IEnumerable<Pyramid> DeSerializeByLINQ(string fileName)
        {
            XDocument xDocument = XDocument.Load(fileName);
            XElement xPyramids = xDocument.Root;

            if (xPyramids != null)
            {
                foreach (var xPyramid in xPyramids.Elements("pyramid"))
                {
                    string name = (string)xPyramid.Element("name");
                    var xPharaohs = xPyramid.Element("pharaohs");

                    if (name != null && xPharaohs != null)
                    {
                        var pharaohs = new List<Pharaoh>();

                        foreach (var xPharaoh in xPharaohs.Elements("pharaoh"))
                        {
                            int yearsOld = (int)xPharaoh.Element("yearsOld");
                            string pharaohName = (string)xPharaoh.Element("name");

                            if (yearsOld != 0 && pharaohName != null)
                            {
                                pharaohs.Add(new Pharaoh(yearsOld, pharaohName));
                            }
                        }

                        yield return new Pyramid(name, pharaohs);
                    }
                }
            }
        }

        public IEnumerable<Pyramid> DeSerializeXML(string fileName)
        {
            XmlSerializer serializer = new XmlSerializer(typeof(List<Pyramid>));
            using (FileStream fs = new FileStream(fileName, FileMode.OpenOrCreate))
            {
                var list = (List<Pyramid>)serializer.Deserialize(fs);
                foreach (var item in list)
                {
                    yield return item;
                }
            }
        }

        public IEnumerable<Pyramid> DeSerializeJSON(string fileName)
        {
            string jsonString = File.ReadAllText(fileName);
            var pyramids = JsonSerializer.Deserialize<List<Pyramid>>(jsonString);

            foreach (var pyramid in pyramids)
            {
                yield return pyramid;
            }
        }

        public void SerializeByLINQ(IEnumerable<Pyramid> pyramids, string fileName)
        {
            XDocument xDocument = new XDocument();
            XElement xPyramids = new XElement("pyramids");
            foreach (var pyramid in pyramids)
            {
                XElement xPyramid = new XElement("pyramid");
                xPyramid.Add(new XElement("name", pyramid.Name));
                XElement xPharaohs = new XElement("pharaohs");
                foreach (var pharaoh in pyramid.Pharaohs)
                {
                    XElement xPharaoh = new XElement("pharaoh");
                    xPharaoh.Add(new XElement("name", pharaoh.Name));
                    xPharaoh.Add(new XElement("yearsOld", pharaoh.YearsOld));
                    xPharaohs.Add(xPharaoh);
                }

                xPyramid.Add(xPharaohs);
                xPyramids.Add(xPyramid);
            }

            xDocument.Add(xPyramids);
            xDocument.Save(fileName);
        }

        public void SerializeXML(IEnumerable<Pyramid> pyramids, string fileName)
        {
            XmlSerializer xmlSerializer = new XmlSerializer(typeof(List<Pyramid>));

            using (FileStream fs = new FileStream(fileName, FileMode.OpenOrCreate))
            {
                xmlSerializer.Serialize(fs, pyramids);
            }

            Console.WriteLine("Object has been serialized");
        }

        public void SerializeJSON(IEnumerable<Pyramid> pyramids, string fileName)
        {
            string jsonString = JsonSerializer.Serialize(pyramids);
            File.WriteAllText(fileName, jsonString);

            Console.WriteLine("Data has been saved to file");
        }
    }
}