## Tekord

TEKORD, or TEK-ord, is a controlled vocabulary used by the NTNU University Library
(the library of the Norwegian University of Science and Technology).
It contains about 15,000 entries with Norwegian terms, each linked to a classification number from the Universal Decimal Classification (UDC).

Because TEKORD was designed for use at a technical university, the terms are heavily skewed to engineering and science although there is some coverage of other subject areas.

Tekord was first converted to RDF in 2010 and released under the Open Data Commons Public Domain Dedication Licence (ODC-PDDL) at https://www.ntnu.no/ub/data/tekord/.
An updated version was published in 2012, but no more updates were published there after a key person left the library.
Since we had to setup a conversion process for [Humord](https://github.com/scriptotek/humord),
another vocabulary on the same source format as Tekord, we decided to also run updated conversions for Tekord.

The source file `src/tekord.xml` (original name "NTUBregister.xml")
was obtained from Bibsys (now Unit), exported from their IBM Adabas database.
Last updated in June 2019.

The conversion is handled by [doit](https://pydoit.org/).

Classification codes (UDC notation) are converted to `skos:notation`,
with datatype `<http://udcdata.info/UDCnotation>`.
For more information on the data model, see [the Humord repository](https://github.com/scriptotek/humord#conversion).
