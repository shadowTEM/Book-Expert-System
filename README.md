<h1> Step One </h1>
Put all your files on a colab enviroment or local enviroment

<h1> Step Two </h1>
Put your hugging face api key as follows 
HUGGINGFACEHUB_API_TOKEN="Api key"
in a .env file

<h1> Step Three </h1>
run the notebook  <br>
and get the ip address from <br>
!wget -q -O - ipv4.icanhazip.com <br>
put the output of this command into the last link from the command  <br>
!streamlit run appV2.py & npx localtunnel --port 8501 <br>


<h1>Step Four</h1>
this will open the streamlit website <br>
choose a book and ask away in the chat <br>



<h1> configuration </h1>
<h3>if you want to add a new pdf add </h3>

pdf_docs = get_pdf_splits(folder path)<br>
embed_index(doc_list=pdf_docs,<br>
             embed_fn=embeddings,<br>
            index_store='new index')<br>

if you want to change the LLM <br>
you have to go to appV2 and go to get_conversation_chain(vectorstore) function <br>

