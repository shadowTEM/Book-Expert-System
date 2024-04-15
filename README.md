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

