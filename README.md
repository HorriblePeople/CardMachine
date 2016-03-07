# CardMachine
*by Horrible People Productions*
## version: OH GOD EVERYTHING IS TERRIBLE

# !!WARNING!!
This script is **NOT** user-friendly by any stretch of the imagination! This is a slapped-together conglomeration of last-minute decisions and hasty shortcuts we've taken while maintaining our ability to make decks of cards. Unless you are a Python expert, we do NOT recommend using this tool for casually creating cards. There are much better options out there.

# INSTALLATION
This tool relies on files being set up in a proper hierarchy:

Base Folder > Card Set > card set files

The Base Folder represents a particular game. e.g. TSSSF, BaBOC, Dominion, Fluxx, Poker
The Card Set is a variant of the base game, possibly an expansion, or just a collection of different versions. e.g. Core 1.0.3, Ponyville University 1.5.6.
The base folder and card set can be named anything.

Within the base folder is where you should put your "Card Art" and "resources" directories, or any other directories that contain necessary assets.

To get started, create the Base Folder in the CardMachine directory. In the Base Folder, make the Card Set directory. And in the Card Set directory, put your cards.pon file. (You can see an example cards.pon file in this repository)

# GETTING STARTED:
Once your files are in place, you can either:

1) Edit `GameGen.py` so that it calls `main()` with the proper arguments (see the `main()` docstring for more info)
2) Call the proper arguments using the command line. E.g. `python GameGen.py -b TSSSF -f "Core 1.0.3/cards.pon"`

The script will open the filepath to cards.pon (or whatever you name it), and will call the CardGen code once for each card. It will attempt to bundle the cards created into 3x3 card images and, at the very end, compile all the images into PDFs of both the fronts and backs.





This script assumes that the TSSSFCabin-Medium font is used, with special changes as described below:

TSSSFCabin-Medium is a specialized variant on Cabin that has the symbols for different pony-related icons replacing some unicode characters. The list below covers the unicode characters that have been replaced, as well as certain {keyword}s that will trigger the change to the unicode character in the script. (See the cards_example.pon file)
* Male = `{male}` = \u2642
* Female = `{female}` = \u2640
* Combination male/female = `{malefemale}` = \u26A4
* Ship = `{ship}` = \u2764
* Earth Pony = `{earthpony}` = \uE000
* Unicorn = `{unicorn}` = \uE001
* Pegasus = `{pegasus}` = \uE002
* Alicorn = `{alicorn}` = \uE003
* Postapocalypse/Dystopian future/hourglass = `{postapocalypse}` = \uE004

The script also allows the following {keyword}s as a shortcut for adding common rules text to the cards, in the same manner as the symbols above:
* `{replace}` = "While this card is in your hand, you may discard a Pony card from the grid and play this card in its place. This power cannot be copied."
* `{swap}` = "You may swap 2 Pony cards on the shipping grid."
* `{3swap}` = "You may swap up to 3 Pony cards on the grid."
* `{draw}` = "You may draw 1 card from the Ship or Pony deck."
* `{goal}` = "You may discard 1 active Goal and draw 1 new Goal to replace it."
* `{search}` = "You may search the Ship or Pony discard pile for 1 card of your choice and put it into your hand. If it's still in your hand at the end of your turn, discard it."
* `{copy}` = "You may copy the power of any Pony card currently on the shipping grid, except for Ponies with the Changeling keyword."
* `{hermaphrodite}` = "May count as either `{male}` or `{female}` for all Goals, Ships, and powers."
* `{double pony}` = "This card counts as 2 Ponies."
* `{love poison}` = "Instead of playing this Ship with a Pony card from your hand, or connecting two Pony cards already on the grid, you may take a Pony card from the shipping grid and reattach it elsewhere with this Ship. That card's power activates."
* `{keyword change}` = "When you attach this card to the grid, you may choose one Pony card attached to this Ship. Until the end of your turn, that Pony card gains one keyword of your choice, except for Pony names."
* `{gender change}` = "When you attach this card to the grid, you may choose one Pony card attached to this Ship. Until the end of your turn, that Pony card becomes the opposite gender."
* `{race change}` = "When you attach this card to the grid, you may choose one Pony card attached to this Ship. Until the end of your turn, that Pony card becomes the race of your choice. This cannot affect Ponies with the Changeling keyword."
* `{timeline change}` = "When you attach this card to the grid, you may choose one Pony card attached to this Ship. Until the end of your turn, that Pony card's timeline becomes `{postapocalypse}`."
* `{play from discard}` = "You may choose to play the top card of the Pony discard pile with this Ship, rather than play a Pony card from your hand."
* `{clone}`: "When you attach this card to the grid, you may choose one Pony card attached to this Ship. Until the end of your turn, that Pony card counts as 2 Ponies."
