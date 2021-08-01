coverage run --rcfile= /tests/test.coveragerc -m unittest discover -s tests/
coverage report -m
coverage html --rcfile= /tests/test.coveragerc
# 不懂 not working - 2021/07/29