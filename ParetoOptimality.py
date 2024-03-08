# -*- coding: utf-8 -*-
"""
Created on Fri Oct 27 13:47:49 2023

@author: AtamertDuman
"""

import pandas as pd
from pyomo.environ import*

model=ConcreteModel()

numOfProducts = 2 #TYPE SAYISI  
model.Products = RangeSet(numOfProducts)
#RESOURCE SETLERİ 
s = [6,12]
AvailableSteel = 200

a= [8,20]
AvailableAluminium = 300

l = [11,24]
AvailableLabor= 300

otCost=10 #OVERTİME COST 

profit = [500,1100]

solver = SolverFactory("gurobi")

model.x = Var(model.Products, domain = NonNegativeReals)
model.overTime = Var(domain = NonNegativeReals)
model.profit = Var(domain = NonNegativeReals)

model.constraint = ConstraintList()
model.constraint.add(sum(s[k-1]*model.x[k] for k in model.Products)<= AvailableSteel)
model.constraint.add(sum(a[k-1]*model.x[k] for k in model.Products)<= AvailableAluminium)
model.constraint.add(sum(l[k-1]*model.x[k] for k in model.Products)<= AvailableLabor+ model.overTime)
model.constraint.add(sum(profit[k-1]*model.x[k] for k in model.Products)-otCost*model.overTime==model.profit)

#OBJECTIVE FUNCTION 1
model.ObjectiveFunction = Objective(expr=model.profit, sense = maximize)

result = solver.solve(model)
Profit = value(model.profit)

#ADD Profit Constraint
model.profitConstraint= Constraint(expr=model.profit>= Profit)

#OBJECTIVE FUNCTION 2
model.del_component(model.ObjectiveFunction)
model.ObjectiveFunction = Objective (expr=model.overTime, sense=minimize)

#SOLVER FOR THE 2ND OBJECTIVE
result = solver.solve(model)
OverTime1=value(model.overTime)

print("Pareto Optimal Solution 1:")
print(f"Profit: {value(model.profit)}")
print(f"Overtime: {value(model.overTime)}")
for k in model.Products:
    print("Production quantity of product", k, ": ", pyomo.environ.value(model.x[k]))

print("----------------------------")
#REMOVE PROFIT CONSTRAINT  
model.del_component(model.profitConstraint)
#SOLVE FOR the 2ND OBJECTIVE
result=solver.solve(model)

Profit = value(model.profit)
OverTime = value(model.overTime)


#ADD OVERTIME CONSTRAINT
model.overtimeConstraint = Constraint(expr=model.overTime<=OverTime)
#OBJECTIVE FUNCTION 1:
model.del_component(model.ObjectiveFunction)
model.ObjectiveFunction = Objective(expr=model.profit, sense=maximize)

#SOLVER FOR THE 1ST OBJECTIVE
result = solver.solve(model)
print("Pareto Optimal Solution 2:")
print(f"Profit: {value(model.profit)}")
print(f"Overtime: {value(model.overTime)}")
for k in model.Products:
    print("Production quantity of product", k, ": ", pyomo.environ.value(model.x[k]))
    
OverTime2=value(model.overTime)  
        
#REMOVE OVERTIME CONSTRAINT
model.del_component(model.overtimeConstraint)

n=5 #?????
stepSize = (OverTime1- OverTime2)/n
for i in range(1,n):
    print("--------------------------------------")
    model.overtimeConstraint = Constraint(expr=model.overTime<=(OverTime1 - stepSize*i))
    #SOLVE FOR THE 1st OBJECTİVE
    model.del_component(model.ObjectiveFunction)
    model.ObjectiveFunction = Objective(expr=model.profit, sense=maximize)
    result = solver.solve(model)
    
    Profit = value(model.profit)
    
    #REMOVE OVERTIME CONSTRAINT
    model.del_component(model.overtimeConstraint)
    #Add Profit Constraint
    model.profitConstraint = Constraint(expr=model.profit>=Profit)
    #SOLVE FOR THE 2nd OBJECTIVE
    model.del_component(model.ObjectiveFunction)
    model.ObjectiveFunction = Objective(expr=model.overTime, sense=minimize)
    
    #SOLVER FOR THE 1ST OBJECYIVE
    result=solver.solve(model)
    print("Pareto Optimal Solution ", i+2, ":")
    print(f"Profit: {value(model.profit)}")
    print(f"Overtime: {value(model.overTime)}")
    for k in model.Products:
        print("Production quantity of product",k,": ", pyomo.environ.value(model.x[k]))
    #REMOVE Profit Constraint
    model.del_component(model.profitConstraint)




