'''
Created on 16 Mar 2014

@author: oguz
'''
import cec14_test_func as cec
import pymeta as pm
import numpy as np


class Cec14SOOProblem(pm.OptimizationProblem):
    def __init__(self, **kwargs):
        pm.OptimizationProblem.__init__(self)  # inherit
        self.ub = np.array([100, 100])  # #defaults
        self.lb = -1 * self.ub
        self.func_num = None
        self.name = 'f'
        self.visualiser = pm.TwoDFunVisualiser(
            fun = self.cost, lb = self.lb, ub = self.ub,
            step = (self.ub - self.lb) / 100.0
            )
        self.__dict__.update(**kwargs)  # #overwrite
        self.minimize = True
        self.name = self.name + str(self.func_num)

    # only gooddims are supported. See this code in cec14_test_func.c:
    #        if (!(nx==2||nx==10||nx==20||nx==30||nx==50||nx==100))
    #        {
    #            printf("\nError: Test functions are only defined for "
    #                "D=2,10,20,30,50,100.\n");
    #        }
    gooddims = [2, 10, 20, 30, 50, 100]

    # when number of dimensions is two, following functions are not supported.
    # See this code in cec14_test_func.c
    #        if (nx==2&&((func_num>=17&&func_num<=22)||
    #            (func_num>=29&&func_num<=30)))
    #        {
    #            printf("\nError: hf01,hf02,hf03,hf04,hf05,hf06,cf07&cf08 "
    #                "are NOT defined for D=2.\n");
    #        }
    badnum2 = [17, 18, 19, 20, 21, 22, 29, 30]

    def costfun(self, x):
        #x needs to have two dimensions
        x = x.reshape((1, -1))

        # call the wrapped cec function
        v = cec.value(x, self.func_num)

        # cec.value() function returns an array as opposed to a scalar
        return v[0]
