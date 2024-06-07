'use client';

import Chat from './components/Chat';
import { useChat } from 'ai/react';
import { FormEvent, useState } from 'react';

import { Label } from '@/components/ui/label';
import { RadioGroup, RadioGroupItem } from '@/components/ui/radio-group';

// enum LLM_VERSION {
//   GPT_PASSTHROUGH = 'gpt-passthrough',
//   RAG_V1 = 'rag-v1'
// }

export default function Home() {
  const { messages, input, handleInputChange, handleSubmit } = useChat({
    // api: 'https://jellyfish-app-ll6mk.ondigitalocean.app/api/chat',
    api:
      process.env.NODE_ENV === 'development'
        ? 'http://127.0.0.1:5328/api/chat'
        : 'https://jellyfish-app-ll6mk.ondigitalocean.app/api/chat',
    onFinish: async () => {},
    streamMode: 'text'
  });

  const handleMessageSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    handleSubmit(e);
  };

  // const [llmVersion, setLlmVersion] = useState<LLM_VERSION>(
  //   LLM_VERSION.GPT_PASSTHROUGH
  // );

  return (
    <main className="flex min-h-screen flex-col items-center justify-start p-24">
      <h1 className="text-4xl font-bold mb-10">Forest Info Bot</h1>
      <Chat
        input={input}
        handleInputChange={handleInputChange}
        handleMessageSubmit={handleMessageSubmit}
        messages={messages}
      />

      {/* <h3 className="text-xl">LLM version: {llmVersion}</h3> */}

      {/* <RadioGroup defaultValue={llmVersion} className="flex text-sm mt-4">
        <div>Set LLM Version</div>
        <div className="flex items-center space-x-2">
          <RadioGroupItem
            value={LLM_VERSION.GPT_PASSTHROUGH}
            id={LLM_VERSION.GPT_PASSTHROUGH}
            onClick={() => {
              setLlmVersion(LLM_VERSION.GPT_PASSTHROUGH);
            }}
          />
          <Label htmlFor="option-one">gpt passthrough</Label>
        </div>
        <div className="flex items-center space-x-2">
          <RadioGroupItem
            value={LLM_VERSION.RAG_V1}
            id={LLM_VERSION.RAG_V1}
            onClick={() => {
              setLlmVersion(LLM_VERSION.RAG_V1);
            }}
          />
          <Label htmlFor="option-two">rag v1</Label>
        </div>
      </RadioGroup> */}
    </main>
  );
}
