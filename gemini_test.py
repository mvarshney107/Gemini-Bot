import google.generativeai as genai

genai.configure(api_key="GEMINI API KEY")
model = genai.GenerativeModel('gemini-1.5-flash')


def generate(prompt):
    reponse = model.generate_content(prompt)
    return reponse.text


def main():
    user_choice = input("Would you like to ask Gemini something? (y/n)")
    while user_choice.lower() != "n":
        prompt = input("Enter prompt: ")
        print(generate(prompt))
        user_choice = input("Would you like to ask Gemini something else? (y/n)")


if __name__ == "__main__":
    main()