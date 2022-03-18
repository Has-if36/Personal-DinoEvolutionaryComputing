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

Gene | Description
---|---
Jump Rock | Probability to Jump over Obstacle 1 (Rock)
Duck Rock | Probability to Duck under Obstacle 1 (Rock)
Idle Rock | Probability to Do Nothing on Obstacle 1 (Rock)
Jump Plant | Probability to Jump over Obstacle 2 (Plant)
Duck Plant | Probability to Duck under Obstacle 1 (Plant)
Idle Plant | Probability to Do Nothing on Obstacle 1 (Plant)
Jump birdLo | Probability to Jump over Obstacle 3 (Bird Low Altitude)
Duck birdLo | Probability to Duck under Obstacle 1 (Bird Low Altitude)
Idle birdLo | Probability to Do Nothing on Obstacle 1 (Bird Low Altitude)
Jump birdMid | Probability to Jump over Obstacle 4 (Bird Middle Altitude)
Duck birdMid | Probability to Duck under Obstacle 1 (Bird Middle Altitude)
Idle birdMid | Probability to Do Nothing on Obstacle 1 (Bird Middle Altitude)
Jump birdHi | Probability to Jump over Obstacle 5 (Bird High Altitude)
Duck birdHi | Probability to Duck under Obstacle 1 (Bird High Altitude)
Idle birdHi | Probability to Do Nothing on Obstacle 1 (Bird High Altitude)
Duck Duration | Duration how long Dino Duck
Duck Duration SD | Standard Deviation Duration how long Dino Duck
Distance Obstacle | Distance for the Dino to take action (Jump, Duck, Do Nothing)
Distance Obstacle SD | Standard Deviation Distance for the Dino to take action (Jump, Duck, Do Nothing)

