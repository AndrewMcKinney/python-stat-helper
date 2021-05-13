import math
from scipy.stats import norm
from scipy.stats import t
from scipy.stats import chi2
from scipy.stats import f

def main():
    f_dist()

def norm_dist():
    z_value = -1.29
    print("here you go: {0}".format(norm.cdf(z_value)))

def f_dist():
    #f.ppf(a, dfn, dfd)
    #REMEMBER DF IS n - 1
    alpha = 0.05
    #put in regualr order
    dfn = 3
    dfd = 16
    print("F DIST")
    #THIS FUNCTION ALREADY DIVIDES BY 1/N
    #IT WILL ALSO AUTOMATICALLY REVERSE THE INPUT
    #IT IS CRACKED
    print("LCV: {0}".format(f.ppf(alpha, dfn, dfd)))
    print("RCV: {0}".format(f.ppf(1-alpha, dfn, dfd)))

def chi_squared():
    #chi.ppf(area, degrees of freedom)
    #area is area to left
    #this is unlike the chat which does area to right
    alpha = 0.01
    df = 2
    print("CHI2 DIST")
    print("LCV: {0}".format(chi2.ppf(alpha, df)))
    print("RCV: {0}".format(chi2.ppf(1-alpha, df)))

def pooled_std_dev():
    x_one = 12.87
    std_dev_one = 3.53
    sample_one = 10

    x_two = 18.42
    std_dev_two = 4.19
    sample_two = 10

    a = (sample_one - 1)*(std_dev_one*std_dev_one)
    b = (sample_two - 1)*(std_dev_two*std_dev_two)
    numerator = a + b
    denominator = sample_one + sample_two -2
    std_dev = math.sqrt(numerator/denominator)
    print("std_dev: {0}".format(std_dev))
    print("remember if you ever want to use std_dev to multiply by sqrt(n1^-1 + n2^-1)")
    std_dev_modified = std_dev * math.sqrt( (1/sample_one) + (1/sample_two))
    print("std_dev with the above factored in: {0}".format(std_dev_modified))
    test_statistic = (x_one - x_two)/std_dev_modified
    print("the test_statistic is {0}".format(test_statistic))
    print("REMEMBER: degrees of freedom is {0}".format(sample_one+sample_two - 2))





def non_pooled_std_dev():
    #just change these directly, like who cares
    x_one = 16
    std_dev_one = 2.6
    sample_one = 20

    x_two = 18
    std_dev_two = 2.3
    sample_two = 20
    #so the actual std_Dev is just std_dev_one^2 + std_dev_two^2 = std_dev_total^2
    #but for some reason this never comes up in statistics
    #lmao
    a = (std_dev_one * std_dev_one) / sample_one
    b = (std_dev_two * std_dev_two) / sample_two

    numerator = x_one - x_two
    denominator = math.sqrt( a + b)
    rtn = numerator / denominator
    print("std dev: {0}".format(denominator))
    print("t/z-score: {0}".format(rtn))


main()