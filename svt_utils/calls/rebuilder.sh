#!/bin/bash
export PYTHONPATH=/home/zen/code/svt_couchdb
curl -k -X DELETE http://admin:Password123@localhost:5984/svt
# curl -k -X DELETE http://localhost:5984/svt
curl -k -X PUT http://admin:Password123@localhost:5984/svt
# curl -k -X PUT http://localhost:5984/svt
python3 utils/create_ddocs.py
#curl -X POST --header 'Accept: application/json' -F 'file=@/home/zen//work/4/output_svt_2016-09-12-11-45-77.zip' http://127.0.0.1:5000/api/upload?client=test
sleep 5
#curl -X POST --header 'Accept: application/json' -F 'file=@/home/zen//work/4/output_svt_2016-09-12-11-45-77.zip' http://127.0.0.1:5000/api/upload?client=test1
sleep 5
#curl -X POST --header 'Accept: application/json' -F 'file=@/home/zen//work/4/output_svt_2016-09-12-11-45-77.zip' http://127.0.0.1:5000/api/upload?client=test2
sleep 5
#curl -X POST --header 'Accept: application/json' -F 'file=@/home/zen//work/4/output_svt_2016-09-12-11-45-77.zip' http://127.0.0.1:5000/api/upload?client=test2
sleep 5
#curl -X POST --header 'Accept: application/json' -F 'file=@/home/zen//work/PGE/output_svt_2016-09-13-10-35-57.zip'  http://127.0.0.1:5000/api/upload?client=PGE



