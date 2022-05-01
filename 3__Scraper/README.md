# Scraper

This is the scraper of the *Knowledge Graphs* seminar project at UIBK.

The main goal here is to scrape *firmenregister.de* 
and find all hotels including the corresponding available
hotel information and store it in a .json file.

## Programming Language:
- Python

## Prerequisites:
### Installed system packages:
Make sure your **Linux**-System has the following packages installed:
- *python3*
- *python-pip*

> **_NOTE:_**  It is necessary to have pip installed since the
> craper installes some dependencies from *requirements.txt*

## Running the Regex-Matcher:

To start the program one can run the command in a terminal:

> python3 scraper.py

or

> python scraper.py

depending on the Linux Distro you are running.

> **_NOTE:_**  It is recommended to execute the program in a folder
> where you have write access since the programm outpouts
> to a .json and .csv file