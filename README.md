## Tekord

TEKORD, or TEK-ord, is a controlled vocabulary used by the NTNU University Library
(the library of the Norwegian University of Science and Technology).
It contains about 15,000 entries with Norwegian terms, each linked to a classification number from the Universal Decimal Classification (UDC).

Because TEKORD was designed for use at a technical university, the terms are heavily skewed to engineering and science although there is some coverage of other subject areas.

### Data source

The source file `src/tekord.xml` (original name "NTUBregister.xml")
was obtained from Bibsys (now Unit), exported from their IBM Adabas database.
Last updated in June 2019, when the database was shutdown.

### Conversion

Tekord was first converted to RDF in 2010 and released under the Open Data Commons Public Domain Dedication Licence (ODC-PDDL) at https://www.ntnu.no/ub/data/tekord/.
An updated version was published in 2012, but no more updates were published there after a key person left the library.

At the University of Oslo Library, we later had to setup a conversion process for
[Humord](https://github.com/scriptotek/humord), another vocabulary on the same source format as Tekord,
so we decided to also run updated conversions for Tekord.
The result is found in this repository, and can be browsed using Skosmos at https://data.ub.uio.no/skosmos/tekord/.

Run `doit build` to run the conversion using the [doit](https://pydoit.org/) build tool.

### Data model

See [the Humord repository](https://github.com/scriptotek/humord#conversion)
for details.

One difference from Humord is that Tekord entries are linked to classification codes.
Currently, we model these using `skos:notation` with datatype `<http://udcdata.info/UDCnotation>`.
It's possible that it would be better to consider these as mappings to UDC.
Unfortunately, UDC is only [partly available as linked open data](http://www.udcdata.info/)
(UDC Summary contains around 2,600 classes out of the more than 70,000 classes in UDC).
