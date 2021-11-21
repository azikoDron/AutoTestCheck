from github import Github
import base64


class GitRepo(Github):
    def __init__(self, repository):
        super().__init__()
        self._repository = str(repository).split("/")
        # self._git = Github()
        self._user = self.get_user(self._repository[3])       # << self.get_user(repository[3])
        self._repo = self._user.get_repo(self._repository[4])

    # def get_user(self):
    #     return self._git.get_user(self._repository[3])

    def grab_path(self):
        contents = self._repo.get_contents("")
        while contents:
            file_content = contents.pop(0)
            if file_content.type == "dir":
                contents.extend(self._repo.get_contents(file_content.path))
            else:
                print(file_content, file_content.type, file_content.content)

    def content(self):
        return self._repo.get_contents("")

    def test(self):
        print(self._repo)
       # print(self._repo.get_)


user1 = GitRepo("https://github.com/Atestov/TestTaskPL")
user1.test()

user1.grab_path()
# print(user1.content()[3])       #  #
# print(base64.b64decode(user1.content()[3].content.encode()).decode())
# user = g.get_user("azikoDron")
# repo = user.get_repo("MyKivyApp")
#
# print(repo.get_contents(""))

# r = g.get_repo("https://github.com/azikoDron/MyKivyApp")

# c = r
#
# print(c)
