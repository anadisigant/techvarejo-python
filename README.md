# techvarejo-python

Repositório com dados e exemplos para o estudo de caso "TechVarejo S.A." — base para exercícios e demonstrações de análise de dados em Python.

**Pré-requisitos**
- Git
- Python 3.8+ (recomendado 3.10+)
- `pip` (gerenciador de pacotes)
- (opcional) `streamlit` para executar a aplicação interativa

**Como clonar o repositório**

Abra um terminal e execute:

```bash
git clone <URL-DO-REPO>
cd techvarejo-python
```

Substitua `<URL-DO-REPO>` pela URL do repositório (HTTPS ou SSH).

**Criar e ativar um ambiente virtual (recomendado)**

Windows (PowerShell):

```powershell
python -m venv .venv
& .venv\Scripts\Activate.ps1
```

Windows (cmd):

```cmd
python -m venv .venv
.venv\Scripts\activate
```

Linux / macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Instalar dependências**

Com o ambiente ativado, execute:

```bash
pip install -r requirements.txt
```

**Estrutura do repositório**

- `data/` — pasta com arquivos CSV de exemplo:
	- `clientes.csv`
	- `custos_logisticos.csv`
	- `marketing.csv`
	- `produtos.csv`
	- `vendas.csv`
- `app.py` — aplicação interativa (Streamlit)
- `analise.py` — script de análise/relatórios
- `gerador_dados.py` — script para gerar dados de exemplo (preenche `data/`)

**Gerar ou atualizar os dados de exemplo**

Se quiser (re)gerar os CSVs de exemplo, rode:

```bash
python gerador_dados.py
```

Os arquivos gerados serão salvos na pasta `data/`.

**Executar a aplicação (Streamlit)**

Com o ambiente ativado e dependências instaladas, execute:

```bash
streamlit run app.py
```

Abra o navegador no endereço que o Streamlit mostrar (por padrão `http://localhost:8501`).

**Executar o script de análise**

Para rodar o script de análise (gera saídas no terminal ou arquivos, dependendo da implementação):

```bash
python analise.py
```

**Dicas e solução de problemas**
- Se `streamlit` não estiver instalado, instale com `pip install streamlit` ou verifique `requirements.txt`.
- Em Windows PowerShell, se ocorrer erro de execução ao ativar o `.venv`, execute `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` antes de `Activate.ps1`.
- Verifique se os arquivos CSV estão na pasta `data/` caso algum script falhe ao carregar dados.

**Contribuições**
- Para contribuir, abra uma issue descrevendo a sugestão/bug ou envie um Pull Request.

**Contato**
- Dúvidas: abra uma issue no repositório.
