n=10
i=2
while test $i -le $n
do
    cd .. 
    source venv/bin/activate
    cd logic_gates
    python main_xor.py $i >> results/results_xor-$i.txt
    i=`expr $i + 1`

done