import sublime, sublime_plugin
import os, re
from . import compile

def extract_syntax_name(path):
	return os.path.split(path)[1].split(".")[0]

class SynesthesiaDeleteCommand(sublime_plugin.WindowCommand):
	def run(self):
		window = self.window

		filetypes = ["%s.sublime-settings", "%s.tmLanguage", "%s.tmLanguage.cache", "%s.tmTheme", "%s.tmTheme.cache"]

		# Find .tmLanguage files
		files = [f for f in os.listdir(compile.SYNESTHESIA_OUTPUT_PATH) if os.path.isfile(os.path.join(compile.SYNESTHESIA_OUTPUT_PATH, f))]
		files = sorted([f for f in files if f.endswith('.tmLanguage')])
		without_extensions = [re.sub('.tmLanguage', '', f) for f in files]

		def done(which):
			# Do nothing in the event of quick panel cancellation
			if not (which == -1):
				nonlocal without_extensions, filetypes
				which = without_extensions[which]

				# Check if open views are using the syntax file that is going to be deleted.
				# If so, unset them.
				for v in self.window.views():
					current_def = extract_syntax_name(v.settings().get('syntax'))
					if (current_def == which):
						v.set_syntax_file("Packages/Text/Plain text.tmLanguage")

				# Delete files

				some_files_deleted = False
				for filepath in filetypes:
					filepath = os.path.join(compile.SYNESTHESIA_OUTPUT_PATH, filepath % which)
					if os.path.exists(filepath):
						os.remove(filepath)
						some_files_deleted = True
					else:
						print("File not found; can't be deleted: %s" % filepath)

				if some_files_deleted:
					sublime.status_message("Highlighting scheme %s removed." % which)
				else:
					sublime.status_message("Highlighting scheme %s not found." % which)

		if not without_extensions:
			sublime.status_message("No highlighting schemes to remove.")
		else:
			window.show_quick_panel(without_extensions, done)