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
	return re.sub("[^\\w]+", "", string)

def get_file_name(filepath):
	temp = filepath.split("\\")
	return temp[len(temp)-1].split(".")[0]

def concat_string_list(lst):
	return ''.join(lst)

class CompileCommand(sublime_plugin.WindowCommand):
    def run(self, cmd = []):
		filepath = os.path.abspath(cmd[0])
		filename = get_file_name(filepath)
		entries = json.loads(read_file(filepath))
		patterns = []
		theme_scopes = []
		pattern_map = entries["patterns"]

		for key in pattern_map.keys():
			keyword = key
			colour = pattern_map[key].lower()
			if colour in colours.name_to_hex:
				colour = colours.name_to_hex[colour]
			keyname = strip_non_alpha(keyword)
			patterns.append(templates.pattern % (keyword, keyname))
			theme_scopes.append(templates.theme_element % (keyname, keyname, colour))

		patterns = concat_string_list(patterns)
		theme_scopes = concat_string_list(theme_scopes)
		colour_scheme_path = re.sub("Packages", sublime.packages_path(), self.window.active_view().settings().get('color_scheme'))
		default_colours = templates.default_colours_template

		if (os.path.exists(colour_scheme_path)):
			settings_block = re.compile(r"[ \t]+<dict>\s+<key>settings</key>[\s\w></#]+</dict>")
			settings_text = read_file(colour_scheme_path)
			match = settings_block.search(settings_text)
			if match:
				default_colours = match.group(0)

		package_directory = sublime.packages_path() + "\\Synesthesia\\"
		scope_filename = package_directory + filename + ".tmLanguage"
		theme_filename = package_directory + filename + ".tmTheme"
		settings_filename = package_directory + filename + ".sublime-settings"
		write_file(scope_filename, templates.scope_template % (filename, patterns, filename, uuid.uuid4()))
		print "Written to %s." % scope_filename
		write_file(theme_filename, templates.theme_template % (filename, default_colours, theme_scopes, uuid.uuid4()))
		print "Written to %s." % theme_filename
		write_file(settings_filename, templates.default_settings_template % filename)
		print "Written to %s." % settings_filename
		print "You may have to reload Sublime Text to see your changes take effect."
		sublime.status_message("%s syntax files generated." % filename)