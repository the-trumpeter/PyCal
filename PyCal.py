import tkinter as tk
from rich import print
import time as tm
from typing import List


root = tk.Tk()
root.title("Calculator")


screenoutDefalt="Enter a sum"
screenout=screenoutDefalt

screeenoutContainsAnswer= False
currentAnswer = None

active=True


specialKeyIcons=["⌫", "+", "-", "×", "÷"]
specialKeyOutput=["D","+","-","×","÷"]







numbers="1234567890"
operators=["÷","×","+","-"]

pedmas=["div","times","plus","minus"]#order in which to calculates

firstLocationOfOperator = [0, 0, 0, 0]
amountOfEachOperator = [0, 0, 0, 0]

def rootCalculate(num1: float, operator: str, num2: float):
    if operator == "+":
        return float(num1) + float(num2)
    elif operator == "-":
        return float(num1) - float(num2)
    elif operator == "÷":
        return float(num1) / float(num2)
    elif operator == "×":
        return float(num1) * float(num2)
    else:
        print("ROOTCALCULATE: [red] Error: unrecognised operator")

def splitAndCalculate(listInput: List[str], operatorAmounts: List[int]):
    OutputList = listInput.copy()
    ronge = max(4, sum(operatorAmounts))

    finalResult = OutputList.copy()

    for f in range(ronge):
        workerInt = operatorAmounts[f]
        currentOperator = operators[f]

        if workerInt > 0:
            for m in range(workerInt):
                operatorPos = finalResult.index(currentOperator)

                firstNumber = finalResult[operatorPos - 1]
                secondNumber = finalResult[operatorPos + 1]

                if firstNumber == "" or secondNumber == "":
                    print("SPLIT WORKER C-GPT: [green]Error: One of the numbers is empty. Skipping...")
                    break

                print(f"SPLIT WORKER: [green]Sum: {firstNumber} {currentOperator} {secondNumber}")
                result = rootCalculate(float(firstNumber), currentOperator, float(secondNumber))
                
                finalResult[operatorPos + 1] = result
                finalResult[operatorPos - 1] = ""  # Remove the first number
                finalResult[operatorPos] = ""       # Remove the operator

    outShop = [item for item in finalResult if item]
    print(outShop)

    # If only one number is left after calculation, return that
    if len(outShop) == 1:
        return float(outShop[0])
    
    # If there are still two numbers left
    numbers = [item for item in outShop if item not in operators]
    if len(numbers) >= 2:
        finalOutput = rootCalculate(float(numbers[-2]), str(outShop[outShop.index(numbers[-2]) + 1]), float(numbers[-1]))
        return finalOutput  # Return the final output

    print("Not enough valid numbers for final calculation.")
    return None



def convertToList(inputString: str):
    current = ""
    list_of_inputString = []
    for char in inputString:
        if char in operators:
            if current:
                list_of_inputString.append(current)
                current = ""
            list_of_inputString.append(char)
        elif char == "=":
            continue
        else:
            current += char
    if current:
        list_of_inputString.append(current)
    return list_of_inputString

def calculate():
    print("[bold green]\n~CALCULATING~\n")
    
    global screenout
    global operators
    global firstLocationOfOperator
    global amountOfEachOperator

    phrases = sum(screenout.count(op) for op in operators)
    print(f"[bold green]There are {int(phrases) + 1} phrases in the sum.")

    for y, op in enumerate(operators):
        try:
            firstLocationOfOperator[y] = int(screenout.index(op))
            amountOfEachOperator[y] = screenout.count(op)
        except ValueError:
            firstLocationOfOperator[y] = None
            amountOfEachOperator[y] = 0
            
    splitworker=splitAndCalculate(convertToList(screenout), amountOfEachOperator)
    print(f"[green]Amount of each operator: {amountOfEachOperator}")
    print(f"[green]First location of each operator: {firstLocationOfOperator}")
    print(f"[green]LIST RETURN: {convertToList(screenout)}")
    print(f"[green]ROOT LIST RETURN: {splitworker}")
    print("[bold green]\n~END CALCULATION OUTPUT~")
    print(f"[bold green]ANSWER: {splitworker}")
    print("\n🎉\n")
    return(splitworker) #🎉
#end()







def button_function(button_id: int):#this runs when any button is pressed, so it splits operators from numbers, and recognises when te equals key is pressed etc
    global active
    global errorMessage
    global screeenoutContainsAnswer
    global currentAnswer
    print(f"\n[red]Button [bold red]{str(button_id)}","[red]pressed!")
    
    specialKeys=("".join(specialKeyOutput)+"=")#List of all operators
    
    if active:
        errorMessage("")
        if specialKeys.find(str(button_id))>=0:#if in the specialKeys strint
            if screeenoutContainsAnswer:
                if operators.count(str(button_id))>0:
                    output=(str(currentAnswer)+str(button_id))
                    updatescreen(output)
                    screeenoutContainsAnswer=False
                    return
            
            if button_id=="D":#DELETE
                if not screeenoutContainsAnswer:
                    updatescreen(removeXCharachtersFromEnd(screenout, 1))
                    print(f"Special key was found!{button_id, "".join(specialKeyOutput).find(str(button_id))}")
                elif screeenoutContainsAnswer:
                    updatescreen(screenoutDefalt)
                    print(f"Special key was found, and we removed text onscreen!{button_id, "".join(specialKeyOutput).find(str(button_id))}")
            elif button_id=="=":
                updateScreenAdditive(str(button_id))
                print(f"Special key was found!{button_id}, {"".join(specialKeyOutput).find(str(button_id))}")
                answer = calculate()
                updateScreenAdditive(answer)
                screeenoutContainsAnswer=True
                currentAnswer = answer

                
            else:
                if operators.count(screenout[len(screenout)-1])>0 or screenout==screenoutDefalt and operators.count(button_id)>0:
                    updateScreenAdditive("0")
                    updateScreenAdditive(button_id)
                    print(f"Special key was found!{button_id, "".join(specialKeyOutput).find(str(button_id))}")
                else:
                    print(f"Special key was found!{button_id, "".join(specialKeyOutput).find(str(button_id))}")
                    updateScreenAdditive(str(button_id))
            
        elif numbers.find(str(button_id))>=0:
            if screeenoutContainsAnswer:
                updatescreen(str(button_id))
                screeenoutContainsAnswer=False
            elif not screeenoutContainsAnswer:
                updateScreenAdditive(str(button_id))
        elif button_id==".":
            updateScreenAdditive(str(button_id))
            print(f"We got the dot: '{button_id}'")
        else:
            
            updatescreen("Disabled")
            errorMessage("please contact developer with error code UB1")
            active=False
            
        
    else:
        errorMessage("please contact developer")
        updatescreen("Disabled")






def removeXCharachtersFromEnd(string, amout):
    global screenoutDefalt
    if len(str(string))==1 or len(str(string))==0 or string==screenoutDefalt:
        return(screenoutDefalt)
    else:
        str1 = string
        list1 = list(str1)
        list2 = list1[:-1]
        return(''.join(list2))






def updateScreenAdditive(button_id):
    if screenout==screenoutDefalt:
        updatescreen(button_id)
    else:
        updatescreen(str(screenout)+str(button_id))





canrun=False
displayframe=None

def updatescreen(output):
    global canrun
    global displayframe
    global screenout
    
    
    if canrun:
        
        displayframe.destroy()
        
        screenout=output
        
        displayframe=tk.Label(text=output, height=2)
        displayframe.grid(row=1, column=1, columnspan=3)
        
        print(f"[bold blue]{screenout}")
        
    
    else:
        displayframe=tk.Label(text=output, height=2)
        displayframe.grid(row=1, column=1, columnspan=3)
        
        print(f"[bold blue]{screenout}")
        
        canrun=True

updatescreen(screenout)







canrunError=False
errorframe=None
errorOut = ""

def errorMessage(output):
    global canrunError
    global errorframe
    global errorOut
    
    
    
    if canrunError:
        errorframe.destroy()
        errorOut=output
        errorframe=tk.Label(text=output, fg="red")
        errorframe.grid(row=6, column=1, columnspan=4)
        print(f"[bold red]{errorOut}")
        
        
        
    else:
        errorframe=tk.Label(text=output, fg="red")
        errorframe.grid(row=6, column=1, columnspan=4)
        print(f"[bold red]{errorOut}")
        canrunError=True
        
errorMessage("")





rowB = 2

for x in range(9):
    column=(x % 3)+1
        
    btn = tk.Button(master=root, text=x+1, command=lambda i=x+1: button_function(i))
    btn.grid(column=column,row=rowB)
    #print("printed button with label",x+1," in the position", (row, column))

    #this comes last: \/
    if column == 3:
        rowB += 1






zero=tk.Button(text="0", master=root, command=lambda: button_function(0))
zero.grid(column=1, row=5)

dot=tk.Button(text=".", master=root, command=lambda: button_function("."))
dot.grid(column=2, row=5)

go=tk.Button(text="=", background="blue", master=root, command=lambda: button_function("="))
go.grid(column=3, row=5)






def sendOperators():
    global specialKeyIcons
    global specialKeyOutput
    out = "".join(specialKeyIcons)
    outPuts = "".join(specialKeyOutput)
    time=len(out)        
    for x in range(time):
        b=tk.Button(text=out[x], command=lambda i=x: button_function((outPuts[i])))
        b.grid(column=4, row=x+1)

sendOperators()




def afterclose():
    print("\n\n[purple]Was terminated by close button")
    if screenout=="":
        print(f"[purple]Screenout blank (this is a problem)")
    else:
        print(f"[purple]Screenout at [bold purple]{screenout}\n")



root.resizable(False, False)

root.mainloop()

afterclose()