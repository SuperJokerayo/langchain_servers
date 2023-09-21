from __future__ import annotations

from typing import Mapping, List

from langchain.schema.document import Document

import copy

class Prompt:
    def __init__(self, template: str) -> None:
        self.template = template

    def generate_prompt_from_str(self, variables: Mapping[str, str]) -> str:
        prompt = copy.deepcopy(self.template)

        for key in variables.keys():
            if prompt.find('{' + key + '}') == -1:
                raise "Error input variables"
            prompt = prompt.replace('{' + key + '}', variables[key])
        return prompt

    def generate_prompt_from_docs(
        self, 
        top_k: int,       
        docs_variables: Mapping[str, List[langchain.schema.document.Document]], 
        query_variables: Mapping[str, str]
    ):
        
        variables = query_variables
        for key in docs_variables.keys():
            if key in query_variables.keys():
                raise "Error input variables"
            content = ""
            for i in range(min(top_k, len(docs_variables[key]))):
                content += f"{i + 1}. " + docs_variables[key][i].page_content.replace("\n", " ") + "\n"
            variables[key] = content
        print(variables)
        return self.generate_prompt_from_str(variables)

        

            