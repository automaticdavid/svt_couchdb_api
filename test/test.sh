for y in test/yaml/*.yaml
do 
echo $y  
python utils/generator.py -s PGE -c 2016-09-13-10-35-57 -y $y > test/run/$(basename $y).run
done
for f in test/run/*.run
do
echo "diff for $f"
# diff $f test/canonical/$(basename $f) 2>&1 > /dev/null
 diff $f test/canonical/$(basename $f) 
if [ $? != 0 ] 
then
   echo "ERROR in $f"
fi
done 
# rm test/run/*.run
