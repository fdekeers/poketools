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
- `nxbt`
- `sounddevice`
- `scipy.io.wavfile`

Use `sudo pip3 install MODULE` to install the modules.

### Console / game settings
- Game sound setting
  - Music: 0
  - Sound effects: 8
  - Pokémon cries: 0
- Switch sound setting: 8
