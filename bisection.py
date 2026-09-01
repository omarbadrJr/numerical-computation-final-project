import math  # for using mathematical calculations

# Substitute x with a and b and c to evaluate the function 
def f(x):
    return eval(equation, {"math": math, "x": x})

# taking the values of a and b from the user
a = float(input("enter the value of the first number:  "))
b = float(input("enter the value of the second number:  "))

# taking the equation from the user 
equation = input("enter the equation:   ")
# the user write ^ instead of ** incase he is using the power
equation = equation.replace("^","**")

# quiting the function incase both function give positive values or both give negative values bec one of them must be + and the other must be -
if f(a) * f(b) >= 0:
    print("invalid interval")
    quit() 
else:
    # asking the user how many iterations he wants
    iterations = int(input("how many iterations you want:     "))
    for i in range(iterations):
        c = (a + b) / 2      # getting the new value from a+b/2 which equal c 
        fb = f(b)  # calling the function "f(x)" and substitute the b with x
        fc = f(c)  # the same but with c 
        # if we got the root which make the equation = 0 , so we stop the loop 
        if fc == 0: 
            print("the root = ",c)    
            break        
        # replacing the c with a or b which depends on the value of the f(x) of each of them 
        if fc * fb > 0:
            b = c
        else:
            a = c

    print("The approximate root =", c)
    print("number of iterations used = " , i+1)
    

