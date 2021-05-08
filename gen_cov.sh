echo "Starting at `date -Iminutes`"
#cleanup and prep 
rm h3_4_*.txt
mkdir -p archive

#generate index
./gen_h3_index.py

for i in 25 35; do 
  echo "Starting $i degrees at `date -Iminutes`"
  seq 0 15 | parallel -j16 "./main.py {} 16 $i"
  ./merge_cover.py
  mv h3_4_cov_full.txt archive/h3_4_cov_op_`date -u +%F`_$i.txt
  mv h3_4_cov_op.bin h3_4_cov_op_$i.bin
  cp h3_4_cov_op_$i.bin archive/h3_4_cov_op_`date -u +%F`_$i.bin
  rm h3_4_cov_*.txt
  echo "Finished $i degrees at `date -Iminutes`"
done

#archive tle for today
mv tle_cache/starlink.txt tle_cache/starlink-`date -u +%F`.txt

#cleanup
rm h3_4_*.txt
echo "Done at `date -Iminutes`"
