from typing import Callable
from .llm.llm import LLM

class IEAppGenerator:
    """
    A class to represent an interactive application generator that uses an LLM (Large Language Model) 
    to process user inputs and generate responses.
    """
    
    def __init__(self, on_question_asked : Callable[[str], str], display_response : Callable[[str],None], llm : LLM) -> None:
        """
        Initializes an IEAppGenerator instance.

        Args:
            on_question_asked (Callable[[str], str]): A callable function to ask the user a question and return the user's response.
            display_response (Callable[[str], None]): A callable function to display the LLM's response to the user.
            llm (LLM): An instance of the LLM class to process the user's input and generate responses.
        """
        self._ask_question: Callable[[str], str] = on_question_asked
        self._display_response: Callable[[str], None] = display_response
        self._llm = llm
    
    def start(self) -> None:
        """
        Starts the interactive application. 

        This method continuously prompts the user for input, processes the input using the LLM, and 
        displays the LLM's response. The loop terminates when the user enters 'exit', 'quit', or 'stop'.

        The method will adjust the prompt based on whether the LLM's response ends with a question mark.
        """
        user_input: str = self._ask_question("What can I do for you today?")
        while user_input.strip().lower() not in ['exit', 'quit', 'stop']:
            llm_response = self._llm.process_prompt(user_input)
            self._display_response(llm_response)
            
            if '?' in llm_response:
                user_input = self._ask_question('')
            else:
                user_input = self._ask_question("Anything else I can do for you?")