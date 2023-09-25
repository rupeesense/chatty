import os

# import your OpenAI key
OPENAI_API_KEY = "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"
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

from langchain.agents import Tool
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain.vectorstores import Chroma
from langchain.llms import OpenAI

user_info = '''

For account: accountA total savings are 316896.4896081795 rupees. 
For account: accountA initial balance was 30000 rupees. 
For account: accountA savings records for each monther after the initial date was are: 
Savings delta for 2023-09-19 is 27874.467807902125 rupees. 
 Savings income ratio for 2023-09-19 is 0.4329080586329377 rupees. 
 Savings rate for 2023-09-19 is 0.9291489269300708 rupees.
Savings delta for 2023-08-20 is 25208.739596901843 rupees. 
 Savings income ratio for 2023-08-20 is 0.33546244887267485 rupees. 
 Savings rate for 2023-08-20 is 0.4355761798203502 rupees.
Savings delta for 2023-07-21 is 19951.215797253855 rupees. 
 Savings income ratio for 2023-07-21 is 0.27978204820182134 rupees. 
 Savings rate for 2023-07-21 is 0.2401353585213208 rupees.
Savings delta for 2023-06-21 is 26646.703176465362 rupees. 
 Savings income ratio for 2023-06-21 is 0.5020247691687931 rupees. 
 Savings rate for 2023-06-21 is 0.25861942395901305 rupees.
Savings delta for 2023-05-22 is 36632.32789493151 rupees. 
 Savings income ratio for 2023-05-22 is 0.3679179068036337 rupees. 
 Savings rate for 2023-05-22 is 0.2824800255667604 rupees.
Savings delta for 2023-04-22 is 38526.51280576158 rupees. 
 Savings income ratio for 2023-04-22 is 0.5014192624126544 rupees. 
 Savings rate for 2023-04-22 is 0.23165000675420883 rupees.
Savings delta for 2023-03-23 is 31754.77900702117 rupees. 
 Savings income ratio for 2023-03-23 is 0.45757419964674195 rupees. 
 Savings rate for 2023-03-23 is 0.15502237898105536 rupees.
Savings delta for 2023-02-21 is 38391.641570902735 rupees. 
 Savings income ratio for 2023-02-21 is 0.38969075892233274 rupees. 
 Savings rate for 2023-02-21 is 0.16226751525965502 rupees.
Savings delta for 2023-01-22 is 41910.10195103933 rupees. 
 Savings income ratio for 2023-01-22 is 0.49685300909632707 rupees. 
 Savings rate for 2023-01-22 is 0.15240791483574775 rupees.


For account: accountB total savings are 334055.4814943724 rupees. 
For account: accountB initial balance was 30000 rupees. 
For account: accountB savings records for each monther after the initial date was are: 
Savings delta for 2023-09-19 is 43591.50999648664 rupees. 
 Savings income ratio for 2023-09-19 is 0.47554255066288936 rupees. 
 Savings rate for 2023-09-19 is 1.4530503332162212 rupees.
Savings delta for 2023-08-20 is 37546.86892305153 rupees. 
 Savings income ratio for 2023-08-20 is 0.7359868381571064 rupees. 
 Savings rate for 2023-08-20 is 0.5102065295962003 rupees.
Savings delta for 2023-07-21 is 15007.792945252948 rupees. 
 Savings income ratio for 2023-07-21 is 0.16244524848813877 rupees. 
 Savings rate for 2023-07-21 is 0.13503699704058372 rupees.
Savings delta for 2023-06-21 is 35347.413434278584 rupees. 
 Savings income ratio for 2023-06-21 is 0.5769488773398074 rupees. 
 Savings rate for 2023-06-21 is 0.28020995731971526 rupees.
Savings delta for 2023-05-22 is 30519.978069673256 rupees. 
 Savings income ratio for 2023-05-22 is 0.42840896231218323 rupees. 
 Savings rate for 2023-05-22 is 0.18898569880130756 rupees.
Savings delta for 2023-04-22 is 37389.530065399566 rupees. 
 Savings income ratio for 2023-04-22 is 0.5524608343135033 rupees. 
 Savings rate for 2023-04-22 is 0.19472338000205064 rupees.
Savings delta for 2023-03-23 is 42903.373456196976 rupees. 
 Savings income ratio for 2023-03-23 is 0.8052428023410851 rupees. 
 Savings rate for 2023-03-23 is 0.1870217738302372 rupees.
Savings delta for 2023-02-21 is 25111.18748214408 rupees. 
 Savings income ratio for 2023-02-21 is 0.40601558602561105 rupees. 
 Savings rate for 2023-02-21 is 0.09221664020288069 rupees.
Savings delta for 2023-01-22 is 36637.827121888826 rupees. 
 Savings income ratio for 2023-01-22 is 0.5542059220070493 rupees. 
 Savings rate for 2023-01-22 is 0.12318645710252253 rupees.


For account: accountC total savings are 318278.29940055945 rupees. 
For account: accountC initial balance was 30000 rupees. 
For account: accountC savings records for each monther after the initial date was are: 
Savings delta for 2023-09-19 is 36210.49514374108 rupees. 
 Savings income ratio for 2023-09-19 is 0.4023743560936425 rupees. 
 Savings rate for 2023-09-19 is 1.2070165047913692 rupees.
Savings delta for 2023-08-20 is 18453.442467412933 rupees. 
 Savings income ratio for 2023-08-20 is 0.19639148659966182 rupees. 
 Savings rate for 2023-08-20 is 0.27870872174193895 rupees.
Savings delta for 2023-07-21 is 29078.320336765108 rupees. 
 Savings income ratio for 2023-07-21 is 0.30688158840323715 rupees. 
 Savings rate for 2023-07-21 is 0.34345579897685025 rupees.
Savings delta for 2023-06-21 is 27292.720702617138 rupees. 
 Savings income ratio for 2023-06-21 is 0.35367451160037155 rupees. 
 Savings rate for 2023-06-21 is 0.23995233781198597 rupees.
Savings delta for 2023-05-22 is 16614.91189845765 rupees. 
 Savings income ratio for 2023-05-22 is 0.2864452919101598 rupees. 
 Savings rate for 2023-05-22 is 0.11780702955702169 rupees.
Savings delta for 2023-04-22 is 35878.69929636176 rupees. 
 Savings income ratio for 2023-04-22 is 0.38586846325137364 rupees. 
 Savings rate for 2023-04-22 is 0.2275846762177833 rupees.
Savings delta for 2023-03-23 is 39846.237700729886 rupees. 
 Savings income ratio for 2023-03-23 is 0.7166253757392603 rupees. 
 Savings rate for 2023-03-23 is 0.20589328807991683 rupees.
Savings delta for 2023-02-21 is 42282.680825195115 rupees. 
 Savings income ratio for 2023-02-21 is 0.7066613930072382 rupees. 
 Savings rate for 2023-02-21 is 0.18117926971727644 rupees.
Savings delta for 2023-01-22 is 42620.791029278786 rupees. 
 Savings income ratio for 2023-01-22 is 0.43758003602542606 rupees. 
 Savings rate for 2023-01-22 is 0.1546150194895951 rupees.

'''


# Set up knowledge base
def setup_knowledge_base(product_catalog: str = None):
    """
    We assume that the product knowledge base is simply a text file.
    """
    # load product catalog
    product_catalog = user_info

    text_splitter = CharacterTextSplitter(chunk_size=1500, chunk_overlap=200)
    texts = text_splitter.split_text(product_catalog)

    llm = OpenAI(temperature=0)
    embeddings = OpenAIEmbeddings()
    docsearch = Chroma.from_texts(
        texts, embeddings, collection_name="user-account-savings-knowledge-base"
    )

    knowledge_base = RetrievalQA.from_chain_type(
        llm=llm, chain_type="stuff", retriever=docsearch.as_retriever()
    )
    return knowledge_base


def get_tools(product_catalog):
    # query to get_tools can be used to be embedded and relevant tools found
    # see here: https://langchain-langchain.vercel.app/docs/use_cases/agents/custom_agent_with_plugin_retrieval#tool-retriever

    # we only use one tool for now, but this is highly extensible!
    knowledge_base = setup_knowledge_base(product_catalog)
    tools = [
        Tool(
            name="ProductSearch",
            func=knowledge_base.run,
            description="useful for when you need to answer questions about product information",
        )
    ]

    return tools


if __name__ == '__main__':
    print(len(user_info))
    knowledge_base = setup_knowledge_base("sample_product_catalog.txt")
    # print(knowledge_base.run("For how many accounts do you have the data? Can you tell more about it?"))
    SYS_PROMPT = '''
    
    You have to act as a personal finance assistant. You will have context of user financial data regarding their savings.
    If you don't have the answer, you can ask the user to provide more information.
    Today's date is 23rd september 2023.
            
    Now answer the below question:
    
    '''
    print(knowledge_base.run(SYS_PROMPT +
                             "What has been the highest and lowest savings month so far this year across all accounts?"))
