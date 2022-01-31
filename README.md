![GameMaster Logo, wordmark, and BBG logo](https://github.com/TheLittleDoc/GameMaster/blob/master/header.png)
# GameMaster       [![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/I2I694490)
**GameMaster** is a Python-based sports scoreboard tool for OBS. In addition to basic scoring functionality, **GameMaster** can also manage game times, periods, and any other stats or variables related to the sport at hand using a simple JSON configuration file.


## Quick-start guide

**GameMaster** is distributed using a single executable installer. Following the provided instructions with the installer should produce no errors and install correctly.

### Windows installation instructions

1.  Download the  **GameMaster** installer from our [GitHub releases page](https://github.com/TheLittleDoc/GameMaster/releases/tag/v2.1.0). v2.1.0 and later include an automatic update check, so you'll now know if a new version is available.  
2.  Run the installer and follow the installation directions.  
3.  We recommend that you install  **GameMaster** into the default location, which, in this instance, will be in your local applications folder.  
4.  When the installation is complete, a  **GameMaster** setup tool will run which will allow you to setup up your own config file or pick from a list of examples. It may take a moment to start. Follow all setup instructions.  
5.  Review the newly-created config file before finishing the setup tool.  
6.  Following the conclusion of the setup tool,  **GameMaster**  will reload and appear populated as you configured it.  
7.  To use the outputs in OBS, just create OBS text sources that "Read from file", and select whichever of the output files you want.  

### Mac installation instructions
*Mac binaries are currently under development. If you're feeling brave, you can try to run it from the source on the [Mac branch](https://github.com/TheLittleDoc/GameMaster/tree/mac), but I can't recommend it or offer much support.*  

## Planned Features
| Next Update               | Near-term                             | Long-term                             |
|---------------------------|---------------------------------------|---------------------------------------|
| Hotkeys                   | Player Details                        | Sound board                           |
| Settings tab              | Scoreboard overlay creator            | Graphical scoreboard output (flask)   |
| Player details            | Config Preset uploader                |                                       |
| Alarm options             |                                       |                                       |


## Info
Latest Version:  **v2.1.0**
### v2.1.0

- **QoL fixed and changes**
  - Added splash-screen on startup (aa9b266)
  - Fixed outdated client compatibility (8696fef) #4
  - Added automatic update checks (4bf0c80)
  - News system for sending announcements to clients (2dc0fad)
  - Moved completely over to Ttk (f6b1018)
- **Reworked a lot of the timing functionality**
  - Added Stop-watch and count-up functionality (28bfa7f) #5 
  - Changed overflow handling (d5f7bc2)
  - Example configs have been updated accordingly (0328aa4)
  - Slightly improved update and config error handling (fbd23be)
  - GameMaster app will reflect minutes output when MM:SS is selected (9161449)
  - Opted to just remove clear-time warning for now (8a91fab)
- **Fixed some bugs (139b85c, f4ccc54, 9f32ce7)**
  - fixed text being written to files in ANSI instead of Unicode (28a8fd0)
  - fixed source code check (b06b6db)
  - fixed 60 minutes bug (dcd9a58) #6
  - fixed discord link issue (2711098)
  - fixed a bad try... except during config loading (c879277)
  - fixed leftover threads on exit (4b6c905)
- **Added a first-run only donation request**
  - Triggered by closing the app following the first run (9944049)
  - After the first run, this will be disabled by a config file. Removing the object or file will cause the popup to show one more time
- **uwu**
  - uwu (4161a6b)

Release notes:
#### v2.0.0
-   Release v2.0.0
-   GameMaster is now under GNU AGPLv3 License ([e10c07e](https://github.com/TheLittleDoc/GameMaster/commit/e10c07e19914f0a8b626d17f7c53307e2369c121))
    -   As per new license, copies of the source are available in the app ([7f81a14](https://github.com/TheLittleDoc/GameMaster/commit/7f81a144240ba9ac017e04c0393b326258e703a1))
-   Updated almost all of the interface ([#2](https://github.com/TheLittleDoc/GameMaster/pull/2))
    -   Now using Ttk for most widgets over tk ([072b571](https://github.com/TheLittleDoc/GameMaster/commit/072b571500edc1848a9c1c2cb4256bf416bb79b2),  [af53e09](https://github.com/TheLittleDoc/GameMaster/commit/af53e09248cf63f92425de0b635508477a64059b))
    -   For now, main tools layout is remaining the same
    -   Added visual header ([22da562](https://github.com/TheLittleDoc/GameMaster/commit/22da562d4e750803af5128f519299aa605e0d8ac))
    -   Added Notebook layout to separate some app functions ([cf31f90](https://github.com/TheLittleDoc/GameMaster/commit/cf31f90e54bebbea9d82ae30820c53cdbbbe819a))
    -   Styling is somewhat more consistent ([518dd54](https://github.com/TheLittleDoc/GameMaster/commit/518dd5496a602ffb7cfade36c2cba5d8c94f6808))
    -   Added button to open output directory ([42f1658](https://github.com/TheLittleDoc/GameMaster/commit/42f165828369f97da782b6cf4017f2a204a664d3))
-   Config loading
    -   Configuration files can now be swapped and exchanged using an in-app tool ([a003a30](https://github.com/TheLittleDoc/GameMaster/commit/a003a3013ce0b632e934c6ca02ff9a912134f806),  [cc514e2](https://github.com/TheLittleDoc/GameMaster/commit/cc514e268474263ff07a0b79b9d1b252762920d2))
    -   Preset config files are now available ([b9931e0](https://github.com/TheLittleDoc/GameMaster/commit/b9931e0ebd4fb4e89f623604fbbe956da17e4e97),  [70fc478](https://github.com/TheLittleDoc/GameMaster/commit/70fc47897038e594b075011100b4e2772f0c7bdb),  [cfeb396](https://github.com/TheLittleDoc/GameMaster/commit/cfeb3966cb97c78015172667a77826c561faa71a))
    -   On the first-run, a config setup tool will be launched to set up the config ([7463b32](https://github.com/TheLittleDoc/GameMaster/commit/7463b323413263b69871d517e41ba9ae77167665),  [ac1d060](https://github.com/TheLittleDoc/GameMaster/commit/ac1d06042c27ae9abfeece757c61bdf45838646c))
    -   Config files can be downloaded from the internet on first run ([59b5f94](https://github.com/TheLittleDoc/GameMaster/commit/59b5f94b8f50fadf47ecd377cb606f929d966a65))
    -   Otherwise, custom config files can be created ([7463b32](https://github.com/TheLittleDoc/GameMaster/commit/7463b323413263b69871d517e41ba9ae77167665),  [7214f80](https://github.com/TheLittleDoc/GameMaster/commit/7214f8090c5233cf2356472b73e5770d4e151d0f),  [4a7ba4e](https://github.com/TheLittleDoc/GameMaster/commit/4a7ba4ef97e576a80fa04aeba35350026d7f31e0),  [ac1d060](https://github.com/TheLittleDoc/GameMaster/commit/ac1d06042c27ae9abfeece757c61bdf45838646c))
-   Added persistent settings ([fda3094](https://github.com/TheLittleDoc/GameMaster/commit/fda30940f9e38cc9f6c3eda41c097c66953ac099))
    -   Supported in gmConfig v2
    -   v2 adds time output formatting and "on top" behavior
    -   This is just the beginning. I plan to use the settings section for way more in future version
-   Added "About" page ([07313ae](https://github.com/TheLittleDoc/GameMaster/commit/07313aedaa7b415c14b56f6ac5b1dd1d44d5a790))
    -   Shows socials and short description ([77c690d](https://github.com/TheLittleDoc/GameMaster/commit/77c690d62e64caeed1effcf238d2dfc6e884ecc3))
    -   Source is retrieved from GitHub and displayed in-app ([7f81a14](https://github.com/TheLittleDoc/GameMaster/commit/7f81a144240ba9ac017e04c0393b326258e703a1))
    -   License is included with installation and can be displayed in-app ([7f81a14](https://github.com/TheLittleDoc/GameMaster/commit/7f81a144240ba9ac017e04c0393b326258e703a1))
-   uwu
    -   uwu ([c64d317](https://github.com/TheLittleDoc/GameMaster/commit/c64d31734c46940fe1726945ee128c05ca2ecea8))
  
#### 1.0.2
	- Updated installer to not require admin (it shouldn't have in the first place) 
	- Included installer art  
  
#### 1.0.0  
	- Initial release  
	- Default Football configuration included. Documentation can be found at https://www.datastream.cf/projects/gamemaster/  
	- Note: Hangs or snags in the timer are due to OBS only checking the files for changes one time per second. GameMaster is outputting the correct timestamp at the right time, but OBS may not be displaying it in sync.  
	- Not working: "Clear time" button (disabled)  
	- Not Implemented: Player information feed, Config editor, First-run setup

## Documentation

*Please check back later. Config documentation is still in the works.*

---
Something not right? Found a bug? No problem, just leave a detailed report on the Issues page here, and I'll get to it as soon as possible.
Thanks for stickin' with this, and please enjoy **GameMaster**!  
  
*Cheers,*  
*TheLittleDoctor*
