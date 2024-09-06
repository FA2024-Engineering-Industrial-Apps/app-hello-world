from ieappgenerator.ieappgenerator import IEAppGenerator
from ieappgenerator.llm.ollama import Ollama
from ieappgenerator.llm.siemens import SiemensLLM

def main():
    def on_question_asked(question : str) -> str:
        if question:
            print(f"IE App Generator: {question} (Multiline input is activated. Press enter and Ctrl-D to send.)")    
        else:
            print("(Multiline input is activated. Press enter and Ctrl-D to send.)")
        print("\nYou: ", end='')
        response: str = ''
        while True:
            try:
                line = input()
            except EOFError:
                break
            response += line + '\n'
        return response
    
    def display_response(response : str) -> None:
        print(f"\nIE App Generator: {response}", end='')
        
    with open('siemens-api-key.txt') as f:
        siemens_api_key = f.readline()

    #ie_app_generator = IEAppGenerator(on_question_asked, display_response, Ollama("localhost:11434", "gemma2:2b"))
    ie_app_generator = IEAppGenerator(on_question_asked, display_response, SiemensLLM("mistral-7b-instruct", siemens_api_key))
    ie_app_generator.start()

if __name__ == "__main__":
    main()