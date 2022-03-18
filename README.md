## A Personal Project
<p>
  After getting lectures from Evolutionary Computing Subject. I would like to create a new project that uses Evolutionary Computing Algorithm. This project has been done quite some time, I might forget few things from the lecture. Since I already made Dino game with
  <a href="https://github.com/Has-if36/BITI2223-ML-ReinforcementLearning">Reinforcement Learning</a>
, why not just make same game but with different algorithm? But this time, it has a more defined shapes.
</p>

## Evolutionary Computing Algorithm
### Population
Depends on the power of the computer, for my computer, I set at 200 of population, meaning there will 200 Dinos running in each run.

### Chromosome
Chromosome is the 'genetic' information or a group of gene for the AI to evolve, so it can improve. In this case, there are 19 informations or gene which are:

Gene | Description | Allele (Value)
---|---|---
Jump Rock | Probability to Jump over Obstacle 1 (Rock) | 0 - 1000
Duck Rock | Probability to Duck under Obstacle 1 (Rock) | 0 - 1000
Idle Rock | Probability to Do Nothing on Obstacle 1 (Rock) | 0 - 1000
Jump Plant | Probability to Jump over Obstacle 2 (Plant) | 0 - 1000
Duck Plant | Probability to Duck under Obstacle 1 (Plant) | 0 - 1000
Idle Plant | Probability to Do Nothing on Obstacle 1 (Plant) | 0 - 1000
Jump birdLo | Probability to Jump over Obstacle 3 (Bird Low Altitude) | 0 - 1000
Duck birdLo | Probability to Duck under Obstacle 1 (Bird Low Altitude) | 0 - 1000
Idle birdLo | Probability to Do Nothing on Obstacle 1 (Bird Low Altitude) | 0 - 1000
Jump birdMid | Probability to Jump over Obstacle 4 (Bird Middle Altitude) | 0 - 1000
Duck birdMid | Probability to Duck under Obstacle 1 (Bird Middle Altitude) | 0 - 1000
Idle birdMid | Probability to Do Nothing on Obstacle 1 (Bird Middle Altitude) | 0 - 1000
Jump birdHi | Probability to Jump over Obstacle 5 (Bird High Altitude) | 0 - 1000
Duck birdHi | Probability to Duck under Obstacle 1 (Bird High Altitude) | 0 - 1000
Idle birdHi | Probability to Do Nothing on Obstacle 1 (Bird High Altitude) | 0 - 1000
Duck Duration | Duration how long Dino Duck | 0 - 1000
Duck Duration SD | Standard Deviation Duration how long Dino Duck | 0 - 1000
Distance Obstacle | Distance for the Dino to take action (Jump, Duck, Do Nothing) | 0 - 1000
Distance Obstacle SD | Standard Deviation Distance for the Dino to take action (Jump, Duck, Do Nothing) | 0 - 1000
  
Note: the range value for the allele was set to 0 - 1000 because it is easier for me to initialise the Dino Chromosome.

## Results
<p align="center">
  <img width="682" height="400" src="https://user-images.githubusercontent.com/55189926/159019825-9072a993-933b-4701-93d9-93e030f44b2b.png">
  <img width="469" height="400" src="https://user-images.githubusercontent.com/55189926/159021584-60a1a7a6-d3f8-4c0a-a5e9-ab1449291b9d.png">
  <br>
  Result
</p>


