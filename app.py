import os
import typer
import openai
import subprocess
from pathlib import Path

app = typer.Typer()
openai.api_key = ""
#openai.api_key = os.environ['OPENAI_API_KEY']

list = []

def request_chat(prompt):
    system_content = "quero que atue como um transpilador de uma linguagem com sintaxe em portugues estruturado para código python executável na versão 3.8, quando receber um prompt neste codigo de linguagem com sintaxe em portugues, faça a conversão para um script python. não explique o código, apenas responda com o codigo python transpilado"
    list = [
        {"role": "system", "content": system_content},
        {"role":"user", "content":"função principal() \n imprima(soma(2,2)) \n fim \n função soma(a,b) \n return a + b \n fim"},
        {"role": "assistant", "content": "def soma(a, b):\n    return a + b\n\nprint(soma(2,2))"}
        ]

    list.append({"role": "user", "content": prompt})

    result = openai.ChatCompletion.create(model="gpt-3.5-turbo",
                                          messages=list)

    item = result["choices"][0]["message"]
    resp = result["choices"][0]["message"]["content"]

    return resp

@app.command()
def compile(filename: str):  
    file_content = Path(filename).read_text()
    pycode = request_chat(file_content)
    filename_no_ext, ext = os.path.splitext(filename)
    with open(filename_no_ext + ".py", 'w') as f:
        f.write(pycode)

@app.command()
def run(filename: str):  
    file_content = Path(filename).read_text()
    pycode = request_chat(file_content)
    filename_no_ext, ext = os.path.splitext(filename)
    with open(filename_no_ext + ".py", 'w') as f:
       f.write(pycode)
    subprocess.run(["python", filename_no_ext + ".py"])
  

if __name__ == "__main__":
    app()