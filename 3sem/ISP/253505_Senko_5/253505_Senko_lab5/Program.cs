using _253505_Senko.Domain;
using SerializerLib;
using System;
using System.Collections.Generic;

var serializer = new Serializer();

var pyramid = new Pyramid("qwerty", new List<Pharaoh> { new Pharaoh(123, "ewq"), new Pharaoh(456, "qwe") });
var pyramids = new List<Pyramid> { pyramid, pyramid, pyramid };

serializer.SerializeXML(pyramids, "file.xml");
var deserializedXML = serializer.DeSerializeXML("file.xml").ToList();

foreach (var value in deserializedXML)
{
    Console.WriteLine(value);
}

serializer.SerializeJSON(pyramids, "file.json");
var deserializedJSON = serializer.DeSerializeJSON("file.json").ToList();

foreach (var value in deserializedJSON)
{
    Console.WriteLine(value);
}

serializer.SerializeByLINQ(pyramids, "file.linq");
var deserializedLINQ = serializer.DeSerializeByLINQ("file.linq").ToList();

foreach (var value in deserializedLINQ)
{
    Console.WriteLine(value);
}


bool xmlMatch = true;
bool jsonMatch = true;
bool linqMatch = true;

for (int i = 0; i < deserializedXML.Count; i++)
{
    xmlMatch = xmlMatch && pyramids[i].Equals(deserializedXML[i]);
}

for (int i = 0; i < deserializedJSON.Count; i++)
{
    jsonMatch = jsonMatch && pyramids[i].Equals(deserializedJSON[i]);
}

for (int i = 0; i < deserializedLINQ.Count; i++)
{
    linqMatch = linqMatch && pyramids[i].Equals(deserializedLINQ[i]);
}


Console.WriteLine($"XML match: {xmlMatch}");
Console.WriteLine($"JSON match: {jsonMatch}");
Console.WriteLine($"LINQ match: {linqMatch}");