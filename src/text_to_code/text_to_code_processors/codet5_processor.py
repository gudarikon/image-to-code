from transformers import T5Config, RobertaTokenizer, T5ForConditionalGeneration

from .text_to_code_processor import TextToCodeProcessor
from src.text_to_code.data_processors import CodeT5DataProcessor
from src import ABCSingleton


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
        self._model = T5ForConditionalGeneration.from_pretrained(kwargs["model_bin_path"], config=config)
        self._processor = CodeT5DataProcessor()

    def predict(self, text: str, max_length: str = -1) -> str:
        """
        Predict fixed code from text
        :param text: input text
        :param max_length: max tokens in output (-1 to not specify)
        :return: fixed code
        """
        text = self._processor.process(text)
        input_ids = self._tokenizer(text, return_tensors="pt").input_ids
        if max_length == -1:
            max_length = len(input_ids[0])
        generated_ids = self._model.generate(input_ids, max_length=max_length)
        return self._tokenizer.decode(generated_ids[0], skip_special_tokens=True)