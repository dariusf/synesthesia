Synesthesia
===========

A Sublime Text 3 plugin for highlighting text with pretty colours.

Installation
------------

- The easiest way is through Package Control (`Shift+Ctrl+P` > Install Package > Synesthesia).
- Alternatively, clone this repository into `Packages/synesthesia`.

Getting Started
---------------

- Open the Command Palette (`Shift+Ctrl+P`) and select **New Highlighting Scheme**.
- Save the file as `Hello World.json`.
- Select **Compile Highlighting Scheme** from the Command Palette.
- Select `Set Syntax: Hello World` from the Command Palette. Voila!
- To change keywords or colours, simply compile again.

Functionality
-------------

This plugin provides a quick and lightweight way to highlight text with different colours.

It takes a *highlighting scheme*, which is a description of words to highlight and how they should look, and generates all the necessary configuration files for Sublime to render them that way.

This is essentially an abstraction for creating a language definition, but much easier to use: you don't have to deal with all that complexity if all you need is to bring attention to a few terms in your text, colour a log file, etc.

The rest of this readme thoroughly documents all the options you can use. You may also wish to browse the examples in `Packages/synesthesia/include`.

What should you use this plugin for?
------------------------------------

- **Ad-hoc highlighting of text.** This plugin is a quick and lightweight way to draw attention to important articles in your text. A few example uses:
	+ Highlighting keywords in log files
	+ Drawing attention to characters or locations in writing
	+ Visualising colours (check out `Pretty.json`)
	+ Lightweight markup (check out [MarkdownEditing](https://github.com/SublimeText-Markdown/MarkdownEditing) for Markdown)
	+ Quick-and-dirty way to add keywords to existing language definitions
- *This plugin is not an easier way to specify syntax highlighting for a programming language.* A list of regular expressions isn't a great way to handle most programming languages. Making syntax highlighting easier is the niche [AAAPackageDev](https://github.com/SublimeText/AAAPackageDev) fills.

### Colours

Keyword colours are specified as RGB in hexadecimal form (`#rrggbb`). We can also use colour names, like `blue` or `red`; a list of these can be found [here](http://en.wikipedia.org/wiki/Web_colours#X11_color_names).

Two additional colour types are available: `random` and `auto`. `random` will give a random colour on every compile, while the colour that `auto` generates is fixed. Both will only generate nice bright colours.

```js
{
	'keywords': {
		'roses': '#ff0000',
		'violets': 'blue',
		'lazy?': 'random',
		'no problem!': 'auto'
	}
}
```

### Formatting and Options

Options can be specified instead of a colour name or value:

```js
{
	'keywords': {
		'something': {
			'colour': 'plum',
			'background': 'blue',
			'bold': true,
			'italics': true,
			'whole-word': true,
			'case-insensitive': true
		}
	}
}
```

- All fields are optional, including `colour`.
- `background` controls the background colour of highlighted keywords. It's used the same way `colour` is.
- `whole-word` will make sure only whole occurrences of keywords are matched. If set to true, the 'java' in 'javascript' won't be coloured.

### Keywords

Keywords are specified using [Oniguruma regular expressions](http://manual.macromates.com/en/regular_expressions), which is what Sublime uses under the hood. Don't worry if you aren't familiar with these: alphanumeric strings are valid regexes, so you don't need to be an expert to use this plugin.

### Mixins

We may find ourselves always wanting to highlight the same things. For example, we want `ERROR` to appear red, in bold font, whether in upper case or lower. It can be tiresome to define it again and again.

That's where this option comes in. Highlighting schemes can be *mixed into others* with `include`, so we can easily separate and combine them:

```js
{
	'include': ['LightMarkdown'],
	'keywords': {
		...
	}
}
```

This will cause the keywords and colours in `LightMarkdown.json` to be copied into the current scheme on compile.

Here's how Synesthesia will search for schemes to mix in:

- The directory that the current scheme is in will first be checked for the mixins specified.
- If a mixin can't be found there, `Packages/synesthesia/include` will be checked next.
- Dependencies will be resolved recursively, depth-first, in the order they are specified. Circular dependencies are prevented.
- If a keyword has appeared before, it won't be overridden should it appear again in a later-loaded dependency.

### File Extensions

File extensions for highlighting schemes go under `extensions`. This is so they apply automatically when files of the type are opened.

```js
{
	'extensions': ['txt', 'md'],
	'keywords': {...}
}
```

By default, `txt` and `md` will be used.

### Autocompletion

```js
{
	'autocompletion': true,
	'keywords': {...}
}
```

If set to true, Sublime's autocompletion will be enabled in the generated language definition.

### Other Settings

```js
{
	'keywords': {
		...
	},
	'settings': {
		'font_face': 'Open Sans'
	}
}
```

Other settings for the generated language definition go here.

### Removing Highlighting Schemes

To remove highlighting schemes, select **Remove Highlighting Scheme** from the Command Palette.

**Don't delete the files manually**. Sublime Text will complain about that, and you might have to reinstall the package to fix the resulting errors.

Inner Workings
--------------

Compiling a highlighting scheme generates three files:

- Language definition (`.tmLanguage`)
- Colour theme (`.tmTheme`)
- Settings (`.sublime-settings`)

The first two work in tandem, specifying a mini-language consisting of the user's keywords, along with a colour theme designed specifically for that mini-language. The settings file glues them together, causing Sublime Text to associate the theme with the mini-language. All this is done via Sublime Text's built-in mechanisms for syntax highlighting, so it's robust and stable.

Other plugins for highlighting arbitrary words do so either via named regions or by mutating the current colour theme.

- The first method doesn't interact well with live editing and is limited to only changing the background colour of text.
- The second provides a slightly higher level of flexibility (for example, there may be no need to switch to a different language) but is much more complex implementation-wise. It also may not play nice with all language definitions and colour schemes.

The method used in this plugin, while static, is great for live editing and is much simpler to manage. Interactions with other language definitions are also made explicit. I see it as the middle ground between these approaches.

License
--------

[MIT](http://opensource.org/licenses/MIT)
