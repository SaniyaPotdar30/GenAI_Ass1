import calculator
import geometry as geo

num1 = int(input("Enter num1/length="))
num2 = int(input("Enter num2/breadth="))

calculator.add(num1,num2)
calculator.multiply(num1,num2)

geo.cal_rect_area(num1,num2)
geo.cal_rect_peri(num1,num2)