# Problem Set 1 
# Name: Matt Graffunder
# Collaborators: None 
# Time Spent: 1:00

monthsInYear = 12

balance = float(raw_input("Enter the outstanding balance on your credit card: "))
annualInterestRate = float(raw_input("Enter the annual credit card interest rate as a decimal: "))

monthlyInterestRate = annualInterestRate / 12

monthsNeeded = 0
paymentAmount = 0
testBalance = balance

paymentAmountLowerBound = balance/12
paymentAmountUpperBound = (balance * (1 + monthlyInterestRate) **12)/12

while (testBalance < -.12 or testBalance > 0) and paymentAmountLowerBound != paymentAmountUpperBound:
    testBalance = balance
    paymentAmount = round((paymentAmountLowerBound + paymentAmountUpperBound) / 2, 2)
    
    for month in range(1,monthsInYear+1):
        testBalance = round(testBalance*(1+monthlyInterestRate) - paymentAmount,2)

        if testBalance <= 0:
            monthsNeeded = month
            break
        
    if testBalance > 0:
        #Didn't payoff Loan, set lower bound to current payment amount
        paymentAmountLowerBound = paymentAmount
    elif testBalance < 0:
        #Paid off too much, set upper bound to current payment amount
        paymentAmountUpperBound = paymentAmount

print 
print "RESULT"
print "Monthly payment to pay off debt in 1 year: " +str(paymentAmount)
print "Number of Months needed: " + str(monthsNeeded)
print "Remaining Balance: " + str(testBalance)
