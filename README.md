# Pokétools
Tool to automate static Pokémon shiny resets in Pokémon BDSP.

### Usage
```shell
sudo python3 shiny_reset.py [-r]
```

Use the `-r` flag to bypass virtual controller synchronization,
and directly connect it to the console,
if this is not the first time you connect to a Switch.

### Needed Python modules
See requirements file `requirements.txt`.
Install modules with the following command:
```
sudo python3 -m pip install -r requirements.txt
```


### Console / game settings
- Game sound setting
  - Music: 0
  - Sound effects: 8
  - Pokémon cries: 0
- Switch sound setting: 8
