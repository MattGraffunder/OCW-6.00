# Problem Set 1 
# Name: Matt Graffunder
# Collaborators: None 
# Time Spent: 1:00

monthsInYear = 12

balance = float(raw_input("Enter the outstanding balance on your credit card: "))
annualInterestRate = float(raw_input("Enter the annual credit card interest rate as a decimal: "))
minimumPaymentRate = float(raw_input("Enter the minimum monthly payment rate as a decimal: "))

monthlyInterestRate = annualInterestRate / 12

totalPaid = 0.0;

for month in range(1,monthsInYear+1):
    minimumPayment = round(balance * minimumPaymentRate, 2)
    interestPaid = round((balance * monthlyInterestRate), 2)
    principlePaid = minimumPayment - interestPaid
    balance -= principlePaid

    totalPaid += minimumPayment

    print "Month: " + str(month)
    print "Minimum monthly payment: " + str(minimumPayment)
    print "Priciple paid: " + str(principlePaid)
    print "Remaining Balence: " + str(balance)
    
    
print 
print "RESULT"
print "Total Amount Paid: " +str(totalPaid)
print "Remaining Balance: " + str(balance)
