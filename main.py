from github_api import GitRepo
from testing import test
import base64
import logging

logging.basicConfig(level=logging.INFO)
_LOGGER = logging.getLogger(__name__)
_LOGGER.setLevel(logging.INFO)


def get_lang_cmd_spec(testing_lang):
    if testing_lang == "java":
        return ".java"
    if testing_lang == "c":
        pass  # можно потом добавить с/с++
    return ".py"


def get_task_num(task_detail_str):
    for task_id in task_detail_str:
        if str(task_id).isdigit():
            return int(task_id)


def get_code(res):
    for i, b in res:
        if get_lang_cmd_spec("python") in str(i) and str(i)[-3] not in "pyc jar":
            task = test.CreateTest(base64.b64decode(b.encode()).decode(), "python")
            test_case = test.CreateTestCase(get_task_num(i))
            test_case.run_test(task)


if __name__ == '__main__':
    user1 = GitRepo("https://github.com/MalofeevAV/PL_test")
    results = user1.grab_path()
    # results = t()       # TESTING VERSION # unlock upper
    get_code(results)
