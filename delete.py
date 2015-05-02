import sublime, sublime_plugin
import os, re

def extract_syntax_name(path):
	return os.path.split(path)[1].split(".")[0]

class SynesthesiaDeleteCommand(sublime_plugin.WindowCommand):
	def run(self):
		window = self.window

		# Find .tmLanguage files
		directory = os.path.join(sublime.packages_path(), "synesthesia")
		files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
		files = sorted([f for f in files if f.endswith('.tmLanguage')])
		without_extensions = [re.sub('.tmLanguage', '', f) for f in files]

		def done(which):
			if not (which == -1):
				nonlocal without_extensions
				which = without_extensions[which]

				# Check if open views are using the syntax file that is going to be deleted
				for v in self.window.views():
					current_def = extract_syntax_name(v.settings().get('syntax'))
					if (current_def == which):
						v.set_syntax_file("Packages/Text/Plain text.tmLanguage")

				# Delete the files
				package_directory = os.path.join(sublime.packages_path(), "synesthesia")
				files = ["%s.sublime-settings", "%s.tmLanguage", "%s.tmLanguage.cache", "%s.tmTheme", "%s.tmTheme.cache"]
				files_deleted = False

				for filepath in files:
					filepath = os.path.join(package_directory, filepath % which)
					if os.path.exists(filepath):
						os.remove(filepath)
						files_deleted = True
					else:
						print("File not found; can't be deleted: %s" % filepath)

				if files_deleted:
					sublime.status_message("Highlighting scheme %s removed." % which)
				else:
					sublime.status_message("Highlighting scheme %s not found." % which)

		if not without_extensions:
			sublime.status_message("No highlighting schemes to remove.")
		else:
			window.show_quick_panel(without_extensions, done)