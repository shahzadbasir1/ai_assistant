# assistant.py

from assistant import calculate, web_search, analyze_data, get_weather

def show_menu():
    print("\n===== AI Assistant =====")
    print("1. Calculator")
    print("2. Web Search")
    print("3. Data Analyzer")
    print("4. Weather")
    print("5. Exit")


def handle_calculator():
    expression = input("Enter calculation (e.g., 25 * 4 + 10): ")
    result = calculate(expression)
    print("Result:", result)


def handle_web_search():
    query = input("Enter your search query: ")
    result = web_search(query)
    print("Result:", result)


def handle_data_analyzer():
    data = input("Enter data (e.g., [10, 20, 30]): ")
    operation = input("Enter operation (average, sum, max, min): ")
    result = analyze_data(data, operation)
    print("Result:", result)


def handle_weather():
    city = input("Enter city name: ")
    result = get_weather(city)
    print("Weather:", result)


def main():
    while True:
        show_menu()
        choice = input("Select an option (1-5): ")

        if choice == "1":
            handle_calculator()
        elif choice == "2":
            handle_web_search()
        elif choice == "3":
            handle_data_analyzer()
        elif choice == "4":
            handle_weather()
        elif choice == "5":
            print("Exiting... Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()