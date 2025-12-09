from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv
load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")
print(groq_api_key, 'is the api key')

model = ChatGroq(
    api_key = groq_api_key,
    model= "llama-3.1-8b-instant",
    temperature= 0.1,
    max_tokens=512
)

def generate_llm_response(query_results, user_query):
    
    # context = type(query_results[1]) # list containing 3 tuples
    # print(context, 'is the final context')
    
    # print(type(query_results[0][1]))
    context = query_results[0]["document"]
    print(context)

    final_code_context = "\n\n".join(doc["document"] for doc in query_results)
        
    
    prompt = f"""
	You are a code analysis assistant.
	
	User question:
	{user_query}

	Relevant repository code:
	{final_code_context}

	Answer the question based ONLY on the above code context.
	If the answer is not found in the code, reply:
	"Not found in repository code. Please ask a relevant question."
	"""
        
    response = model.invoke(prompt)
    return response