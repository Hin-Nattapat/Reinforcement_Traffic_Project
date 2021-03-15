# Reinforcement Learning for Controlling Traffic

This is our graduation project 
"Training Reinforcement Learning Agent for traffic Signal Control"

So we use Reinforcement learning for control traffic signal and use simulation of urban mobility(SUMO)
for simulate traffic network , we use Traci[python script] for communication between Reinforcement learning and SUMO

# Generate route file

This command will generate routing that contain many types of car depend on `map/4-way/Rou_File/vTypeDistributions.add.xml`

This command will generate route file :
```
python randomTrips.py -n ../4-way.net.xml -r ./Period_1/Period_1.rou.xml -e 1000 -l --validate --fringe-factor 10 --period 1 --trip-attributes="departLane=\"best\" departSpeed=\"random\" departPos=\"random\" type=\"vehDist\"" --weights-prefix ../4-way --additional-file vTypeDistributions.add.xml
```

<!-- # Running simulation

Run simulator with normal traffic light solution : -->
# Result from simulation

After simulate traffic for `'n'` seconds, simulation will return these value after collecting them every `'m'` seconds
* result [0] = flow rate
* result [1] = speed
* result [2] = density
* result [3] = waiting time
* result [4] = arrival rate
* result [5] = queue length

