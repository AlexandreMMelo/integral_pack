
from sympy import Symbol, integrate, solveset, Eq, init_printing
import argparse


init_printing(use_unicode=True, wrap_line=True, pretty_print=False)

global x, y, z, k, m, n
x = Symbol('x')
y = Symbol('y')
z = Symbol('z')
k = Symbol('k', integer=True)
m = Symbol('m', integer=True)
n = Symbol('n', integer=True)

def integral(expre, a, b):

    return (integrate(expre,(x, a, b)))


def integral_func(expre1, expre2):

    expre = '{}-({})'.format(expre1,expre2)
    a_b = solveset(Eq(expre, 0), x)
    result = integrate(expre1, (x,*a_b)) - integrate(expre2, (x,*a_b))
    
    return result


def integral_dupla(expre):
    expre = integrate(expre,x).doit()
    return integrate(expre, x).doit()

def main():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    parser.add_argument('-e1', help='é a primeira expressão', type=str)
    parser.add_argument('-d', help='caso queira calcular o valor de uma integral dupla', action='store_true')
    group.add_argument('-e2', help='é a segunda expressão', type=str)
    group.add_argument('-a', help='defina um valor inicial para a integração', type=int)
    parser.add_argument('-b', help='defina um valor final para a integração', type=int)
    args = parser.parse_args()
    

    if args.e1 != None and args.d:
        print(integral_dupla(args.e1))
    
    elif args.e1 == None or ((args.e2 == None and (args.a == None or args.b ==None)) or args.d): 
        print('Argumentos invalidos. consulte o help usando \"-h\"')

    elif args.a != None: 
        print(integral(args.e1, args.a, args.b).evalf())

    else:
       print(integral_func(args.e1, args.e2)) 


if __name__ == "__main__":
    main()
	
