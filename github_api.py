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

    def content(self):
        return self._repo.get_contents("")

    def test(self):
        print(self._repo)
       # print(self._repo.get_)


user1 = GitRepo("https://github.com/azikoDron/MyKivyApp")
user1.test()
print(user1.content()[3])
print(base64.b64decode(user1.content()[3].content.encode()).decode())
# user = g.get_user("azikoDron")
# repo = user.get_repo("MyKivyApp")
#
# print(repo.get_contents(""))

# r = g.get_repo("https://github.com/azikoDron/MyKivyApp")

# c = r
#
# print(c)
