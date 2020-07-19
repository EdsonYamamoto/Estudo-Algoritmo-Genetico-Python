from jinja2 import Template
from datetime import datetime

from subprocess import check_output

genFilePath = "./code/"

class Method:

    def __init__(self, name):

        self.name = name
        self.method = f"def {name}():\n\tteste='teste'\n"

    def getMethod(self):
        
        self.method += f"import timeit\nprint(timeit.timeit('test()', setup='from __main__ import test'))\n"
        return self.method

f = open(genFilePath+"gen.py", "w")
f.write(Method("test").getMethod())
f.close()

teste = float(check_output("python code/gen.py", shell=True).decode('ascii'))
print(teste)