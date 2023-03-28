import re
from typing import List, Union

from transformers import RobertaTokenizer, T5Config, T5ForConditionalGeneration

from src import ABCSingleton, get_project_path, unify_path
from src.text_to_code.data_processors import CodeT5DataProcessor
from .text_to_code_processor import TextToCodeProcessor


class CodeT5Processor(TextToCodeProcessor, metaclass=ABCSingleton):
    def __init__(self, **kwargs):
        """
        You can download model from:
        https://drive.google.com/file/d/19Sb_aMCi-XIBrjqlDiGpYOwG7MmCpWnj/view
        :param model_bin_path: local path to binary model file
        """
        assert kwargs.get("model_bin_path", "") != "", "CodeT5Processor should get `model_bin_path` argument with" \
                                                       " path to model's bin file "
        self._tokenizer = RobertaTokenizer.from_pretrained('Salesforce/codet5-small')
        config = T5Config.from_pretrained('Salesforce/codet5-small')
        model_path = get_project_path() / unify_path(kwargs["model_bin_path"])

        self._model = T5ForConditionalGeneration.from_pretrained(str(model_path), config=config)
        self._processor = CodeT5DataProcessor()

    def predict(self, text: Union[str, List[str]], extra_length=5, **kwargs) -> str:
        """
        Predict fixed code from text
        :param text: input text
        :param extra_length: how many extra tokens to generate
            (5 found by researches and is a 0.975 quantile)

        :return: fixed code
        """
        spaces = [re.findall(r'^\s*', line)[0] for line in text.split("\n")]

        text = self._processor.process(text)
        input_ids = self._tokenizer(text, return_tensors="pt").input_ids
        max_length = len(input_ids[0]) + extra_length
        generated_ids = self._model.generate(input_ids, max_length=max_length)

        text = self._tokenizer.decode(generated_ids[0], skip_special_tokens=True)

        parsed_text_with_spaces = []
        for i, line in enumerate(text.split("\n")):
            new_line = line if i >= len(spaces) else spaces[i] + line
            parsed_text_with_spaces.append(new_line)
        return "\n".join(parsed_text_with_spaces)
