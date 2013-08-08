Sublime Select Quoted
=====================

This is a small plugin for Sublime Text 2 and 3 which adds 'select within quoted' and 'select around quoted' functionality. This is roughly equivalent to Vim's `vi"` and `va"` commands.


Usage
-----

To select text within quotation marks, place your cursor within some quoted text, or partially select some quoted text. Then either select "Expand Selection to Quoted" under the "Edit" menu, or press `command+'` (Mac)/`control+'` (Linux/Windows) on your keyboard.

To select the text around the quote marks (that is, the quoted text and the quotes themselves,) use the keyboard shortcut `command+shift+'`/`control+shift+'`. Additionally, if the selection includes the starting or ending quote, or if the selection is surrounded by quotes on either side, the expanded selection will include the quotes automatically.


Install
-------

The easiest way to install this plugin is to use [package control](http://wbond.net/sublime_packages/package_control) (search for 'Select Quoted'.)

Alternatively, you can `git clone` this repo into your Sublime packages directory manually.


Additional Info
---------------

While we refer to "quotes" above, this plugin should work with any string deliminator. The only requirement is that the syntax file for the language tag the string with the scope string.quoted, and it is deliminated by characters tagged with the scope punctuation.definition.string.