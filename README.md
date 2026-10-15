<div align="center">

# 🤖 Curso API de Claude

**Aprende a usar la API de Claude con Python, paso a paso:<br>desde tu primera petición hasta herramientas, imágenes, PDFs, búsqueda semántica y servidores MCP.**

<br>

<img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.10+">
<img src="https://img.shields.io/badge/Claude-API-D97757?style=for-the-badge&logo=anthropic&logoColor=white" alt="Claude API">
<img src="https://img.shields.io/badge/Voyage_AI-Embeddings-5B5BD6?style=for-the-badge" alt="Voyage AI">
<img src="https://img.shields.io/badge/Jupyter-Notebooks-F37626?style=for-the-badge&logo=jupyter&logoColor=white" alt="Jupyter">

<br><br>

[🔑 Claves](#claves) &nbsp;·&nbsp; [⚙️ Configuración](#configuracion) &nbsp;·&nbsp; [📚 Notebooks](#notebooks) &nbsp;·&nbsp; [🧩 Proyectos](#proyectos) &nbsp;·&nbsp; [🗂️ Estructura](#estructura)

</div>

<br>

<a id="claves"></a>

## 🔑 Antes de empezar: necesitas tus propias API keys

Este repositorio **no incluye ninguna clave**. Para ejecutar los códigos tienes que crear las tuyas:

<table>
<tr>
<td width="50%" valign="top">

### 🟠 Claude

**`ANTHROPIC_API_KEY`**

✅ **Obligatoria**

La usan casi todos los notebooks y el proyecto `cli_project`.

**Cómo obtenerla**
1. Entra a [console.anthropic.com](https://console.anthropic.com)
2. Carga créditos en la sección de facturación
3. Crea tu clave en **API Keys**

</td>
<td width="50%" valign="top">

### 🟣 Voyage AI

**`VOYAGE_API_KEY`**

⬜ **Solo para dos notebooks**

La necesitan `Incrustacion.ipynb` y `Vectorizacion.ipynb`, que generan *embeddings*.

**Cómo obtenerla**
1. Entra a [dashboard.voyageai.com](https://dashboard.voyageai.com)
2. Crea una cuenta
3. Crea tu clave en **API Keys**

</td>
</tr>
</table>

> [!WARNING]
> La API de Claude es **de pago por uso**. La suscripción de Claude.ai (Pro o Max) **no** incluye acceso a la API: los créditos se compran aparte en la consola. Cada celda que llama a Claude gasta créditos, y los modelos `haiku` son los más baratos.

<br>

<a id="configuracion"></a>

## ⚙️ Configuración en 4 pasos

**1️⃣ &nbsp;Clona el repositorio**

```bash
git clone https://github.com/jacob0900/Curso_API_Claude.git
cd Curso_API_Claude
```

**2️⃣ &nbsp;Crea tu archivo `.env` a partir de la plantilla**

```bash
copy .env.example .env      # Windows
cp .env.example .env        # Mac / Linux
```

Ábrelo y pega tus claves:

```ini
ANTHROPIC_API_KEY=sk-ant-...
VOYAGE_API_KEY=pa-...
```

**3️⃣ &nbsp;Instala las dependencias** (Python 3.10 o superior)

```bash
pip install anthropic python-dotenv voyageai jupyter
```

**4️⃣ &nbsp;Abre los notebooks**

```bash
jupyter notebook
```

> [!TIP]
> También puedes abrirlos en VS Code. Para usar otro modelo, cambia la variable `model` al inicio de cada notebook (por ejemplo `claude-haiku-4-5` o `claude-sonnet-4-5`).

<br>

<a id="notebooks"></a>

## 📚 Guía de los notebooks

Están pensados para recorrerse en este orden:

```mermaid
flowchart LR
    A["1 · Primeros pasos"] --> B["2 · Prompts"] --> C["3 · Herramientas"] --> D["4 · Avanzado"] --> E["5 · Búsqueda y RAG"] --> F["6 · Proyectos MCP"]
```

Las casillas de cada tabla indican qué clave necesita el notebook: &nbsp; ✅ la necesita &nbsp;·&nbsp; ⬜ no la necesita

### 1️⃣ Primeros pasos

<table>
<thead>
<tr><th align="left" width="250">📓 Notebook</th><th align="left">¿Qué hace?</th><th width="80">Claude</th><th width="80">Voyage</th></tr>
</thead>
<tbody>
<tr><td><code>Introduccion</code></td><td>Tu primera petición a Claude y una comprobación de que el <code>.env</code> se cargó bien.</td><td align="center">✅</td><td align="center">⬜</td></tr>
<tr><td><code>Ejercicio1</code></td><td>Mini chatbot en consola que recuerda la conversación. Escribe <code>salir</code> para terminar.</td><td align="center">✅</td><td align="center">⬜</td></tr>
<tr><td><code>Ejercicio2</code></td><td>El mismo chatbot con un <i>system prompt</i>: Claude actúa como tutor de matemáticas.</td><td align="center">✅</td><td align="center">⬜</td></tr>
<tr><td><code>TemperaturaDeterministica</code></td><td>Cómo la <code>temperature</code> vuelve las respuestas más consistentes o más variadas.</td><td align="center">✅</td><td align="center">⬜</td></tr>
<tr><td><code>Streming</code></td><td>Respuestas en <i>streaming</i>: el texto aparece mientras Claude lo escribe.</td><td align="center">✅</td><td align="center">⬜</td></tr>
<tr><td><code>Json</code></td><td>Claude responde en JSON estructurado, con explicación, pasos y resultado.</td><td align="center">✅</td><td align="center">⬜</td></tr>
</tbody>
</table>

### 2️⃣ Ingeniería y evaluación de prompts

<table>
<thead>
<tr><th align="left" width="250">📓 Notebook</th><th align="left">¿Qué hace?</th><th width="80">Claude</th><th width="80">Voyage</th></tr>
</thead>
<tbody>
<tr><td><code>CalificacionPromts</code></td><td>Crea casos de prueba (<code>dataset.json</code>) y califica las respuestas de dos formas: con otro modelo y validando la sintaxis (JSON, Python o regex).</td><td align="center">✅</td><td align="center">⬜</td></tr>
<tr><td><code>IngeneriaPromts</code></td><td>Evaluador automático de prompts aplicado a un plan de comidas para atletas. Genera un reporte en <code>output.html</code>.</td><td align="center">✅</td><td align="center">⬜</td></tr>
<tr><td><code>EjercicioIngPromt</code></td><td>El mismo evaluador aplicado a extraer los temas de un artículo académico como lista JSON.</td><td align="center">✅</td><td align="center">⬜</td></tr>
</tbody>
</table>

### 3️⃣ Herramientas (Tool Use)

<table>
<thead>
<tr><th align="left" width="250">📓 Notebook</th><th align="left">¿Qué hace?</th><th width="80">Claude</th><th width="80">Voyage</th></tr>
</thead>
<tbody>
<tr><td><code>Herramientas</code></td><td>Tool use paso a paso y a mano: definir una herramienta, forzarla con <code>tool_choice</code> y devolverle el resultado a Claude.</td><td align="center">✅</td><td align="center">⬜</td></tr>
<tr><td><code>Herramientasv2</code></td><td>Bucle automático en el que Claude usa varias herramientas (fecha actual, sumar tiempo, recordatorios) hasta terminar.</td><td align="center">✅</td><td align="center">⬜</td></tr>
<tr><td><code>LlamadoHerramientas</code></td><td>Herramientas combinadas con <i>streaming</i>, incluido el <i>fine-grained tool streaming</i>.</td><td align="center">✅</td><td align="center">⬜</td></tr>
<tr><td><code>EditorHerramienta</code></td><td>La herramienta de editor de texto de Claude: ver, crear, reemplazar e insertar texto en archivos.<br>⚠️ <b>Puede modificar archivos de la carpeta.</b></td><td align="center">✅</td><td align="center">⬜</td></tr>
<tr><td><code>BisquedaWeb</code></td><td>Claude busca en internet con la herramienta <code>web_search</code>.<br>💲 <b>Debe estar habilitada en la consola y cobra por búsqueda.</b></td><td align="center">✅</td><td align="center">⬜</td></tr>
</tbody>
</table>

### 4️⃣ Funciones avanzadas

<table>
<thead>
<tr><th align="left" width="250">📓 Notebook</th><th align="left">¿Qué hace?</th><th width="80">Claude</th><th width="80">Voyage</th></tr>
</thead>
<tbody>
<tr><td><code>PensamientoExtendido</code></td><td><i>Extended thinking</i>: Claude razona antes de responder, con un presupuesto de tokens.</td><td align="center">✅</td><td align="center">⬜</td></tr>
<tr><td><code>Imagenes</code></td><td>Claude analiza una imagen satelital de <code>images/</code> y evalúa el riesgo de incendio de una propiedad.</td><td align="center">✅</td><td align="center">⬜</td></tr>
<tr><td><code>PDF</code></td><td>Preguntas sobre <code>earth.pdf</code>, con citas a las partes del documento de donde sale cada respuesta.</td><td align="center">✅</td><td align="center">⬜</td></tr>
<tr><td><code>Cache</code></td><td><i>Prompt caching</i>: guarda en caché herramientas y prompts largos para ahorrar costo y tiempo.</td><td align="center">✅</td><td align="center">⬜</td></tr>
</tbody>
</table>

### 5️⃣ Búsqueda y RAG

<table>
<thead>
<tr><th align="left" width="250">📓 Notebook</th><th align="left">¿Qué hace?</th><th width="80">Claude</th><th width="80">Voyage</th></tr>
</thead>
<tbody>
<tr><td><code>chunking</code></td><td>Tres formas de dividir <code>report.md</code> en fragmentos: por caracteres, por oraciones y por secciones.</td><td align="center">⬜</td><td align="center">⬜</td></tr>
<tr><td><code>Incrustacion</code></td><td>Convierte los fragmentos en <i>embeddings</i> (vectores) con Voyage AI.</td><td align="center">⬜</td><td align="center">✅</td></tr>
<tr><td><code>Vectorizacion</code></td><td>Arma una base de datos vectorial en memoria y hace búsqueda semántica sobre <code>report.md</code>.</td><td align="center">⬜</td><td align="center">✅</td></tr>
<tr><td><code>BusquedaLexica</code></td><td>Búsqueda por palabras clave con BM25, implementado desde cero.</td><td align="center">⬜</td><td align="center">⬜</td></tr>
<tr><td><code>Hibrido (1)</code></td><td>Búsqueda híbrida: une vectores y BM25 con <i>Reciprocal Rank Fusion</i>.<br>💾 <b>Usa un modelo local que la primera vez descarga más de 2 GB.</b> Requiere <code>pip install sentence-transformers</code>.</td><td align="center">⬜</td><td align="center">⬜</td></tr>
</tbody>
</table>

<br>

<a id="proyectos"></a>

## 🧩 Proyectos

<table>
<tr>
<td width="50%" valign="top">

### 💬 `cli_project`

**Chat por consola con MCP**

Chat en la terminal conectado a un servidor MCP con documentos de ejemplo. Menciona documentos con `@` (por ejemplo `@deposition.md`) y ejecuta comandos con `/`.

✅ Claude &nbsp;·&nbsp; ⬜ Voyage

</td>
<td width="50%" valign="top">

### 📄 `app_starter`

**Servidor MCP para documentos**

Herramientas para sumar números y para convertir archivos PDF o DOCX a Markdown. Incluye tests con `pytest`.

⬜ Claude &nbsp;·&nbsp; ⬜ Voyage

</td>
</tr>
</table>

<details>
<summary><b>▶️ Cómo ejecutar <code>cli_project</code></b></summary>
<br>

1. Entra a la carpeta y crea su propio `.env`:

   ```bash
   cd cli_project
   copy .env.example .env      # Windows
   cp .env.example .env        # Mac / Linux
   ```

2. Rellena las tres variables:

   ```ini
   ANTHROPIC_API_KEY=sk-ant-...
   CLAUDE_MODEL=claude-haiku-4-5
   USE_UV=0                    # 1 si usas uv, 0 si no
   ```

3. Instala y ejecuta:

   ```bash
   pip install anthropic python-dotenv prompt-toolkit "mcp[cli]"
   python main.py
   ```

Más detalles en [`cli_project/README.md`](cli_project/README.md).

</details>

<details>
<summary><b>▶️ Cómo ejecutar <code>app_starter</code></b></summary>
<br>

Este proyecto usa [uv](https://github.com/astral-sh/uv). Si no lo tienes: `pip install uv`.

```bash
cd app_starter
uv venv
uv pip install -e .
uv run main.py      # inicia el servidor MCP
uv run pytest       # ejecuta los tests
```

> 💡 Al iniciarlo, el servidor se queda esperando a que se conecte un cliente MCP, así que es normal que no muestre nada en la terminal.

Más detalles en [`app_starter/README.md`](app_starter/README.md).

</details>

<br>

<a id="estructura"></a>

## 🗂️ Estructura del repositorio

```text
Curso_API_Claude/
├── 📓 *.ipynb        Notebooks del curso (ver la guía de arriba)
├── 📁 cli_project/   Chat por consola con MCP
├── 📁 app_starter/   Servidor MCP de herramientas para documentos
├── 📁 images/        Imágenes satelitales para Imagenes.ipynb
├── 📄 report.md      Documento de ejemplo para chunking, embeddings y búsqueda
├── 📄 earth.pdf      PDF de ejemplo para PDF.ipynb
├── 📄 dataset.json   Casos de prueba de la evaluación de prompts
├── 📄 output.json    Resultados de la evaluación de prompts
├── 📄 output.html    Reporte visual de la evaluación de prompts
├── 📄 main.py        Archivo que lee EditorHerramienta.ipynb
└── 🔒 .env.example   Plantilla de claves: cópiala a .env
```

<br>

## 🔒 Seguridad

> [!CAUTION]
> Tus claves van **solo** en el archivo `.env`, que git ignora. Nunca las escribas dentro de un notebook.
>
> Si alguna vez subes una clave por error, **revócala de inmediato** en la consola correspondiente y crea una nueva. Borrarla del repositorio no basta.

<br>

<div align="center">
<sub>Hecho por <a href="https://github.com/jacob0900">jacob0900</a> durante el curso de la API de Claude</sub>
</div>
