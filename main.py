from llm.rag_chain import ask_legal_question

while True:

    question = input("\nAsk Legal Question: ")

    answer = ask_legal_question(question)

    print("\nAnswer:")
    print(answer)