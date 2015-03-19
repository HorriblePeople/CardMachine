(README is currently under construction)

This script assumes that the TSSSFCabin-Medium font is used, with special changes as described below:

TSSSFCabin-Medium is a specialized variant on Cabin that has the symbols for different pony-related icons replacing some unicode characters. The list below covers the unicode characters that have been replaced, as well as certain {keyword}s that will trigger the change to the unicode character in the script. (See the cards_example.pon file)
 * Male = {male} = \u2642
 * Female = {female} = \u2640
 * Combination male/female = {malefemale} = \u26A4
 * Ship = {ship} = \u2764
 * Earth Pony = {earthpony} = \uE000
 * Unicorn = {unicorn} = \uE001
 * Pegasus = {pegasus} = \uE002
 * Alicorn = {alicorn} = \uE003
 * Postapocalypse/Dystopian future/hourglass = {postapocalypse} = \uE004
 
The script also allows the following {keyword}s as a shortcut for adding common rules text to the cards, in the same manner as the symbols above:
 * {replace} = "While in your hand, you may discard a Pony card from the grid and play this card in its place. This power cannot be copied."
 * {swap} = "You may swap 2 Pony cards on the shipping grid."
 * {3swap} = "You may swap up to 3 Pony cards on the grid."
 * {draw} = "You may draw a card from the Ship or Pony deck."
 * {goal} = "You may discard a Goal and draw a new one to replace it."
 * {search} = "You may search the Ship or Pony discard pile for a card of your choice and play it."
 * {copy} = "You may copy the power of any Pony card currently on the shipping grid, except for Changelings."
 * {hermaphrodite} = "May count as either {male} or {female} for all Goals, Ships, and powers."
 * {double pony} = "This card counts as 2 Ponies."
 * {love poison} = "Instead of playing this ship with a Pony card from your hand, or connecting two ponies already on the grid, take a Pony card from the shipping grid and reattach it elsewhere with this Ship. That card's power activates."
 * {keyword change} = "When you attach this card to the grid, you may choose one Pony card attached to this Ship. Until the end of your turn, that Pony card counts as having any one keyword of your choice, except pony names."
 * {gender change} = "When you attach this card to the grid, you may choose one Pony card attached to this Ship. Until the end of your turn, that Pony card becomes the opposite gender."
 * {race change} = "When you attach this card to the grid, you may choose one Pony card attached to this Ship. Until the end of your turn, that Pony card becomes a race of your choice. This cannot affect Changelings."
 * {timeline change} = "When you attach this card to the grid, you may choose one Pony card attached to this Ship. Until the end of your turn, that Pony card counts as {postapocalypse}."
 * {play from discard} = "You may choose to play the top card on the Pony discard pile with this Ship, rather than use a Pony card from your hand."