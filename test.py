from run_JJ import get_qa_by_GPT

#get_qa_by_GPT('안녕')

while True:
    text_input = input("User: ")
    if text_input == "exit":
        break
    get_qa_by_GPT(text_input)