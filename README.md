wals3
=====

This repository holds the source code of web application and the data of WALS Online (The World Atlas Of Language Structures Online.)


Cite
----

Dryer, Matthew S. & Haspelmath, Martin (eds.) 2013.
The World Atlas of Language Structures Online.
Leipzig: Max Planck Institute for Evolutionary Anthropology.
(Available online at http://wals.info, Accessed on -date-.) 

Version 2014.1: [![DOI](https://zenodo.org/badge/5142/clld/wals3.png)](http://dx.doi.org/10.5281/zenodo.10995)



Data
----

The data of version 2014.1, released in July 2014 is available as ZIP archive `data.zip`. Consult the `README.txt` in this archive for
further information.



Software
--------

The software is implemented as pyramid web app based on the clld toolkit.


Install
-------

To get WALS Online running locally, you need python 2.7 and have to run your system's equivalent to the following bash commands:

```bash
virtualenv --no-site-packages wals
cd wals/
. bin/activate
curl -O http://zenodo.org/record/11040/files/wals3-v2014.2.zip
unzip wals3-v2014.2.zip
python clld-wals3-d23d403/fromdump.py
cd wals3/
pip install -r requirements.txt
python setup.py develop
python wals3/scripts/unfreeze.py sqlite.ini
pserve sqlite.ini
```

Then you should be able to access the application by visiting http://localhost:6543 in your browser. Note that you still need an internet connection for the application to download external resources like the map tiles or javascript libraries.
