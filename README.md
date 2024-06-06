## Forest Info Bot - A RAG app for exploring a large pdf (1, for now). Implemented to support Central African Environmental Preservation

The repo contains the Nextjs ui and backend Fastapi, the PDFs and a workspace folder

## Getting Started

With both versions of the app, use poetry to manage the python dependencies

```bash
poetry install
poetry shell
```

Add a `.env` file in the root directory with the following content:

```
OPENAI_API_KEY=<your_openai_api_key>
```

### Fastapi

```bash
cd backend_fastapi
```

```bash
poetry run uvicorn app:app --port 5328
```

for dev you can do:

```bash
poetry run uvicorn app:app --reload --port 5328
```

Or in vscode you can debug using

```
Run -> Start Debugging
```

The Fastapi server will be running on [http://127.0.0.1:5328](http://127.0.0.1:5328)

### UI

Install the dependencies:

```bash
cd ui_next
npm install
# or
yarn
# or
pnpm install
```

Then, run the development server:

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.
