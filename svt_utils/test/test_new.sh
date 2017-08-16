export PYTHONPATH=/home/zen/code
for y in test/yaml/*.yaml
do 
# echo $y  
printf "."
python utils/generator.py -s PGE -c 2016-09-13-10-35-57 -y $y > test/run/$(basename $y).run
done
echo ""
for f in test/canonical/*.run
do
# echo "diff for $f"
# diff $f test/canonical/$(basename $f) 2>&1 > /dev/null
 diff $f test/run/$(basename $f) 
if [ $? != 0 ] 
then
   echo "ERROR in $f"
else
   echo "PASS for $f"
fi
done 
# rm test/run/*.run

