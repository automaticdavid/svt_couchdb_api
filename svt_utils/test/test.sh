declare -A errors 
for y in $PWD/yamldefs/*.yaml
do 
	echo $y  

	json='{
		"yamldef": "'$y'", 
                "date": "2016-09-13-10-35-57",
                "client": "PGE" 
	}'

	curl -X POST --header 'Content-Type: application/json' --header 'Accept: application/json' -d "$json" http://127.0.0.1:5000/api/generate > $PWD/test/run/$(basename $y).run

	if [ $? -ne 0 ]; then
		errors[$(basename $y)]=1
	fi
done
for f in test/canonical/*.run
do
	# echo "$(basename $f)"
 	diff $f test/run/$(basename $f) 2>&1 > /dev/null
	if [ $? != 0 ] || [[ ${errors[$(basename $f .run)]} ]]
	then
   		echo "ERROR in $f"
	else
		echo "SUCCESS for $f"
	fi
done 
# rm test/run/*.run


