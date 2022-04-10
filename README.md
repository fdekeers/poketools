# Pokétools

Three tools to automate boring and repetitive tasks in Pokémon Brilliant Diamond/Shining Pearl,
namely:
- Stationary Pokémon shiny reset
- Masuda breeding (WORK IN PROGRESS)
- Experience farming (WORK IN PROGRESS)

### Contributors

- François DE KEERSMAEKER ([fdekeers](https://github.com/fdekeers))
- Augustin DELECLUSE ([augustindelecluse](https://github.com/augustindelecluse))
- CDMcKinley ([cdmckinley](https://github.com/cdmckinley))

## Stationary Pokémon shiny reset

Use this tool to automate the reset of stationary Pokémon,
in order to shiny hunt them.
It detects if the Pokémon is shiny by detecting the sound made by the shiny sparkles,
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
- It is preferable to mute the game music and Pokémon cries
(not the sound effects, as they are used to detect if the Pokémon is shiny or not).

### Usage
```shell
sudo python3 shiny_reset.py [-s CONFIG_NAME] [-c screenshot|video] [-p]
```

Use option `-s` or `--scenario` to indicate which scenario configuration you want to use,
i.e. which Pokémon you are hunting, where `SCENARIO` is the name of the scenario.
All configuration files are in the `configs` directory.
Specific configuration files **must** start with `cfg_` to be recognized.
However, for the `SCENARIO` command line argument, you only have to provide the scenario name,
i.e. the name between `cfg_` and the file extension `.py` (e.g. `ramanas` or `arceus`).
Currently, the following scenarios are implemented:
- `general.py`: general macros used for any scenario, should not be modified.
- `cfg_ramanas.py`: configuration for Pokémon that are encountered in the Ramanas park.
Default configuration if no scenario is provided as command line argument.
- `cfg_shaymin.py`: configuration for Shaymin, encountered in the Flower Paradise.
- `cfg_arceus.py`: configuration for Arceus, encountered in the Hall of Origin.
- `cfg_darkrai.py`: configuration for Darkrai, encountered on the New Moon Island. (IN PROGRESS)

If no configuration matches the Pokémon you want to hunt,
please contribute by adding a configuration file corresponding to this Pokémon.

Use option `-p` or `--plot-correlation` to save a graph showing the signal correlation
between the game sound recording and the template sound of the shiny sparkles,
metric that is used to detect if the shiny sparkles are present in the recording.

Use option `-c` or `--capture`, followed by `screenshot` or `video` to capture a screenshot
or video upon finding a shiny.

Use option `-d` os `--device`, followed by the name of your audio input device wrapped in quotes,
to select a specific audio device. The device names can be listed with: `python3 -m sounddevice`

## Masuda breeding

WORK IN PROGRESS


## Experience farming

WORK IN PROGRESS


## Troubleshooting

Here, we will gather some known issues, and propose potential fixes.

### PaAlsaStreamComponent_BeginPolling: Assertion `ret == self->nfds' failed.

If this error occurs, you may try to install PortAudio from the source.
To do this, do the following:

```shell
sudo apt-get remove libportaudio2
sudo apt-get install libasound2-dev
git clone -b alsapatch https://github.com/gglockner/portaudio
cd portaudio
./configure && make
sudo make install
sudo ldconfig
cd ..
```

Source: https://stackoverflow.com/questions/59006083/how-to-install-portaudio-on-pi-properly

## Special thanks

We would like to thank the following people,
that helped us by giving us helpful advice:
- Guillaume DERVAL
- Matthieu PIGAGLIO ([Countermatt](https://github.com/Countermatt))
- Olivier GOLETTI
