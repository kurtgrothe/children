import random
import time
import pandas as pd
import pickle

# Open results file if not found create a new one
try:
    with open("addition_results.pkl", "rb") as f:
        addition_results = pickle.load(f)
    print("File loaded successfully.")
except FileNotFoundError:
    print("File not found. Creating a new one.")
    addition_results = pd.DataFrame(columns=["Date", "Question", "Wrong", "Question_time", "Total_time"])

# Create random numbers for addition (1-9 and 1-10) to keep it below 20
number1 = random.randint(1, 10)
number2 = random.randint(1, 9)

# Initialize variables
number_of_questions = 60

# DataFrame variables
date = time.strftime("%Y-%m-%d %H:%M", time.localtime())
correct = 0
wrong = 0
question_time_average = 0
total_time = 0

# Intermediate variables
question_time_start = 0
question_time_end = 0
question_time = []
total_time_start = time.time()
total_time_end = 0

# Loop through questions
i = 1
while i <= number_of_questions:
    print("Question", i)
    print(number1, "+", number2, "=")
    question_time_start = time.time()
    try:
        answer = int(input())
        question_time_end = time.time()
        
        if answer < 1:
            break
        
        if answer == number1 + number2:
            print("Correct!\n")
            correct += 1
            wrong_flag = 0
        else:
            print(f"******  Try again. The correct answer is {number1 + number2}  ******\n")
            wrong += 1
            wrong_flag = 1

        # Calculate question time
        question_time.append((question_time_end - question_time_start))
        
        # Append results to the DataFrame
        new_result = pd.DataFrame([{
            "Date": date,
            "Question": f"{number1} + {number2}",
            "Wrong": wrong_flag,
            "Question_time": round(question_time_end - question_time_start, 2),
            "Total_time": round(question_time_end - total_time_start, 2)
        }])
        addition_results = pd.concat([addition_results, new_result], ignore_index=True)

        i += 1
        
    except ValueError:
        print("Enter a number. Try again.\n")
        
    number1 = random.randint(1, 10)
    number2 = random.randint(1, 9)

# Calculate results
if question_time:  # Avoid division by zero
    question_time_average = round(sum(question_time) / len(question_time), 2)
total_time_end = time.time()
total_time = round(total_time_end - total_time_start, 2)
percentage_correct = round(correct / (correct + wrong) * 100, 1) if correct + wrong > 0 else 0

# Print results
print("\n\n")
print(30 * "#")
print("Correct:", correct)
print("Incorrect:", wrong)
print(f"Percentage correct: {percentage_correct}%")
print("Average question time:", question_time_average)
print("Total time:", total_time)
print(30 * "#")

# Append summary results to the DataFrame
summary_result = pd.DataFrame([{
    "Date": date,
    "Question": "Summary",
    "Wrong": wrong,
    "Question_time": question_time_average,
    "Total_time": total_time
}])

addition_results = pd.concat([addition_results, summary_result], ignore_index=True)

# Save results to the file
addition_results.to_pickle("addition_results.pkl")
print("DataFrame saved to addition_results.pkl.")
