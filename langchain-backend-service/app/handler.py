import json
import os

from openai import AzureOpenAI



class AzureOpenAIHandler:
    def __init__(
        self,
        api_functions,
        function_definitions,
        system_message,
        model="gpt-35-turbo",
    ):

        api_key = os.environ.get("AZURE_OPENAI_API_KEY")
        if api_key is None:
            raise ValueError("AZURE_OPENAI_API_KEY not found in environment variables.")
        
        self.client = AzureOpenAI(
            azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT"), 
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),  
            api_version="2023-05-15"
        )
        self.api_functions = api_functions
        self.function_definitions = function_definitions
        self.model = model
        self.system_message = system_message

    def send_message(self, query):
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": self.system_message,
                },
                {"role": "user", "content": query},
            ],
            functions=self.function_definitions,
        )
        message = response.choices[0].message
        return message

    def process_function_call(self, message):
        if message.function_call:
            print(message.function_call)
            function_name = message.function_call.name
            function_args_json = message.function_call.arguments
            function_args = json.loads(function_args_json)

            api_function = self.api_functions.get(function_name)

            if api_function:
                result = str(api_function(**function_args))
                return function_name, result
            else:
                print(f"Function {function_name} not found")
        return None, None

    def send_response(self, query):
        message = self.send_message(query)
        function_name, result = self.process_function_call(message)

        if function_name and result:
            print("Function call necessary to fulfill users request")
            second_response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": self.system_message,
                    },
                    {"role": "user", "content": query},
                    message,
                    {
                        "role": "function",
                        "name": function_name,
                        "content": result,
                    },
                ],
            )
            return second_response.choices[0].message.content
        else:
            return message.content
