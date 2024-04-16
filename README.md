# Templates

The starting template is a combination of the following 2 vercel templates:

1. https://vercel.com/templates/next.js/nextjs-flask-starter:

**How it works** (from the readme):

The Python/Flask server is mapped into to Next.js app under `/api/`.

This is implemented using [`next.config.js` rewrites](https://github.com/vercel/examples/blob/main/python/nextjs-flask/next.config.js) to map any request to `/api/:path*` to the Flask API, which is hosted in the `/api` folder.

On localhost, the rewrite will be made to the `127.0.0.1:5328` port, which is where the Flask server is running.

In production, the Flask server is hosted as [Python serverless functions](https://vercel.com/docs/concepts/functions/serverless-functions/runtimes/python) on Vercel.

2. https://github.com/vercel/ai-chatbot. Basic chatbot components pulled from here

# Setup notes

add a `.env` file in the root directory with the following content:

```
OPENAI_API_KEY=your_openai_api_key
```

python version has to be 3.11.0. 3.12.0 (only specfically tried 3.12, not sure about > 3.12.0) gives a setup error

node version has to be 18.x, not 20.x. 20.x is incompatible with the needed Python version within Vercel.
See here: https://stackoverflow.com/questions/78233938/vercel-error-unable-to-find-any-supported-python-versions

## Getting Started

First, install the dependencies:

```bash
npm install
# or
yarn
# or
pnpm install
```

Then, run the development server:

I recommend running the Flask server in a separate terminal window, especially if you want to debug the api.

```bash
# in one window:
npm run next-dev
# in another window:
npm run flask-dev
```

If you want to run both servers in one terminal window, you can run the following command:

```bash
npm run dev
# or
yarn dev
# or
pnpm dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

The Flask server will be running on [http://127.0.0.1:5328](http://127.0.0.1:5328) – feel free to change the port in `package.json` (you'll also need to update it in `next.config.js`).
