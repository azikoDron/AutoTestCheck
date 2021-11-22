from github_api import GitRepo

user1 = GitRepo("https://github.com/MalofeevAV/PL_test")
results = user1.grab_path()


def get_lang_cmd_spec(testing_lang):
    if testing_lang == "java":
        return ".java"
    if testing_lang == "c":
        pass  # можно потом добавить с/с++
    return ".py"


def get_code():
    for i in results[0]:
        if get_lang_cmd_spec(user1.language) in str(i[0]):
            print(i)


