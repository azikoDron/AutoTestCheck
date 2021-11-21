# encoding=utf-8
import sys
import os
import subprocess
import logging
import json

logging.basicConfig(level=logging.INFO)
_LOGGER = logging.getLogger(__name__)
_LOGGER.setLevel(logging.INFO)


class CreateTest:
    def __init__(self, content, language):
        """

        :param content: python код из гита
        """
        self.content = content
        self.testing_lang = language
        self.testing_lang_cmd_run = self.get_lang_cmd_header()
        self.testing_lang_spec = self.get_lang_cmd_spec()
        self.file_name = self.make_tmp_file()

    def get_lang_cmd_header(self):
        if self.testing_lang == "java":
            return "javac"      # !НУЖНО ПОМЕНЯТЬ НА ВИРТУАЛЬНОЕ ОКРУЖЕНИЯ
        if self.testing_lang == "c":
            pass                # можно потом добавить с/с++
        return "python"         # !НУЖНО ПОМЕНЯТЬ НА ВИРТУАЛЬНОЕ ОКРУЖЕНИЯ

    def get_lang_cmd_spec(self):
        if self.testing_lang == "java":
            return ".java"
        if self.testing_lang == "c":
            pass  # можно потом добавить с/с++
        return ".py"

    def make_tmp_file(self, file_name=f"tmp"):
        with open(f"{file_name}{self.testing_lang_spec}", "w", encoding="utf-8") as w:
            w.write(self.content)
        return file_name + self.testing_lang_spec

    def run_os_cmd(self, *args):
        inp = f"{self.testing_lang_cmd_run} {self.file_name}"
        for i in args:
            inp += f" {i}"
        return subprocess.check_output(inp, shell=True, text=True)

    # def run_check(self):
    #     return os.system(self.get_cmd_param())
    #

    # def check_by_str(self, *args):
    #     return os.system(f"python tmp{os.sep}{self.file_name}.py {args.}")
    #


class CreateTestCase:
    def __init__(self):
        self.case_num = 1
        self.is_file_testing = True
        self.data_being_tested = self.load_data_being_tested()   # [['4', '3'], ['5', '4']]
        self.correct_data = self.load_correct_data()
        self.result_data = []

    def load_data_being_tested(self):
        return self.load_params()["case_" + str(self.case_num)]["data_being_tested"]

    def load_correct_data(self):
        print(self.load_params()["case_" + str(self.case_num)]["correct_data"])
        return self.load_params()["case_" + str(self.case_num)]["correct_data"]

    def load_params(self):
        with open("test_cases.json", "r") as r:
            return json.load(r)

    def test_case(self, obj):
        """

        :param obj: объект класса CreateTest
        :return:
        """
        try:
            data = self.data_being_tested
            if self.is_file_testing:
                data = [self.create_case_file()]
            for i, b in data:
                res = ""
                for u in obj.run_os_cmd(i, b):
                    if u.isdigit():
                        res += u
                self.result_data.append(res)
        except Exception as e:
            if self.is_file_testing:
                self.is_file_testing = False
                self.test_case(obj)

    def get_result(self):
        print(self.result_data, self.correct_data)
        if self.result_data == self.correct_data:
            return True
        return False

    def create_case_file(self, file_type=".txt"):
        """
        ОДИН ТЕСТ : [[1, 1], [0, 0]],
        :param file_type:
        :param data_list: data_list=[4, 5]
        :return:
        """
        # sample = [[1, 1], [0, 0]]
        case_files = []
        for i, b in enumerate(self.data_being_tested):
            with open(f"test_files{os.sep}{i}{file_type}", "w", encoding="utf-8") as d:
                for z in b:
                    d.write(z + '\n')
                # d.write(str(b).replace("[", "").replace("]", "").replace(",", "").replace("'", ""))
                case_files.append(f"test_files{os.sep}{i}{file_type}")
        print(case_files)
        return case_files


if __name__ == '__main__':
    task_1_py = """
import math
import sys
import re

with open('{}'.format(sys.argv[1]), 'r') as f1:
    file1 = f1.read()

num_cor = re.findall(r'\d+', file1)
a = float(num_cor[0])
b = float(num_cor[1])
r = float(num_cor[2])
with open('{}'.format(sys.argv[2]), 'r') as f2:
    file2 = f2.read()

xy = re.findall(r'\d+', file2)
answer = []
for i in range(1, len(xy), 2):
    x = float(xy[i - 1])
    y = float(xy[i])
    if math.sqrt((x - a) ** 2) + math.sqrt((y - b) ** 2) < math.sqrt(r ** 2):
        answer.append(1)
    elif math.sqrt((x - a) ** 2) + math.sqrt((y - b) ** 2) == math.sqrt(r ** 2):
        answer.append(0)
    else:
        answer.append(2)

for i in range(len(answer)):
    print(answer[i], 'n')

    """
    task_1_py = CreateTest(task_1_py, "python")
    test_case_1 = CreateTestCase()
    print(test_case_1.test_case(task_1_py), test_case_1.create_case_file(), test_case_1.result_data)
