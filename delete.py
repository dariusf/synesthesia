import sublime, sublime_plugin
import os

PATH_SEPARATOR = "\\" if sublime.platform() == "windows" else "/"

def extract_syntax_name(path):
	temp = path.split("/")
	return temp[len(temp)-1].split(".")[0]

class SynesthesiaDeleteCommand(sublime_plugin.WindowCommand):
	def run(self):
		self.window.show_input_panel("Highlighting scheme to delete:", "", self.done, None, None)

	def done(self, which):

		# check if open views are using the syntax file that i'm going to delete
		for v in self.window.views():
			current_def = extract_syntax_name(v.settings().get('syntax'))
			if (current_def.lower() == which):
				v.set_syntax_file("%s/Text/Plain text.tmLanguage" % sublime.packages_path())

		# delete the files
		package_directory = sublime.packages_path() + PATH_SEPARATOR + "Synesthesia" + PATH_SEPARATOR
		files = ["%s.sublime-settings", "%s.tmLanguage", "%s.tmLanguage.cache", "%s.tmTheme", "%s.tmTheme.cache"]
		files_deleted = False

		for filepath in files:
			filepath = package_directory + (filepath % which)
			if os.path.exists(filepath):
				os.remove(filepath)
				files_deleted = True
			else:
				print "File not found; can't be deleted: %s" % filepath

		if files_deleted:
			sublime.status_message("Highlighting scheme %s removed." % which)
		else:
			sublime.status_message("Highlighting scheme %s not found." % which)
