# command randomTrips.py

python randomTrips.py -n ../4-way.net.xml -r .rou.xml -e 10800 -l --validate --fringe-factor 10 --period 1 --vehicle-class passenger --trip-attributes="departLane=\"best\" departSpeed=\"random\" departPos=\"random\" length=\"4.7\" minGap=\"1.3\"" --weights-prefix ../4-way
