from github import Github


class GitRepo(Github):
    def __init__(self, repository):
        super().__init__()
        self._repository = str(repository).split("/")
        self._user = self.get_user(self._repository[3])       # << self.get_user(repository[3])
        self._repo = self._user.get_repo(self._repository[4])
        self.language = self._repo.language

    def grab_path(self):
        contents = self._repo.get_contents("")
        z = []
        while contents:
            file_content = contents.pop(0)
            if file_content.type == "dir":
                contents.extend(self._repo.get_contents(file_content.path))
            else:
                z.append([file_content.path, file_content.content])
        return z

    def content(self):
        return self._repo.get_contents("")


if __name__ == '__main__':
    user1 = GitRepo("https://github.com/MalofeevAV/PL_test")
    gr = user1.grab_path()
    print(gr)
