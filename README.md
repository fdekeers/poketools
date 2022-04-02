# Pokétools

By François DE KEERSMAEKER ([fdekeers](https://github.com/fdekeers)),
Augustin DELECLUSE ([augustindelecluse](https://github.com/augustindelecluse)),
and CDMcKinley ([cdmckinley](https://github.com/cdmckinley)).

Two tools to automate boring and repetitive tasks in Pokémon Brilliant Diamond/Shining Pearl,
namely:
- Stationary Pokémon shiny reset
- Masuda breeding (WORK IN PROGRESS)

## Stationary Pokémon shiny reset

Use this tool to automate the reset of stationary Pokémon,
in order to shiny hunt them.
It detects if the Pokemon is shiny by detecting the sound made by the shiny sparkles,
and automates the game reset if not.
The tool puts the Nintendo Switch in sleep mode
when the Pokémon has been detected to be shiny,
then stops.

### Prerequisites

- Install the required libraries:
```shell
sudo apt-get install libasound-dev portaudio19-dev libatlas-base-dev
```
- Install the required Python modules:
```shell
sudo python3 -m pip install -r requirements.txt
```
- Connect your Nintendo Switch to your computer with an audio cable,
and make sure it is considered as an audio source (i.e. a microphone).
- Make sure the game is running,
and that your character is placed just in front of the stationary Pokémon.
- Activate Bluetooth on your computer.
- Disconnect all wired controllers from your console.
- Go to the "Change Grip/Order" menu of your Nintendo Switch.
- As different Pokémon can have different input sequences needed to start the battle,
make sure the `START_BATTLE` macro, in the [macros.py](macros.py) file,
corresponds to your Pokémon.
- It is preferable to mute the game music and Pokémon cries
(not the sound effects, as they are used to detect if the Pokémon is shiny or not).

### Usage
```shell
sudo python3 shiny_reset.py [-p] [-s arceus/default] [-c screenshot/video]
```

Use option `-p` or `--plot-correlation` to save a graph showing the signal correlation
between the game sound recording and the template sound of the shiny sparkles,
metric that is used to detect if the shiny sparkles are present in the recording.

Use option `-s` or `--scenario`, followed by `arceus` to hunt Arceus as opposed to other
encounters. (W.I.P.)

Use option `-c` or `--capture`, followed by `screenshot` or `video` to capture a screenshot
or video upon finding a shiny. (W.I.P.)

## Masuda breeding

WORK IN PROGRESS


## Special thanks

We would like to thank the following people,
that helped us by giving us helpful advice:
- Guillaume DERVAL
- Matthieu PIGAGLIO ([Countermatt](https://github.com/Countermatt))
- Olivier GOLETTI
