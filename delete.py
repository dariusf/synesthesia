import sublime, sublime_plugin
import os, re
from . import compile

def extract_syntax_name(path):
	return os.path.split(path)[1].split(".")[0]

def essential_filetypes_present(path, filetypes, scheme_name):
	for filetype in filetypes:
		ft_path = os.path.join(path, filetype % scheme_name)
		if not (os.path.exists(ft_path) and os.path.isfile(ft_path)):
			return False
	return True

class SynesthesiaDeleteCommand(sublime_plugin.WindowCommand):
	def run(self):
		window = self.window

		essential_filetypes = ["%s.sublime-settings", "%s.tmLanguage", "%s.tmTheme"]

		# Find .tmLanguage files
		files = [f for f in os.listdir(compile.SYNESTHESIA_OUTPUT_PATH) if os.path.isfile(os.path.join(compile.SYNESTHESIA_OUTPUT_PATH, f))]
		files = sorted([f for f in files if f.endswith('.tmLanguage')])
		without_extensions = [re.sub('.tmLanguage', '', f) for f in files]

		# Ensure that all essential filetypes are present for safety reasons.
		# If we can't find all those files, we don't consider the scheme for deletion.

		without_extensions = [x for x in without_extensions if essential_filetypes_present(compile.SYNESTHESIA_OUTPUT_PATH, essential_filetypes, x)]

		def done(which):
			# Do nothing in the event of quick panel cancellation
			if not (which == -1):
				nonlocal without_extensions, essential_filetypes
				which = without_extensions[which]

				# Check if open views are using the syntax file that is going to be deleted.
				# If so, unset them.
				for v in self.window.views():
					current_def = extract_syntax_name(v.settings().get('syntax'))
					if (current_def == which):
						v.set_syntax_file("Packages/Text/Plain text.tmLanguage")

				# Delete files

				all_filetypes = essential_filetypes + ["%s.tmLanguage.cache", "%s.tmTheme.cache"]
				some_files_deleted = False

				for filepath in all_filetypes:
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