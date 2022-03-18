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

### Fitness Function
The formula to determine the best chromosome is:
<p align="center">
  <img width="266" height="100" src="https://user-images.githubusercontent.com/55189926/159027072-eee6f9e7-f860-41d0-aa79-cf6427b8070d.png">
</p>

### Parent Selection
Top 20 Population were picked at the end of the generation. The 20 best scorer will be selected and the rest will be eliminated.

### Crossover
Similar to reproduction, two chromosome will become parent and perform crossover (exchanging genetics information). In the end, it will produce 2 children. N Point crossover were implmented for crossover. If I still remember, the parent will be kept after the crossover in order to secure the best genetics.

### Mutation
After the crossover, there is a chance for the children to mutate. The mutation rate is 0.1, meaning if there is 180 children, there may be around 18 children that will have mutation. This adds the randomness in this algorithm, hoping that we can get better gene, knowing that there is a risk that we can get terrible gene.

## Results
<p align="center">
  <img width="682" height="400" src="https://user-images.githubusercontent.com/55189926/159019825-9072a993-933b-4701-93d9-93e030f44b2b.png">
  <img width="469" height="400" src="https://user-images.githubusercontent.com/55189926/159021584-60a1a7a6-d3f8-4c0a-a5e9-ab1449291b9d.png">
  <br>
  Result
</p>

For this run, it has been run for over 50 generations. From here, we can see the there is an increase of score, meaning that the Dino gets better over the course of whole run. On average score, we can see that there are times that the score of the dino falls. This may due to being unlucky as this algorithm has randomness. It can also be due to mutation for getting bad gene, which could drag down the average average score of the generation.
