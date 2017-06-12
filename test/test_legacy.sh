declare -A errors 
for y in yamldefs/*.yaml
do 
	echo $y  
	python3 utils/generator.py -s PGE -c 2016-09-13-10-35-57 -y $y > test/run/$(basename $y).run
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


