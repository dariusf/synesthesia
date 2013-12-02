import re, uuid, os, json
import sublime, sublime_plugin
import templates
import colours

PATH_SEPARATOR = "\\" if sublime.platform() == "windows" else "/"

def write_file(filepath, s):
	f = open(filepath, 'w')
	f.write(s)
	f.close()

def read_file(filepath):
	f = open(filepath, 'r')
	result = f.read()
	f.close()
	return result

def strip_non_alpha(string):
	return re.sub("[^A-Za-z]+", "", string)

def split_filepath(abspath):
	segments = abspath.split(PATH_SEPARATOR)
	filename = segments[-1:][0]
	extparts = filename.split(".")
	return PATH_SEPARATOR.join(segments[:-1]), extparts[0], '.'.join(extparts[1:])

def read_default_settings(view):
	colour_scheme_path = re.sub("Packages", sublime.packages_path(), view.settings().get('color_scheme'))

	if (os.path.exists(colour_scheme_path)):
		settings_block = re.compile(r"[ \t]+<dict>\s+<key>settings</key>[\s\w></#]+</dict>")
		settings_text = read_file(colour_scheme_path)
		match = settings_block.search(settings_text)
		if match:
			default_colours = match.group(0)
			return default_colours

	return None

def load_json_data(filepath):
	_, themename, ext = split_filepath(filepath)

	entries = None
	try:
		entries = json.loads(read_file(filepath))
	except ValueError:
		sublime.status_message("%s is not a valid JSON file." % themename + ext)

	return themename, entries

class SynesthesiaCompileCommand(sublime_plugin.WindowCommand):
    def run(self, cmd = []):

		path = cmd[0] if len(cmd) > 0 else self.window.active_view().file_name()
		filepath = os.path.abspath(path)
		themename, entries = load_json_data(filepath)
		directory, _, _ = split_filepath(filepath)

		if not entries:
			return

		hs = HighlightingScheme(directory, entries)

		default_colours = read_default_settings(self.window.active_view())
		if default_colours:
			hs.default_colours = default_colours

		hs.save(themename)

class HighlightingScheme():
	"""
	A highlighting scheme consists of:

	- a syntax definition
	- a colour theme
	- a settings file

	"""

	default_colours = templates.default_colours

	def __init__(self, directory, data):
		self.directory = directory
		self.data = data

	def save(self, themename):
		# initialization
		autocompletion = "autocompletion" in self.data and self.data["autocompletion"]
		keywords = []
		theme_scopes = []
		keyword_map = self.data["keywords"]
		count = 0

		# resolve dependencies (depth-first)
		if "include" in self.data:
			inclusions = self.data["include"]
			already_included = [themename]
			while len(inclusions) > 0:
				i = inclusions.pop()
				# prevents recursive dependency, since it only looks in the same directory
				if i not in already_included:
					already_included.append(i)
					_, entries = load_json_data(os.path.join(self.directory, i + '.json'))
					if "include" in entries:
						inclusions.extend(entries["include"])
					if "keywords" in entries:
						new_keywords = entries["keywords"]
						for key in new_keywords.keys():
							# won't add colling names
							if key not in keyword_map:
								keyword_map[key] = new_keywords[key]

		def colour(c):
			c = c.lower()
			if c in colours.name_to_hex:
				c = colours.name_to_hex[c]
			return c

		# generate syntax and theme files
		for key in keyword_map.keys():
			regex = key
			value = keyword_map[key]

			options = []
			case_insensitive = False
			whole_word = False

			if type(value) == str or type(value) == unicode:
				options.append(templates.theme_element_foreground % colour(value))
			elif type(value) == dict:
				fontstyle = []
				if "colour" in value:
					options.append(templates.theme_element_foreground % colour(value["colour"]))
				if "background" in value:
					options.append(templates.theme_element_background % colour(value["background"]))
				if "italics" in value and value["italics"]:
					fontstyle.append("italic")
				if "bold" in value and value["bold"]:
					fontstyle.append("bold")
				if "whole-word" in value and value["whole-word"]:
					whole_word = True
				if "case-insensitive" in value and value["case-insensitive"]:
					case_insensitive = True

				if len(fontstyle) > 0:
					options.append(templates.theme_element_fontstyle % ' '.join(fontstyle))

			keyname = strip_non_alpha(regex)

			if keyname == regex or whole_word:
				# regex is completely alphabetical;
				# automatically enforce word boundary
				regex = "\\b%s\\b" % regex
			if case_insensitive:
				regex = "(?i:%s)" % regex
			keyname = "%s_%d" % (keyname, count)
			count = count + 1

			keywords.append(templates.keyword % (regex, keyname))
			theme_scopes.append(templates.theme_element % (keyname, keyname, ''.join(options)))

		keywords = ''.join(keywords)
		theme_scopes = ''.join(theme_scopes)

		# produce output files
		package_directory = os.path.join(sublime.packages_path(), "Synesthesia")
		scope_filename = os.path.join(package_directory, themename + ".tmLanguage")
		theme_filename = os.path.join(package_directory, themename + ".tmTheme")
		settings_filename = os.path.join(package_directory, themename + ".sublime-settings")
		write_file(scope_filename, templates.scope % (themename, keywords, "source" if autocompletion else "text", themename, uuid.uuid4()))
		print "Written to %s." % scope_filename
		write_file(theme_filename, templates.theme % (themename, self.default_colours, theme_scopes, uuid.uuid4()))
		print "Written to %s." % theme_filename
		write_file(settings_filename, templates.default_settings % themename)
		print "Written to %s." % settings_filename
		sublime.status_message("Highlighting scheme %s generated." % themename)
