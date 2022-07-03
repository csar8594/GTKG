# GTKG

This is the repository of the *Knowledge Graphs* seminar project at UIBK.

The main goal here is the 
- creation
- curation 
- extension

of the German Tourism Knowledge Graph *(GTKG)*

### Folder structure:

```
GTKG
¦   README.md   
+---1__Sources_Research
¦   ¦   presentation.pdf
¦   ¦   presentation.pptx
+---2__Dimensions_Metrics
¦   ¦   KG Assessment - Dimensions and Metrics.pdf
¦   ¦   KG Assessment - Dimensions and Metrics.docx
¦   ¦   presentation.pdf
¦   ¦   presentation.pptx
+---3__Scraper
¦   ¦   README.md
¦   ¦   requirements.tx
¦   ¦   log.csv
¦   ¦   firmenregister.json
¦   ¦   scraper.py
+---4__Scraper_Results
¦   ¦   firmenregister.json
¦   ¦   log.csv
+---5__Mappings
¦   +---mapping_firmenregister
¦   ¦   ¦   index.js
¦   ¦   ¦   firmenregister.json
¦   ¦   ¦   firmenregister.n3
¦   ¦   ¦   mapping.ttl
¦   +---mapping_wikidata
¦   ¦   ¦   index.js
¦   ¦   ¦   mapping.ttl
¦   ¦   ¦   mapping_results.n3
¦   ¦   ¦   sparql_query_wikidata.txt
¦   ¦   ¦   wikidata_sparql_query_result.json
+---6__Assessment
¦   ¦   presentation.pdf
¦   ¦   presentation.pptx
¦   +---assessment_firmenregister
¦   ¦   ¦   convert.sh
¦   ¦   ¦   firmenregister.json
¦   ¦   ¦   assessing.py
¦   ¦   ¦   requirements.txt
¦   ¦   ¦   manualChecking.csv
¦   +---assessment_wikidata
¦   ¦   ¦   convert.sh
¦   ¦   ¦   wikidata.json
¦   ¦   ¦   assessing.py
¦   ¦   ¦   requirements.txt
¦   ¦   ¦   manualChecking.csv
+---7__Duplicate_Detection
¦   +---Duke
¦   ¦   ¦   Dockerfile
¦   ¦   ¦   Dockerfile_alt
¦   ¦   ¦   config.xml
¦   ¦   ¦   duke-core-1.3-SNAPSHOT.jar
¦   ¦   ¦   entrypoint.sh
¦   ¦   ¦   generatedDuplicateCheckFile.nt
¦   ¦   ¦   hotels.nt
¦   ¦   ¦   out.txt
¦   ¦   ¦   reports_2.txt
¦   ¦   ¦   reports_3.txt
¦   ¦   ¦   reports_4.txt
+---8__Error_Detection
¦   ¦   SHACL_Code.txt
¦   ¦   Violation_Reports.txt
¦   ¦   hotels.nt
+---9__Final_Knowledge_Graph
¦   ¦   presentation.pdf
¦   ¦   presentation.pptx
¦   ¦   Just_Hotels.nt
```
