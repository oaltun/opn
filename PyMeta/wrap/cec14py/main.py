import cec14_test_func
import numpy as np

print dir(cec14_test_func)

x= np.array([[1,2],[3,4]]).astype(float)
func_num=1

f=cec14_test_func.value(x,func_num)
f=cec14_test_func.value(x,func_num)

print "x\n",x
print "f\n",f


#a=raw_input('enter char')
