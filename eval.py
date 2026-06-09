from retriever import retrieve

# A list of test cases: (Question, Expected Game)
TEST_CASES = [
    ("What happens when you roll a 7?", "Catan"),
    ("How do you get out of Jail?", "Monopoly"),
    ("What happens when you run out of disease cubes?", "Pandemic"),
    ("What is the penalty for forgetting to yell UNO?", "Uno"),
    ("How many points do you need to win?", "Uno") 
]

def run_eval():
    print("==========================================")
    print("🤖 Running Retrieval Evaluation Agent...")
    print("==========================================\n")
    
    correct = 0
    total = len(TEST_CASES)

    for query, expected_game in TEST_CASES:
        print(f"Q: {query}")
        
        # Retrieve top 3 results
        results = retrieve(query, n_results=3)
        
        # Extract the game names from the retrieved chunks
        retrieved_games = [chunk["game"] for chunk in results]
        
        # Check if the expected game is in our top results
        if expected_game in retrieved_games:
            print(f"✅ PASS: Found {expected_game} in top results. (Got: {retrieved_games})")
            correct += 1
        else:
            print(f"❌ FAIL: Expected {expected_game}, but got {retrieved_games}")
        print("-" * 40)

    # Calculate and print final accuracy
    accuracy = (correct / total) * 100
    print(f"\nFinal Score: {correct}/{total} ({accuracy:.1f}% Accuracy)")

if __name__ == "__main__":
    run_eval()