# GameMaster

**GameMaster** is a Python-based sports scoreboard tool for OBS. In addition to basic scoring functionality, **GameMaster** can also manage game times, periods, and any other stats or variables related to the sport at hand using a simple JSON configuration file.

## Quick-start guide

GameMaster is distributed using a single executable installer. Following the provided instructions with the installer should produce no errors and install correctly.

1.  Download the GameMaster installer using the button above.
2. On the second panel, you can see what the current version is, and any necessary release notes. Click next.
3. We recommend that you install GameMaster into the default location, which, in this instance, will be in your Documents folder. Click next.
4. Begin the installation. By default, GameMaster will run on the completion of the installation.  
5. Inside the newly created `\Documents\GameMaster\` folder, you can find the executable, an uninstaller, the icon, the dependencies folder, and an output files folder.
6. To use the outputs in OBS, just create OBS text sources that "Read from file", and select whichever of the output files you want.

## Planned Features

| Next Update | Near-term | Long-term |
|-|--|-|
| Settings |Player Details | Sound board |
| Config error handling | Config Presets | Config creator
| Config updating |Hotkeys|
| First-run config setup
| Fixing time output (hours)

## Info

Latest Version:  **1.0.2**

Release notes:

- 1.0.2
  - Updated installer to not require admin (it shouldn't have in the first place)
  - Included installer art  
  
- 1.0.0  
  - Initial release  
  - Default Football configuration included. Documentation can be found at <https://www.datastream.cf/projects/gamemaster/>  
  - Note: Hangs or snags in the timer are due to OBS only checking the files for changes one time per second. GameMaster is outputting the correct timestamp at the right time, but OBS may not be displaying it in sync.  
  - Not working: "Clear time" button (disabled)  
  - Not Implemented: Player information feed, Config editor, First-run setup

## Documentation

*Please check back later. Config documentation is still in the works.*

---
Something not right? Found a bug? No problem, just leave a detailed report on the Issues page here, and I'll get to it as soon as possible.
Thanks for stickin' with this, and please enjoy **GameMaster**!

*Cheers,
TheLittleDoctor*
