# command randomTrips.py

python randomTrips.py -n ../16-way.net.xml --weights-output-prefix ../16-way

New Folder Name Period_0_5,Period_1

python randomTrips.py -n ../16-way.net.xml -r ./Period_0.5/Period_0.5.rou.xml -e 10800 -l --validate --fringe-factor 10 --period 0.5 --vehicle-class passenger --trip-attributes="departLane=\"best\" departSpeed=\"random\" departPos=\"random\" length=\"4.7\" minGap=\"1.3\"" --weights-prefix ../16-way

python randomTrips.py -n ../16-way.net.xml -r ./Period_1/Period_1.rou.xml -e 10800 -l --validate --fringe-factor 10 --period 1 --vehicle-class passenger --trip-attributes="departLane=\"best\" departSpeed=\"random\" departPos=\"random\" length=\"4.7\" minGap=\"1.3\"" --weights-prefix ../16-way
