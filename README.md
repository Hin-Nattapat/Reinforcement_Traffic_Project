# Reinforcement Learning for Controlling Traffic

This is our graduation project 
"Training Reinforcement Learning Agent for traffic Signal Control"

So we use Reinforcement learning for control traffic signal and use simulation of urban mobility(SUMO)
for simulate traffic network , we use Traci[python script] for communication between Reinforcement learning and SUMO

# Generate route file

This command will generate routing that contain many types of car depend on `map/4-way/Rou_File/vTypeDistributions.add.xml`

This command will generate route file :
```

python randomTrips.py -n ./4-way/4-way.net.xml -r ./4-way/route/Period_3.rou.xml -e 10800 -l --validate --period 1.2 --trip-attributes="departLane=\"random\" departSpeed=\"random\" departPos=\"random\" type=\"vehDist\"" --weights-prefix ./4-way/4-way --additional-file vTypeDistributions.add.xml

python randomTrips.py -n ./16-way/16-way.net.xml -r ./16-way/route/Period_3.rou.xml -e 10800 -l --validate --period 1 --trip-attributes="departLane=\"random\" departSpeed=\"random\" departPos=\"random\" type=\"vehDist\"" --weights-prefix ./16-way/16-way --additional-file vTypeDistributions.add.xml --min-distance 2500 

python randomTrips.py -n ./36-way/36-way.net.xml -r ./36-way/route/Period_3.rou.xml -e 10800 -l --validate --period 1 --trip-attributes="departLane=\"random\" departSpeed=\"random\" departPos=\"random\" type=\"vehDist\"" --weights-prefix ./36-way/36-way --additional-file vTypeDistributions.add.xml --min-distance 7500


```

16-way => --min-distance 2500 
36-way => --min-distance 7500 

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

# Edge 4-way
* 'TFL_1' : ['gneE8', 'gneE10', 'gneE12', 'gneE14'] 

# Rou 4-way
* File Period_1 : Period 0.8
* File Period_2 : Period 1
* File Period_3 : Period 1.2

# Edge 16-way
* 'TFL_1' : ['InB_WN_2', 'InB_NW_2', 'Mid_N_2', 'Mid_W_1'],
* 'TFL_2' : ['Mid_N_1', 'InB_NE_2', 'InB_EN_2', 'Mid_E_1'],
* 'TFL_3' : ['Mid_S_1', 'Mid_E_2', 'InB_ES_2', 'InB_SE_2'],
* 'TFL_4' : ['InB_WS_2', 'Mid_W_2', 'Mid_S_2', 'InB_SW_2']

# Rou 16-way
* File Period_1 : Period 0.6
* File Period_2 : Period 0.8
* File Period_3 : Period 1

# Edge 36-way
* 'TFL_1' : ['InB_WN_2', 'InB_NW_2', 'Mid_NW_2', 'Mid_WN_1'],
* 'TFL_2' : ['Mid_NW_1', 'InB_NM_2', 'Mid_NE_2', 'Mid_N_1'],
* 'TFL_3' : ['Mid_NE_1', 'InB_NE_2', 'InB_EN_2', 'Mid_EN_1'],
* 'TFL_4' : ['InB_WM_2', 'Mid_WN_2', 'Mid_W_2', 'Mid_WS_1'],
* 'TFL_5' : ['Mid_W_1', 'Mid_N_2', 'Mid_E_2', 'Mid_S_1'],
* 'TFL_6' : ['Mid_E_1', 'Mid_EN_2', 'InB_EM_2', 'Mid_ES_1'],
* 'TFL_7' : ['InB_WS_2', 'Mid_WS_2', 'Mid_SW_2', 'InB_SW_2'],
* 'TFL_8' : ['Mid_SW_1', 'Mid_S_2', 'Mid_SE_2', 'InB_SM_2'],
* 'TFL_9' : ['Mid_SE_1', 'Mid_ES_2', 'InB_ES_2', 'InB_SE_2']

# Rou 36-way
* File Period_1 : Period 0.6
* File Period_2 : Period 0.8
* File Period_3 : Period 1

# How to run?
* Choose solution ( fix = normal , PRL = model in paper , SRL = our model)
* Choose running map (4,16,36)
