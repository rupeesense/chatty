# Function to calculate EMI and total interest
def calculate_emi_and_interest(principal, annual_interest_rate, years):
    monthly_interest_rate = annual_interest_rate / (12 * 100)
    months = years * 12
    emi = principal * monthly_interest_rate * ((1 + monthly_interest_rate) ** months) / (
                ((1 + monthly_interest_rate) ** months) - 1)
    total_amount = emi * months
    total_interest = total_amount - principal
    return emi, total_interest


# Main function to process the loan details
def main():
    # Input for total house cost and interest rate
    total_house_cost = float(input("Enter the total house cost: "))
    annual_interest_rate = float(input("Enter the annual interest rate (in %): "))

    # Define down payment percentages and loan tenures
    down_payment_percentages = [20, 25, 30]
    loan_tenures = [10, 15, 20, 30]

    print("\nCalculating EMI and Total Interest for different combinations...\n")

    # Iterate through down payments and tenures, calculate and display results
    for down_payment_percentage in down_payment_percentages:
        for tenure in loan_tenures:
            down_payment = (down_payment_percentage / 100) * total_house_cost
            loan_amount = total_house_cost - down_payment
            emi, total_interest = calculate_emi_and_interest(loan_amount, annual_interest_rate, tenure)

            print(f"Down Payment: {down_payment_percentage}% (₹{down_payment:.2f}), Loan Tenure: {tenure} years")
            print(f"Loan Amount: ₹{loan_amount:.2f}")
            print(f"Monthly EMI: ₹{emi:.2f}")
            print(f"Total Interest Paid: ₹{total_interest:.2f}\n")


# Run the program
if __name__ == "__main__":
    main()
