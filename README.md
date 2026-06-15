# DEBT TO INCOME GUI

## Update: 6/4/26

I have decided to change from a CLI interface to a GUI interface to make it more user friendly. Since seeing a terminal is scary to people having a GUI should allow it to be more accessible and in turn give me feedback.

I plan to add a menu later on seeing how it would be odd to have the user thrown straight into the input section. I did add the save and load parts of the files in case the user wants to save it to adjust later... or wants an unfriendly reminder of their situation.

I could add priority flags into the program so that some things could flagged differently. For example, my rent would 100% have a stronger priority over a weekly starbucks since I wouldnt want to be homeless but I could sacrifice a drink in comparison.

## Update: 6/7/26

I think the GUI looks really dated, I plan to modernize it so that it doesnt look like an old sketchy program. I believe a GUI update would help this program look more presentable in a way that users can trust. Perhaps I could add some colors to give it a "brand" look and also make the buttons and listbox look more modern as well.

## Update: 6/12/26

I removed the spaces between the '=' of the code inside of parameters. Theres no practical use for it, but it makes the code look more intentional. Updated the GUI to look more modern, it now has color implemented and the buttons are color coded to visually show what they may do. In order to do this I had to rewrite some of the code to support ttk instead of tk. My next plan is to have the cursor change if over a button or dropdown menu (options included). I accidentally made the program fullscreen instead of windowed fullscreen and it dawned on me that I never implemented a way to exit the program. Thankfully I Alt+f4'd out but most users dont know that, perhaps I could add an exit button or more likely I will add a menu bar on the top of the screen seen in most applications. I added two versions of windowed fullscreen in order to achieve higher compatability.

## Update: 6/15/26

Theres a QoL issue in the dropdown menu which is shown when the menu is extended, tapping the menu again does not get rid of the extended menu.