import torch
import json
import scrapper_flipkart
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline, BitsAndBytesConfig

model_name = "notBeastKing/Llama3_sentiment_analysis"
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type= "nf4",
    bnb_4bit_use_double_quant=True,
    bnb_4bit_compute_dtype=torch.bfloat16
)

config_data = json.load(open("config.json"))
HF_TOKEN = config_data["HF_TOKEN"]

tokenizer = AutoTokenizer.from_pretrained(model_name,
                                          token = HF_TOKEN)
tokenizer.pad_token = tokenizer.eos_token

model = AutoModelForCausalLM.from_pretrained(
    model_name,
    device_map="auto",
    quantization_config = bnb_config,
    token = HF_TOKEN
)

reviews = scrapper_flipkart.Scrape("https://www.flipkart.com/apple-iphone-14-plus-blue-128-gb/p/itmac8385391b02b?pid=MOBGHWFHUYWGB5F2&lid=LSTMOBGHWFHUYWGB5F2XIJVA7&marketplace=FLIPKART&q=iphone&store=tyy%2F4io&srno=s_1_1&otracker=search&otracker1=search&fm=organic&iid=a74bd35b-b4b3-4139-b29f-ad85737d640f.MOBGHWFHUYWGB5F2.SEARCH&ppt=hp&ppn=homepage&ssid=hum80i4c9y8wekn41719848468572&qH=0b3f45b266a97d70")
negative =  0
positive = 0
xbox_prompt = """

### Instruction:
{}

### Input:
{}

### Response:
{}"""


pipe = pipeline(task="text-generation", model=model, tokenizer=tokenizer, max_length=500)

for reivew in reviews:
    prompt = xbox_prompt.format(
        'Recognize the overall sentiment of the given review as input. Determine the overall sentiment from the options ["positive", "negative","neutral"]. Answer without any explanation.',

        f"""{reivew}""",

        "", 
    )
    result = pipe(prompt,stop_sequence="### Instruction:")
    output = result[0]["generated_text"].split("###")
    response = output[-2].split(":")[-1]
    if response == "positive":
        positive += 1
    else:
        negative += 1

if positive > negative:
    print("good product")
else:
    print("bad product")