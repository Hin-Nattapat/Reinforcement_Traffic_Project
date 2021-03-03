# command randomTrips.py

python randomTrips.py -n ../4-way.net.xml -r ./Period_1/Period_1.rou.xml -e 10800 -l --validate --fringe-factor 10 --period 1 --vehicle-class passenger --trip-attributes="departLane=\"best\" departSpeed=\"random\" departPos=\"random\" length=\"4.7\" minGap=\"1.3\"" --weights-prefix ../4-way

python randomTrips.py -n ../4-way.net.xml -r ./Period_1/Period_1.rou.xml -e 1000 -l --validate --fringe-factor 10 --period 1 --trip-attributes="departLane=\"best\" departSpeed=\"random\" departPos=\"random\" type=\"vehDist\"" --weights-prefix ../4-way --additional-file vTypeDistributions.add.xml