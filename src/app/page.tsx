'use client';

import Chat from './components/Chat';
import { useChat } from 'ai/react';
import { FormEvent } from 'react';

export default function Home() {
  const { messages, input, handleInputChange, handleSubmit } = useChat({
    onFinish: async () => {
      // setGotMessages(true);
    }
  });

  const handleMessageSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    handleSubmit(e);
    // setContext(null);
    // setGotMessages(false);
  };
  return (
    <main className="flex min-h-screen flex-col items-center justify-start p-24">
      <h1 className="text-4xl font-bold mb-10">Forestbot</h1>
      <Chat
        input={input}
        handleInputChange={handleInputChange}
        handleMessageSubmit={handleMessageSubmit}
        messages={messages}
      />
      <h2 className="test-xl mb-4">
        Ask questions of the documents and backed by the documents
      </h2>
    </main>
  );
}
