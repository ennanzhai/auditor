#!/bin/bash

user="ez73"
host="128.36.231.35"

i=1;

for line in `cat iplist.txt`; do
    name="hard"-$i".xml"
    ((i++));
    echo "Getting hardware information from: $line ..."
    ssh $user@$line /home/accts/ez73/lshw/./lshw -xml >> tmpHard.xml | ssh $user@$line /home/accts/ez73/lshw/./lshw -xml > $name
done

./filter.sh tmpHard.xml hard.xml
rm tmpHard.xml

echo "<root>" > tmp.xml
cat hard.xml >> tmp.xml
echo "</root>" >> tmp.xml
cp tmp.xml hard.xml
rm tmp.xml

j=0

for ((j = i-1; j >= 1; j--))
do
    echo "<root>" > tmp.xml
    cat hard-$j.xml >> tmp.xml
    echo "</root>" >> tmp.xml
    ./filter.sh tmp.xml hard-$j.xml
    #cp tmp.xml hard-$j.xml
done

rm tmp.xml

echo "Hardware information collection is finished!"


#spawn ssh $user@$host lshw -xml > hard.xml

#expect "*assword*"
#send "$pass\r"

#spawn scp $user@$host:~/hard.xml .
#expect "*assword*"
#send "$pass\r"

#interact
