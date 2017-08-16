#!/bin/bash -e

# TODO: secrets
IP="couchdb:5984"
ADMIN="admin"
PASS="password123"
URI="http://$ADMIN:$PASS@$IP"
SVTADMIN="svtadmin"
SVTPASS="password123"
TIMEOUT=600

export PYTHONPATH="/app/"

# Define request with variable expansion

adminjson=$(cat <<EOF
{
  "action": "enable_cluster",
  "bind_address": "0.0.0.0",
  "username": "admin",
  "password": "$PASS",
  "port": "5984",
  "node_count":"1"
} 
EOF
)

svtadminjson=$(cat <<EOF
{
  "name":"$SVTADMIN", 
  "type":"user", 
  "roles":[], 
  "password":"$SVTPASS"
}
EOF
)

securityjson=$(cat <<EOF
{
  "admins": { "names" : ["$SVTADMIN"] },
  "members" : {"names" : [] }
}
EOF
)

# Wait for CouchDB container to come up

echo ">>> TEST GET"
WAIT=0
until curl -s -X GET http://$IP/ || [ $WAIT -ge $TIMEOUT ]; do
	echo ">>> Waiting for CouchDB"
	let WAIT=WAIT_TIME+60
	sleep 60
done

# Configure if needed

if ! curl -s -I -X GET "http://$IP/svt/configured" | tac | grep -q "HTTP/1.1 200"
then
	echo ">>> PUT system DB"
	curl -s -X PUT http://$IP/_users
	curl -s -X PUT http://$IP/_replicator
	curl -s -X PUT http://$IP/_global_changes
	echo ">>> Configure Cluster"
	curl  -s -X POST -H "Content-Type: application/json" http://$IP/_cluster_setup -d "$adminjson"
	curl  -s -X POST -H "Content-Type: application/json" $URI/_cluster_setup -d '{"action": "finish_cluster"}'
	echo ">>> PUT svt"
	curl -s -X PUT $URI/svt
	echo ">>> PUT SVT security"
	curl -s -g -H 'Content-Type: application/json' -X PUT -d "$svtadminjson" "$URI/_users/org.couchdb.user:$SVTADMIN"
	curl -s -g -H 'Content-Type: application/json' -X PUT -d "$securityjson" "$URI/svt/_security"
	curl -s -g -H 'Content-Type: application/json' -X PUT -d '{"_id":"configured", "ok":"true"}' "$URI/svt/configured"
fi

# update DDOCS
	
for ddoc in /app/ddocs/*.js; do
	python /app/app/update_ddoc.py -f $ddoc
done



