declare -A errors 
for y in test/yaml/*.yaml
do 
	echo $y  
	python utils/generator.py -s PGE -c 2016-09-13-10-35-57 -y $y > test/run/$(basename $y).run
	if [ $? -ne 0 ]; then
		errors[$(basename $y)]=1
	fi
done
for f in test/canonical/*.run
do
# echo "$(basename $f)"
	diff $f test/canonical/$(basename $f) 2>&1 > /dev/null
 	# diff $f test/run/$(basename $f) 
	if [ $? != 0 ] || [[ ${errors[$(basename $f .run)]} ]]
	then
   		echo "ERROR in $f"
	else
		echo "PASS for $f"
	fi
done 
# rm test/run/*.run

# echo ${!errors[@]}
