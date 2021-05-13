import os
import pathlib
import json
from scipy.stats import norm
from scipy.stats import t
import math
ROOT = pathlib.Path().absolute()
JSON_FILE_NAME = "stat_information.json"
JSON_FILE_PATH = ROOT / JSON_FILE_NAME

VALID_TESTS = ["one_mean_interval", "one_mean_test", "two_mean_interval", "two_mean_test"]



def openStatStorageJson():
    with open(JSON_FILE_PATH, 'r') as stat_storage:
        return json.load(stat_storage)
#saves changes to the stat storage.json file

def saveStatStorageJson(new_json):
    with open(JSON_FILE_PATH, 'w') as stat_storage:
        json.dump(new_json, stat_storage, indent=4)

def main():
    if(not JSON_FILE_PATH.exists()):
        print("No input JSON file detected, creating a JSON file now")
        json_storage = {}
        json_storage['test_name'] = "Check attatched code for valid test names, not all tests use all variables"
        json_storage['mu'] = "null hypothesis mean"
        json_storage['Ha'] = "should be >, <, or !=, mu"
        json_storage['signifigance_level'] = "alpha value, should be .05 or something"
        json_storage['x_bar_one'] = "sample mean one"
        json_storage['std_dev_one'] = "standard deviation one, can be sample or population"
        json_storage['sample_size_one'] = "size of the sample of one"
        json_storage['x_bar_two'] = "sample mean two"
        json_storage['std_dev_two'] = "standard deviation two, can be sample or population"
        json_storage['sample_size_two'] = "size of the sample of two"
        json_storage['is_pop_std_dev'] = "whether or not this program is working with the population standard deviation"
        json_storage['pooled?'] = 'whether or not the samples can be pooled'
        saveStatStorageJson(json_storage)
        print("the input JSON file was created, go edit it then run this program")
        return
    
    stats = openStatStorageJson()
    switcher = {
        "one_mean_interval":oneMeanInterval,
        "one_mean_test":oneMeanTest,
        "two_mean_test":twoMeanTest,
        "two_mean_interval":twoMeanInterval
    }
    switcher.get(stats['test_name'])(stats)

def oneMeanInterval(stats):
    sig_level = float(stats['signifigance_level'])
    test_type = "z"
    if (stats["is_pop_std_dev"] == "false"):
        test_type = "t"
    
    mu = float(stats['mu'])
    x_one = float(stats['x_bar_one'])
    std_dev_one = float(stats['std_dev_one'])
    sample_one = int(stats['sample_size_one'])
        
    std_dev_modified = std_dev_one / math.sqrt(sample_one)

        
    degrees_of_freedom = sample_one - 1

    #Critical value used as the T_a/2 or whatever
    cv_value = 0
    if(test_type == "t"):
        cv_value = t.ppf(sig_level/2, degrees_of_freedom)
    else:
        cv_value = norm.ppf(sig_level/2)
    
    #cv_value is always going to be negative, I just want MOE to be positive
    margin_of_error = cv_value * std_dev_modified * (-1)
    mean = x_one
    low = mean - margin_of_error
    high = mean + margin_of_error
    print("CI at a sig level of {0}%: ({1},{2})".format((1 - sig_level) * 100, low, high))

def oneMeanTest(stats):
    sig_level = float(stats['signifigance_level'])
    test_type = "z"
    if (stats["is_pop_std_dev"] == "false"):
        test_type = "t"
    
    mu = float(stats['mu'])
    x_one = float(stats['x_bar_one'])
    std_dev_one = float(stats['std_dev_one'])
    sample_one = int(stats['sample_size_one'])

    std_dev_modified = std_dev_one / math.sqrt(sample_one)

        
    degrees_of_freedom = sample_one - 1
    test_statistic = (x_one - mu )/std_dev_modified
    print("the test_statistic is {0}".format(test_statistic))
    
  
    #now its time to calculate CV and P-value
    p_value = -1
    if(test_type == "t"):
        p_value = t.cdf(test_statistic, degrees_of_freedom)    
    else:
        p_value = norm.cdf(test_statistic)
    
    if(stats['Ha'] == ">"):
        p_value = 1-p_value
    if(stats['Ha'] == "!="):
        if(test_statistic > 0 ):
            p_value = 1 - p_value
        p_value = p_value * 2
    print("The p-value is {0}".format(p_value))
    
    #CV time
    cv_value = 0
    if(test_type == "t"):
        cv_value = t.ppf(sig_level, degrees_of_freedom)
        if(stats['Ha'] == "!="):
            cv_value = t.ppf(sig_level / 2, degrees_of_freedom)
    else:
        cv_value = norm.ppf(sig_level)
        if(stats['Ha'] == "!="):
            cv_value = norm.ppf(sig_level / 2)
    
    if(stats['Ha'] == ">"):
        cv_value = -1*cv_value
    
    print("cv_value: {0}".format(cv_value))

def twoMeanInterval(stats):
    sig_level = float(stats['signifigance_level'])
    test_type = "z"
    if (stats["is_pop_std_dev"] == "false"):
        test_type = "t"
    
    
    x_one = float(stats['x_bar_one'])
    std_dev_one = float(stats['std_dev_one'])
    sample_one = int(stats['sample_size_one'])

    x_two = float(stats['x_bar_two'])
    std_dev_two = float(stats['std_dev_two'])
    sample_two = int(stats['sample_size_two'])

    if(stats['pooled?'] == 'true'):
        #std dev calculation starts here for pooled
        a = (sample_one - 1)*(std_dev_one*std_dev_one)
        b = (sample_two - 1)*(std_dev_two*std_dev_two)
        numerator = a + b
        denominator = sample_one + sample_two -2
        std_dev = math.sqrt(numerator/denominator)
        print("std_dev: {0}".format(std_dev))
        print("remember if you ever want to use std_dev to multiply by sqrt(n1^-1 + n2^-1)")
        std_dev_modified = std_dev * math.sqrt( (1/sample_one) + (1/sample_two))
        print("std_dev with the above factored in: {0}".format(std_dev_modified))
        degrees_of_freedom = sample_one+sample_two - 2
    else:
        #non-pooled standard dev
        a = (std_dev_one * std_dev_one) / sample_one
        b = (std_dev_two * std_dev_two) / sample_two

        std_dev = math.sqrt( a + b)
        print("std_dev: {0}".format(std_dev))
        #does not need to be modified any further
        std_dev_modified = std_dev

        #now to calculate degrees of freedom
        print("remember the non-pooled test uses the big fat degrees of freedom equation")
        numerator = (a+b)*(a+b)
        denominator = ( (a*a)/(sample_one - 1) ) + ( (b*b)/(sample_two - 1) )
        degrees_of_freedom = math.trunc(numerator/denominator)
        print("REMEMBER: degrees of freedom is {0}".format(degrees_of_freedom))
        
    
    #Critical value used as the T_a/2 or whatever
    cv_value = 0
    if(test_type == "t"):
        cv_value = t.ppf(sig_level/2, degrees_of_freedom)
    else:
        cv_value = norm.ppf(sig_level/2)
    
    #cv_value is always going to be negative, I just want MOE to be positive
    margin_of_error = cv_value * std_dev_modified * (-1)
    mean = x_one - x_two
    low = mean - margin_of_error
    high = mean + margin_of_error
    print("CI at a sig level of {0}%: ({1},{2})".format((1 - sig_level) * 100, low, high))

    
    

def twoMeanTest(stats):
    #always does x1 - x2
    #always assumes that the data is pooled!!!!
    sig_level = float(stats['signifigance_level'])
    test_type = "z"
    if (stats["is_pop_std_dev"] == "false"):
        test_type = "t"
    
    
    x_one = float(stats['x_bar_one'])
    std_dev_one = float(stats['std_dev_one'])
    sample_one = int(stats['sample_size_one'])

    x_two = float(stats['x_bar_two'])
    std_dev_two = float(stats['std_dev_two'])
    sample_two = int(stats['sample_size_two'])

    if(stats['pooled?'] == 'true'):
        #std dev calculation starts here for pooled
        a = (sample_one - 1)*(std_dev_one*std_dev_one)
        b = (sample_two - 1)*(std_dev_two*std_dev_two)
        numerator = a + b
        denominator = sample_one + sample_two -2
        std_dev = math.sqrt(numerator/denominator)
        print("std_dev: {0}".format(std_dev))
        print("remember if you ever want to use std_dev to multiply by sqrt(n1^-1 + n2^-1)")
        std_dev_modified = std_dev * math.sqrt( (1/sample_one) + (1/sample_two))
        print("std_dev with the above factored in: {0}".format(std_dev_modified))
        degrees_of_freedom = sample_one+sample_two - 2
    else:
        #non-pooled standard dev
        a = (std_dev_one * std_dev_one) / sample_one
        b = (std_dev_two * std_dev_two) / sample_two

        std_dev = math.sqrt( a + b)
        print("std_dev: {0}".format(std_dev))
        #does not need to be modified any further
        std_dev_modified = std_dev

        #now to calculate degrees of freedom
        print("remember the non-pooled test uses the big fat degrees of freedom equation")
        numerator = (a+b)*(a+b)
        denominator = ( (a*a)/(sample_one - 1) ) + ( (b*b)/(sample_two - 1) )
        degrees_of_freedom = math.trunc(numerator/denominator)
        print("REMEMBER: degrees of freedom is {0}".format(degrees_of_freedom))
        

    test_statistic = (x_one - x_two)/std_dev_modified
    print("the test_statistic is {0}".format(test_statistic))
    
  
    #now its time to calculate CV and P-value
    p_value = -1
    if(test_type == "t"):
        p_value = t.cdf(test_statistic, degrees_of_freedom)    
    else:
        p_value = norm.cdf(test_statistic)
    
    if(stats['Ha'] == ">"):
        p_value = 1-p_value
    if(stats['Ha'] == "!="):
        if(test_statistic > 0 ):
            p_value = 1 - p_value
        p_value = p_value * 2
    print("The p-value is {0}".format(p_value))
    
    #CV time
    cv_value = 0
    if(test_type == "t"):
        cv_value = t.ppf(sig_level, degrees_of_freedom)
        if(stats['Ha'] == "!="):
            cv_value = t.ppf(sig_level / 2, degrees_of_freedom)

    else:
        cv_value = norm.ppf(sig_level)
        if(stats['Ha'] == "!="):
            cv_value = norm.ppf(sig_level / 2)
    
    if(stats['Ha'] == ">"):
        cv_value = -1*cv_value
    
    print("cv_value: {0}".format(cv_value))





    
main()