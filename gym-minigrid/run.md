# for Game 1: MiniGrid-Empty-5x5-v0
## Training:
    python3 -m scripts.train --algo a2c --env MiniGrid-Empty-5x5-v0 --model Empty5_a2c --save-interval 10 --frames 80000
## Evaluate:
    python3 -m scripts.evaluate --env MiniGrid-Empty-5x5-v0 --model Empty5_a2c --argmax
## Save to gif:
    python3 -m scripts.visualize --env MiniGrid-Empty-5x5-v0 --model Empty5_a2c --argmax --gif empty5x5 --episodes 5
## Gendata:
    python3 -m scripts.visualize --env MiniGrid-Empty-5x5-v0 --model Empty5_a2c --argmax --gif empty5x5 --episodes 1

# for Game 2: MiniGrid-DoorKey-5x5-v0
## Training:
    python3 -m scripts.train --algo a2c --env MiniGrid-DoorKey-5x5-v0 --model d5x5 --save-interval 10
## Evaluate:
    python3 -m scripts.evaluate --env MiniGrid-DoorKey-5x5-v0 --model d5x5 --argmax
## Save to gif:
    python3 -m scripts.visualize --env MiniGrid-DoorKey-5x5-v0 --model d5x5 --argmax --gif door5x5 --episodes 5
## Gendata:
    python3 -m scripts.visualize --env MiniGrid-DoorKey-5x5-v0 --model d5x5 --argmax --gif door5x5 --episodes 1

# for Game 3: MiniGrid-DoorKey-6x6-v0
## Training:
    python3 -m scripts.train --algo a2c --env MiniGrid-DoorKey-6x6-v0 --model d6x6 --save-interval 10
## Evaluate:
    python3 -m scripts.evaluate --env MiniGrid-DoorKey-6x6-v0 --model d6x6 --argmax
## Save to gif:
    python3 -m scripts.visualize --env MiniGrid-DoorKey-6x6-v0 --model d6x6 --argmax --gif door6x6 --episodes 5
## Gendata:
    python3 -m scripts.visualize --env MiniGrid-DoorKey-6x6-v0 --model d6x6 --argmax --gif door6x6 --episodes 1

# for Game 4: MiniGrid-DoorKey-8x8-v0
## Training:
    python3 -m scripts.train --algo a2c --env MiniGrid-DoorKey-8x8-v0 --model DoorKey8 --save-interval 10
## Evaluate:
    python3 -m scripts.evaluate --env MiniGrid-DoorKey-8x8-v0 --model DoorKey8 --argmax
## Save to gif:
    python3 -m scripts.visualize --env MiniGrid-DoorKey-8x8-v0 --model DoorKey8 --argmax --gif door8x8 --episodes 5
## Gendata: **************************************************************************************************
    python3 -m scripts.visualize --env MiniGrid-DoorKey-8x8-v0 --model DoorKey8 --argmax --gif door8x8 --episodes 1
## ***********************************************************************************************************

# for Game 5: MiniGrid-Empty-16x16-v0
## Training:
    python3 -m scripts.train --algo a2c --env MiniGrid-Empty-16x16-v0 --model e16x16 --save-interval 10
## Evaluate:
    python3 -m scripts.evaluate --env MiniGrid-Empty-16x16-v0 --model e16x16 --argmax
## Save to gif:
    python3 -m scripts.visualize --env MiniGrid-Empty-16x16-v0 --model e16x16 --argmax --gif door8x8 --episodes 5
## Gendata:
    python3 -m scripts.visualize --env MiniGrid-Empty-16x16-v0 --model e16x16 --argmax --gif door8x8 --episodes 1