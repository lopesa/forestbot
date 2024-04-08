"use client";

import Chat from "./components/Chat";
import { useChat } from "ai/react";
import { FormEvent } from "react";

export default function Home() {
  const { messages, input, handleInputChange, handleSubmit } = useChat({
    onFinish: async () => {
      // setGotMessages(true);
    },
  });

  const handleMessageSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    handleSubmit(e);
    // setContext(null);
    // setGotMessages(false);
  };
  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-24">
      <Chat
        input={input}
        handleInputChange={handleInputChange}
        handleMessageSubmit={handleMessageSubmit}
        messages={messages}
      />
    </main>
  );
}
