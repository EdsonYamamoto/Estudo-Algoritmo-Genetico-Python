def test():
	teste='teste'
import timeit
print(timeit.timeit('test()', setup='from __main__ import test'))
