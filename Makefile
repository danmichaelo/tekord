.PHONY: ttl solr clean
.DEFAULT_GOAL := ttl

ttl: tekord.ttl
solr: tekord_solr.json

tekord_solr.json: tekord.ttl
	python ./tools/ttl2solr.py -v tekord.ttl tekord_solr.json

tekord.ttl: tekord.tmp.ttl
	rm -f skosify.log
	python ./tools/skosify-sort.py -b 'http://data.ub.uio.no/' -o tekord.ttl vocabulary.ttl tekord.tmp.ttl

tekord.tmp.ttl: tekord.rdf.xml
	rapper -i rdfxml -o turtle tekord.rdf.xml >| tekord.tmp.ttl

tekord.rdf.xml: tools tekord.xml
	cd tools && \
	git pull && \
	cd .. && \
    zorba -i tools/emneregister2rdf.xq -e "base:=ntub" -e "scheme:=http://data.ub.uio.no/tekord" \
      -e "file:=../tekord.xml" -e "signature_handler:=udc" >| tekord.rdf.xml

tools:
	git clone https://github.com/danmichaelo/ubdata-tools.git tools

#tekord.xml:
#	<eksporteres ikke automatisk fra bibsys enda>
#    wget -nv -O tekord.xml http://www.bibsys.no/files/out/humordsok/ntubregister.xml

clean:
	rm -f skosify.log
	rm -f tekord.rdf.xml
	rm -f tekord.ttl
	rm -f tekord.tmp.ttl
