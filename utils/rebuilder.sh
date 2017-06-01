#!/bin/bash
export PYTHONPATH=/home/zen/code/svt_couchdb
curl -k -X DELETE http://admin:Password123@localhost:5984/svt
# curl -k -X DELETE http://localhost:5984/svt
curl -k -X PUT http://admin:Password123@localhost:5984/svt
# curl -k -X PUT http://localhost:5984/svt
python3 utils/create_ddocs.py
python3 utils/loader.py -c test1 -f /home/zen//work/4/output_svt_2016-09-12-11-45-77.zip
sleep 5
python3 utils/loader.py -c test1 -f /home/zen//work/4/output_svt_2016-09-12-11-45-99.zip 
sleep 5
python3 utils/loader.py -c test2 -f /home/zen//work/4/output_svt_2016-09-12-11-45-77.zip
sleep 5
python3 utils/loader.py -c test2 -f /home/zen//work/4/output_svt_2016-09-12-11-45-99.zip
sleep 5
python3 utils/loader.py -c PGE -f /home/zen//work/PGE/output_svt_2016-09-13-10-35-57.zip
