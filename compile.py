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

def remove_ext(filename):
	return filename.split(".")[0]

def get_file_name_with_ext(filepath):
	temp = filepath.split("\\")
	return temp[len(temp)-1]

def concat_string_list(lst):
	return ''.join(lst)

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

class SynesthesiaCompileCommand(sublime_plugin.WindowCommand):
    def run(self, cmd = []):
    	# prepare input file paths
		path = cmd[0] if len(cmd) > 0 else self.window.active_view().file_name()
		filepath = os.path.abspath(path)
		filename = get_file_name_with_ext(filepath)
		themename = remove_ext(filename)

		# load input file
		try:
			entries = json.loads(read_file(filepath))
		except ValueError:
			sublime.status_message("%s is not a vaild JSON file." % filename)
			return

		hs = HighlightingScheme(entries)

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

	default_colours = templates.default_colours_template

	def __init__(self, data):
		self.data = data

	def save(self, themename):
		# initialization
		patterns = []
		theme_scopes = []
		pattern_map = self.data["patterns"]
		count = 0

		# generate syntax and theme files
		for key in pattern_map.keys():
			regex = key
			colour = pattern_map[key].lower()
			if colour in colours.name_to_hex:
				colour = colours.name_to_hex[colour]
			keyname = strip_non_alpha(regex)
			if keyname == regex:
				# regex is completely alphabetical;
				# automatically enforce word boundary
				regex = "\\b%s\\b" % regex

			keyname = "%s%d" % (keyname, count)
			count = count + 1
			patterns.append(templates.pattern % (regex, keyname))
			theme_scopes.append(templates.theme_element % (keyname, keyname, colour))

		patterns = concat_string_list(patterns)
		theme_scopes = concat_string_list(theme_scopes)

		# produce output files
		package_directory = sublime.packages_path() + "\\Synesthesia\\"
		scope_filename = package_directory + themename + ".tmLanguage"
		theme_filename = package_directory + themename + ".tmTheme"
		settings_filename = package_directory + themename + ".sublime-settings"
		write_file(scope_filename, templates.scope_template % (themename, patterns, themename, uuid.uuid4()))
		print "Written to %s." % scope_filename
		write_file(theme_filename, templates.theme_template % (themename, self.default_colours, theme_scopes, uuid.uuid4()))
		print "Written to %s." % theme_filename
		write_file(settings_filename, templates.default_settings_template % themename)
		print "Written to %s." % settings_filename
		sublime.status_message("%s syntax files generated." % themename)
