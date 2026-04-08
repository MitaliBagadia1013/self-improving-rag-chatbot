# # from app.generation.answerer import AnswerGenerator


# # def main():
# #     generator = AnswerGenerator()

# #     query = "What is retrieval augmented generation?"
# #     result = generator.answer_question(query, top_k=5)

# #     print("=" * 100)
# #     print("QUESTION:")
# #     print(result["query"])
# #     print("\nANSWER:")
# #     print(result["answer"])
# #     print("\nRETRIEVED SOURCES:")
# #     for chunk in result["retrieved_chunks"]:
# #         meta = chunk["metadata"]
# #         print(f'- {meta["source"]}, page {meta["page"]}, chunk {meta["chunk_id"]}')


# # if __name__ == "__main__":
# #     main()

# from app.generation.answerer import AnswerGenerator


# def main():
#     generator = AnswerGenerator()

#     query = "What is retrieval augmented generation?"
#     result = generator.answer_question(query, top_k=5)

#     print("=" * 100)
#     print("INTERACTION ID:", result["interaction_id"])
#     print("QUESTION:")
#     print(result["query"])
#     print("\nANSWER:")
#     print(result["answer"])
#     print("\nRETRIEVED SOURCES:")
#     for chunk in result["retrieved_chunks"]:
#         meta = chunk["metadata"]
#         print(f'- {meta["source"]}, page {meta["page"]}, chunk {meta["chunk_id"]}')


# if __name__ == "__main__":
#     main()

from app.generation.answerer import AnswerGenerator


def main():
    generator = AnswerGenerator()

    query = "What is retrieval augmented generation?"
    result = generator.answer_question(query, top_k=5)

    print("=" * 100)
    print("INTERACTION ID:", result["interaction_id"])
    print("QUESTION:")
    print(result["query"])
    print("\nANSWER:")
    print(result["answer"])
    print("\nRETRIEVED SOURCES:")
    for chunk in result["retrieved_chunks"]:
        meta = chunk["metadata"]
        print(f'- {meta["source"]}, page {meta["page"]}, chunk {meta["chunk_id"]}')

    feedback = input("\nEnter feedback label (correct / hallucination / incomplete / bad_retrieval): ").strip()
    comment = input("Optional comment: ").strip()

    generator.log_feedback(
        interaction_id=result["interaction_id"],
        label=feedback,
        comment=comment if comment else None,
    )

    print("Feedback saved successfully.")


if __name__ == "__main__":
    main()