from analysis_engine import BurnoutAnalyzer

# Create the analyzer (loads the AI model)
print("Creating analyzer...")
analyzer = BurnoutAnalyzer()

# Test 1: Stressed entry
print("\n--- Test 1: Stressed Entry ---")
result = analyzer.analyze(
    text="I am so exhausted from work. Back to back meetings all day and I couldn't even eat lunch.",
    activities=["Overtime Work", "Skipped Meals"],
    sleep_hours=5,
    stress_level=8
)
print(f"Burnout Score: {result['burnout_score']}")
print(f"Risk Level: {result['risk_level']}")
print(f"Emotions: {result['emotions']}")
print(f"Recommendations: {result['recommendations']}")

# Test 2: Happy entry
print("\n--- Test 2: Happy Entry ---")
result = analyzer.analyze(
    text="Had a great day! Went for a walk in the park and spent time with friends.",
    activities=["Exercise", "Socializing", "Nature Walk"],
    sleep_hours=8,
    stress_level=2
)
print(f"Burnout Score: {result['burnout_score']}")
print(f"Risk Level: {result['risk_level']}")
print(f"Emotions: {result['emotions']}")
print(f"Recommendations: {result['recommendations']}")