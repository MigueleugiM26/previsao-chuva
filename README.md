# Previsão de Chuva — Recife, PE

Interface web local que mostra a previsão de chuva para Recife (bairro do
Cavaleiro) usando um modelo Random Forest treinado com dados históricos do
Open-Meteo.

A página busca os dados meteorológicos de hoje e de ontem diretamente da API
do Open-Meteo, envia ao backend local, e exibe a probabilidade de chuva para
**hoje** e para **amanhã**.

---

## Requisitos

- **Python 3.9+** ([download](https://www.python.org/downloads/))
- Conexão com a internet (para buscar os dados do Open-Meteo)

Para verificar se o Python está instalado:

```bash
python3 --version
```

No Windows, use `python --version`.

---

## Como usar

### 1. Clone o repositório

```bash
git clone https://github.com/MigueleugiM26/previsao-chuva.git
cd previsao-chuva
```

### 2. Crie um ambiente virtual (recomendado)

**Linux / macOS:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows (PowerShell):**

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**Windows (cmd):**

```cmd
python -m venv .venv
.venv\Scripts\activate.bat
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Rode o servidor

```bash
python app.py
```

Você verá algo assim:

```
Previsão de Chuva — Recife
Servidor rodando em http://localhost:8000
Pressione Ctrl+C para encerrar.
```

O navegador abrirá automaticamente em `http://localhost:8000`. Se não abrir,
acesse manualmente.

Para encerrar, pressione `Ctrl+C` no terminal.

---

## Alternativa: modo linha de comando

Se você só quer a previsão rápida no terminal, sem interface gráfica:

```bash
python main.py
```

Saída de exemplo:

```
Previsão de chuva para amanhã: 83.0%
Previsão: 🌧 Chuva
```

---

## Estrutura do projeto

```
previsao-chuva-api/
├── app.py                 # Backend Flask (serve a página + API /predict)
├── main.py                # Alternativa CLI
├── index.html             # Interface web
├── requirements.txt
├── model/
│   └── rain_model.pkl     # Modelo Random Forest treinado
├── data/                  # CSVs usados no treinamento
└── notebooks/             # Notebooks de exploração e treino
```

---

## Como funciona

1. O navegador carrega `index.html` a partir do servidor Flask local.
2. O JavaScript busca os dados de hoje e de ontem na API pública do
   [Open-Meteo](https://open-meteo.com/).
3. Os dados são enviados via `POST` para `http://localhost:8000/predict`.
4. O Flask carrega o `rain_model.pkl`, monta o vetor de features na ordem
   correta e chama `predict_proba()` do modelo.
5. A resposta (`{probability, prediction}`) volta para o navegador, que
   renderiza os cartões de "hoje" e "amanhã".

A porta padrão é `8000`. Para usar outra, defina a variável de ambiente
`PORT`:

```bash
PORT=9000 python app.py
```

E ajuste a URL no `index.html` (`callSpace`) de acordo.

---

## Solução de problemas

**`ModuleNotFoundError: No module named 'flask'`**
→ O ambiente virtual não está ativado, ou as dependências não foram
instaladas. Rode `pip install -r requirements.txt`.

**`FileNotFoundError: Model not found at .../model/rain_model.pkl`**
→ O arquivo do modelo está faltando. Verifique se `model/rain_model.pkl`
existe no repositório clonado.

**Porta 8000 já em uso**
→ Outro programa está usando a porta. Rode com `PORT=9000 python app.py` e
ajuste a URL no `index.html`.

**O navegador não abre sozinho**
→ Acesse manualmente `http://localhost:8000`.

**A página mostra "erro ao carregar dados"**
→ Verifique a conexão com a internet. A API do Open-Meteo pode estar
temporariamente fora do ar.

---

## Licença

Uso pessoal / educacional. Os dados meteorológicos pertencem ao
[Open-Meteo](https://open-meteo.com/).
