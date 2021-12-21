![GameMaster Logo, wordmark, and BBG logo](https://github.com/TheLittleDoc/GameMaster/blob/master/header.png)
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

Latest Release:  **1.0.2**
Latest Build:  1.2.0-Pre1

Release notes:
<details>
  <summary>1.2.0-Pre1</summary>
  <ul>
    <ul>
      <li>- Updated to config version 2 (documentation forthcoming (for real, this time))</li>
      <li>- Added config updater (needs work)</li>
      <li>- Added application settings</li>
      <li>- Added time output format options</li>
      <li>- Fixed time only outputting in MM:SS (see above)</li>
      <li>- Added preliminary config swapper</li>
      <li>- Added basic first-run detection</li>
      <li>- Added config error detection (needs work)</li></li>
      <li>- Added static header image</li>
      <li>- Reworked general formatting back-end</li>
      <li>- Not working: "Clear time" button (disabled)</li>
      <li>- Not Implemented: Player information fed, Config editor, First-run setup, Alarm</li>
      <li>- Note: If Pre1 is successful on other machines, Pre2 will focus on cleaning up and ironing-out first-run and error detection, Pre3 will fix config updater, and RC1 may debut custom installer.</li>
  </ul>
  </ul>
</details>

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
