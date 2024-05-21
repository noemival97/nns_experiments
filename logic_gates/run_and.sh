n=10
i=1
while test $i -le $n
do
    cd .. 
    source venv/bin/activate
    cd logic_gates
    python main_and.py $i >> results3_and-$i.txt
    i=`expr $i + 1`
done