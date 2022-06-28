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
+---1__Task 1
¦   ¦   presentation.pdf
¦   ¦   presentation.pptx
+---2__Task 2
¦   ¦   KG Assessment - Dimensions and Metrics.pdf
+---3__Scraper
¦   ¦   README.md
¦   ¦   requirements.txt
¦   ¦   log.csv
¦   ¦   firmenregister.json
¦   ¦   scraper.py
+---4__Scraper_results
¦   ¦   firmenregister.json
¦   ¦   log.csv
+---5__Mappings
¦   +---mapping_firmenregister
¦   ¦   ¦   index.js
¦   ¦   ¦   firmenregister.json
¦   ¦   ¦   firmenregister.n3
¦   ¦   ¦   mapping.ttl
¦   +---mapping_wikidata
¦   ¦   ¦   .....
+---6__Assessment
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
+---7__Duplicate_Detection/Duke
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
¦   ¦   ¦   SHACL_Code.txt
¦   ¦   ¦   Violation_Reports.txt
¦   ¦   ¦   hotels.nt
+---9__Knowledge_Graph
¦   ¦   ¦   Just_Hotels.nt
```
