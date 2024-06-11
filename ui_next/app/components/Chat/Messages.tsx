import { Message } from 'ai';
import { useEffect, useRef, useState } from 'react';

export default function Messages({
  messages,
  augmentationDataArray
}: {
  messages: Message[];
  augmentationDataArray: any[];
}) {
  const messagesEndRef = useRef<HTMLDivElement | null>(null);
  const [messagesWithAugmentationData, setMessagesWithAugmentationData] =
    useState<Message[]>([]);
  useEffect(() => {
    if (messages.length && augmentationDataArray.length) {
      var i = 0;
      messages.forEach(message => {
        if (message.role === 'assistant' && augmentationDataArray.length) {
          message.data = augmentationDataArray[i];
          i++;
        }
      });
    }
    setMessagesWithAugmentationData(messages);
  }, [messages]);
  return (
    <div className="border-2 border-gray-600 p-6 rounded-lg overflow-y-scroll flex-grow flex flex-col justify-end bg-gray-700">
      {messagesWithAugmentationData.map((msg, index) => (
        <div
          key={index}
          className={`${
            msg.role === 'assistant' ? 'text-green-300' : 'text-blue-300'
          } my-2 p-3 rounded shadow-md hover:shadow-lg transition-shadow duration-200 flex slide-in-bottom bg-gray-800 border border-gray-600 message-glow`}
        >
          <div className="rounded-tl-lg bg-gray-800 p-2 border-r border-gray-600 flex items-center">
            {msg.role === 'assistant' ? '🤖' : '🧑‍💻'}
          </div>
          <div className="ml-2 flex items-center text-gray-200">
            {msg.content}
          </div>

          {msg.data && (
            <div className="ml-2 flex items-center text-gray-200 text-xs">
              {JSON.stringify(msg.data)}
            </div>
          )}
        </div>
      ))}
      <div ref={messagesEndRef} />
    </div>
  );
}
