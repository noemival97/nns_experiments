n=10
i=1
while test $i -le $n
do
    cd .. 
    source venv/bin/activate
    cd logic_gates
    python main_or.py $i >> ./results/results_or-$i.txt 
    i=`expr $i + 1`
done