Synesthesia
===========

A plugin for Sublime Text 2 for highlighting text with pretty colours.

Installation
------------

- The easiest way is through Package Control (`Shift+Ctrl+P` > Install Package > Synesthesia).
- Alternatively, clone this repository into `Packages/Synesthesia`.

Getting Started
---------------

- Open the Command Palette (`Shift+Ctrl+P`) and select **New Highlighting Scheme**. A JSON file containing a list of keywords and associated colours will be created for you.
- Save the file as `Hello World.json`.
- Select **Compile Highlighting Scheme** from the Command Palette.
- Click on the bottom-right corner of the window to change the syntax for the current view; `Hello World` will appear in the list. Click on it to select it. (You can also choose `Set Syntax: Hello World` from the Command Palette).
- Voila!
- If you want to make changes to the keywords and/or colours, simply compile again and Sublime Text will automatically reload it.

Functionality
-------------

Most of the plugin's functionality is based on 'highlighting schemes' - JSON files with a list of keywords and the colours to highlight them with. The first step is to create such a file. Select **Sample Highlighting Scheme** from the Command Palette for an example that uses most of the plugin's features. You may also wish to browse the examples in `Synesthesia/include`.

Once you're satisfied with your scheme, compile it. Synthesia will generate the configuration files necessary for Sublime Text to highlight everything.

### Colours

Keyword colours are specified as RGB in hexadecimal form (`#rrggbb`). You can also use colour names, like `blue` or `red`; a list of these can be found (and were taken from) [here](http://en.wikipedia.org/wiki/Web_colours#X11_color_names).

	'keywords': {
		'hello': '#0CBDE8',
		'world': 'dodgerblue'
	}

### Formatting and Options

A map of options can be specified instead of a colour name or value:

	'a keyword': {
		'colour': 'plum',
		'background': 'blue',
		'bold': true,
		'italics': true,
		'whole-word': true,
		'case-insensitive': true
	}

- `colour` is optional
- `background` controls the background colour of highlighted keywords. It's used the same way `colour` is.
- `whole-word` will make sure only whole occurrences of keywords are matched. If set to true, the 'fun' in 'funeral' won't be coloured.

### Keywords

Keywords are specified using [Oniguruma regular expressions](http://manual.macromates.com/en/regular_expressions). Don't worry if you aren't familiar with regexes: all alphanumeric strings are valid regexes, so you don't strictly *need* them to use this plugin.

### Mixins

It can be cumbersome to manage a huge list of regexes and hexadecimal colours. Highlighting schemes can be mixed into others with the `include` option, so you can easily separate and combine them:

	{
		'include': ['LightMarkdown'],
		'keywords': {...}
	}

This will cause the keywords and colours in `LightMarkdown.json` to be copied into the current scheme.

- The folder that the current scheme is in will first be checked for the mixins specified.
- If a mixin can't be found there, `Packages/Synesthesia/include` will be checked next.
- Dependencies will be resolved recursively. Circular depedenceies are guarded against.
- Dependencies are loaded depth-first, in the order they are specified. If a keyword has appeared before, it won't be overridden should it appear again in a later-loaded dependency.

### Extensions

You can specify new extensions for your highlighting schemes under the `extensions` key.

	{
		'extensions': ['txt', 'etc'],
		'keywords': {...}
	}

`txt` will be used by default if you don't specify anything.

### Autocompletion

	{
		'autocompletion': true,
		'keywords': {...}
	}

If set to true, Sublime Text's autocompletion will be enabled for your highlighting scheme.

### Deleting Schemes

To remove schemes, select **Delete Highlighting Scheme** from the Command Palette, then enter the name of the unwanted scheme.

***Don't delete them manually***. Sublime Text will *complain* about that, and you might have to reinstall the package to fix the resulting errors.

What should you use this plugin for?
------------------------------------

- **Ad-hoc highlighting of text.** I personally appreciate the visual cues provided by syntax highlighting of code very much and wanted to bring the concept to text-editing in general. This plugin is a lightweight and unobtrusive way to draw attention to important articles in your text, such as key terms, characters, or locations. I hope this makes writing (or text-editing in general) more fun for you!
- **Highlighting simple markup languages.** You can see an example of this in `LightMarkdown.json`. It's not perfect, but it shows how you can easily define a colour theme for a [regular language](http://en.wikipedia.org/wiki/Chomsky_hierarchy).
- *This plugin is not an easier way to specify syntax highlighting for a programming language.* That's the niche [AAAPackageDev](https://github.com/SublimeText/AAAPackageDev) fills.

Inner Workings
--------------

Compiling a highlighting scheme generates three files:

- A syntax definition
- A colour theme
- A settings file

The first two work in tandem, specifying a mini-language consisting of the user's keywords, along with a colour theme designed specifically for that mini-language. The settings file glues them together, causing Sublime Text to associate the theme with the mini-language. All this is done via Sublime Text's built-in mechanisms for syntax highlighting, so it's robust and fairly stable.

Other plugins for highlighting arbitrary words do so either via named regions or by mutating the current colour theme: the first method doesn't interact well with live editing and is limited to only changing background colour, while the second provides a high level of flexibility but involves messing with colour theme files. The method used here, while slightly more static, is equally robust for live editing and much simpler to manage. It's the middle ground between all these approaches.

License
--------

[MIT](http://opensource.org/licenses/MIT)
