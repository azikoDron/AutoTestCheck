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
    def __init__(self, case_num):
        self.case_num = case_num
        self.is_file_testing = True
        self.data_being_tested = self.load_data_being_tested()   # [['4', '3'], ['5', '4']]
        self.correct_data = self.load_correct_data()
        self.result_data = []

    def load_data_being_tested(self):
        return self.load_data_from_json()["case_" + str(self.case_num)]["data_being_tested"]

    def load_correct_data(self):
        return self.load_data_from_json()["case_" + str(self.case_num)]["correct_data"]

    def load_data_from_json(self, param_file="test_cases"):
        with open(f"{param_file}.json", "r") as r:
            return json.load(r)

    def run_test(self, obj):
        """

        :param obj: объект класса CreateTest
        :return:
        """
        if self.case_num in [1, 2, 4]:
            try:
                data = self.data_being_tested
                if self.is_file_testing:
                    data = [self.create_case_file()]
                    if self.case_num == 4:
                        return self.case_4(obj, data)
                for i, b in data:
                    res = ""
                    for u in obj.run_os_cmd(i, b):
                        if u.isdigit():
                            res += u
                    self.result_data.append(res)
                return self.get_result()
            except Exception as e:
                if self.is_file_testing:
                    self.is_file_testing = False
                    return self.run_test(obj)
        if self.case_num in [3]:
            return self.test_3(obj)


    def get_result(self):
        # print(self.result_data, self.correct_data)
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
        # print(case_files)
        return case_files

    def test_3(self, obj):
        data = self.data_being_tested
        for i, b in data:
            obj.run_os_cmd(f"test_files{os.sep}{i}", f"test_files{os.sep}{b}")
            self.result_data.append(self.load_data_from_json(param_file="report"))
            return self.get_result()

    def case_4(self, obj, data):
        for i in data[0]:
            res = ""
            for u in obj.run_os_cmd(i):
                if u.isdigit():
                    res += u
            self.result_data.append(res)
        return self.get_result()


if __name__ == '__main__':
    task_1_py = """
import sys
import math

data_file = sys.argv[1]
total = 0
steps = 0

with open(data_file, 'r') as file:
    arr = [int(x) for x in file]

for item in arr:
    total += item

average = math.ceil(total / len(arr))

for item in arr:
    if item > average:
        while(item != average):
            steps += 1
            item -= 1
    elif item < average:
        while(item != average):
            steps += 1
            item += 1
    else:
        continue
 
print(steps)
    """
    task_1_py = CreateTest(task_1_py, "python")
    test_case_1 = CreateTestCase(4)
    print(test_case_1.run_test(task_1_py))
