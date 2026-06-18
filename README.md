# DEBT TO INCOME GUI

## Update: 6/4/26

I have decided to change from a CLI interface to a GUI interface to make it more user friendly. Since seeing a terminal is scary to people having a GUI should allow it to be more accessible and in turn give me feedback.

I plan to add a menu later on seeing how it would be odd to have the user thrown straight into the input section. I did add the save and load parts of the files in case the user wants to save it to adjust later... or wants an unfriendly reminder of their situation.

I could add priority flags into the program so that some things could flagged differently. For example, my rent would 100% have a stronger priority over a weekly starbucks since I wouldnt want to be homeless but I could sacrifice a drink in comparison.

# Update: 6/7/26

The GUI is now functional, it works but it's very basic. I created a seperate branch in order to categorize the debts differently. This would mean that I would also need the user to name the debt as well, however, if i did that then the pie chart would probably look messy potentially having hundreds of slices. This would mean that I should implement categories to create less visual clutter. If I did that, then maybe i could implement a seperate pie chart to show the contents in that slice alone.
## Update: 6/7/26 (GUI branch)

I think the GUI looks really dated, I plan to modernize it so that it doesnt look like an old sketchy program. I believe a GUI update would help this program look more presentable in a way that users can trust. Perhaps I could add some colors to give it a "brand" look and also make the buttons and listbox look more modern as well.

## Update: 6/12/26 (GUI branch)

I removed the spaces between the '=' of the code inside of parameters. Theres no practical use for it, but it makes the code look more intentional. Updated the GUI to look more modern, it now has color implemented and the buttons are color coded to visually show what they may do. In order to do this I had to rewrite some of the code to support ttk instead of tk. My next plan is to have the cursor change if over a button or dropdown menu (options included). I accidentally made the program fullscreen instead of windowed fullscreen and it dawned on me that I never implemented a way to exit the program. Thankfully I Alt+f4'd out but most users dont know that, perhaps I could add an exit button or more likely I will add a menu bar on the top of the screen seen in most applications. I added two versions of windowed fullscreen in order to achieve higher compatability.

## Update: 6/15/26 (GUI branch)

Theres a QoL issue in the dropdown menu which is shown when the menu is extended, tapping the menu again does not get rid of the extended menu. Merged the GUI branch with the feature branch.

## Update: 6/16/26 (Post Merge)

Today I wanted to see what would happen if the user had the debt exceed the income and what happened was that the pie chart just turned all red (which is what I expected). What I would want to implement instead is having a secondary "pie" appear on top of the pie chart but only as big as the percentage as the first pie chart similar to the stamina system in TLOZ: BOTW.

## Update: 6/17/26
This may unfortunately be the last update for a while because of school 💔🥀, so here's some reminders of what to add later on:
* Add the ability to scroll on the menus, for example, some buttons or activities may be inaccessible if the window is minimized, or have it be scalable to the window.
* For the money investments, make the money a green color since its a positive debt, it should visually reflect so.
* For the secondary pie chart (Whenever it is implemented (prefereably on click)) we can group serparate baby slices with the same priority colors that theyre flagged with. 
* We can also add sortments so that when toggled the priorities flip to the users choice.
* Some people also have more that one income, we would have to implement the ability for people to add multiple incomes, but should we segregate their looks? so far im thinking....probably not...
* Fix the dropdown menus
* Add the ability to edit previous entries, for example, credit card mimimums are variable to the spending, with the ability to edit, if its deep in there they wont need to delete a ton of entries just to edit one thing
* Add little ? buttons so if a person is confused they can click it and a small window will appear to give a brief description.