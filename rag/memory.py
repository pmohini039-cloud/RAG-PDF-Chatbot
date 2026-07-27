from langchain.memory import ConversationBufferMemory


def get_memory():
    """
    Creates a conversation memory object.
    Stores previous user and AI messages.
    """

    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True,
        output_key="answer",
    )

    return memory