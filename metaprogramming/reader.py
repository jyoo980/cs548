import os

class Reader:

    @staticmethod
    def read_impl(file_name):
        working_dir = os.getcwd()
        with open(f"{working_dir}/{file_name}", "r") as f:
            content = f.read()
            return content
