<h2> Step One </h2>
Put all your files on a colab enviroment or local enviroment

<h2> Step Two </h2>
Put your hugging face api key as follows 
HUGGINGFACEHUB_API_TOKEN="Api key"
in a .env file

<h2> Step Three </h2>
run the notebook  <br>
and get the ip address from <br>
!wget -q -O - ipv4.icanhazip.com <br>
put the output of this command into the last link from the command  <br>
!streamlit run appV2.py & npx localtunnel --port 8501 <br>


<h2>Step Four</h2>
this will open the streamlit website <br>
choose a book and ask away in the chat <br>



<h2> configuration </h2>
<h3>if you want to add a new pdf add </h3>

pdf_docs = get_pdf_splits(folder path)<br>
embed_index(doc_list=pdf_docs,<br>
             embed_fn=embeddings,<br>
            index_store='new index')<br>

if you want to change the LLM <br>
you have to go to appV2 and go to get_conversation_chain(vectorstore) function <br>

