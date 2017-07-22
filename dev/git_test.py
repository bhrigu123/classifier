class Classifier:
    def save_current(self, directory):
        self.import_git()
        repo = git.Repo.init(directory)  # works even if repo already exists
        repo.git.add('--all', '--force')
        repo.git.commit('--author="Classifier <https://github.com/jyn514/classifier>"',
                        '--message="Saved by classifier.py to allow an undo function."',
                        '--quiet')
        
    def undo(self, directory, commit=None):
        # commit is an integer of number of previous revisions
        self.import_git()
        repo = git.Repo.init(directory)
        version = 'master'
        if commit:
            version += '~'
            version += commit
        repo.git.checkout('--force', version)

    def import_git(self):
        try:
            import git
            git = self.git
        except ImportError:
            print("You must install both git and gitpython to use the undo " +
                  "function, using `apt install git` and `pip install gitpython`.")
            print("Note: If both are installed and you still see this error, " +
                  "make sure you installed gitpython for the version of python " +
                  "you are using.")
            quit()
