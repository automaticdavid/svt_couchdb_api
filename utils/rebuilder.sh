#!/bin/bash
curl -k -X DELETE http://localhost:5984/svtdev
curl -k -X PUT http://localhost:5984/svtdev
python utils/create_ddocs.py
python utils/loader.py -c test1 -f ../work/4/output_svt_2016-09-12-11-45-77.zip
python utils/loader.py -c test1 -f ../work/4/output_svt_2016-09-12-11-45-99.zip 
python utils/loader.py -c test2 -f ../work/4/output_svt_2016-09-12-11-45-77.zip
python utils/loader.py -c test2 -f ../work/4/output_svt_2016-09-12-11-45-99.zip
python utils/loader.py -c PGE -f ../work/PGE/output_svt_2016-09-13-10-35-57.zip
