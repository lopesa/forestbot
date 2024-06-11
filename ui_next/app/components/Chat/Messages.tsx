import { Message } from 'ai';
import { useEffect, useRef, useState } from 'react';
import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger
} from '@/components/ui/accordion';

export interface messageWithAugmentationData extends Message {
  augmentationData?: {
    page_content: string;
    metadata: {
      page: number;
      source: string;
    };
  }[];
}

export default function Messages({
  messages,
  augmentationDataArray
}: {
  messages: messageWithAugmentationData[];
  augmentationDataArray: any[];
}) {
  const messagesEndRef = useRef<HTMLDivElement | null>(null);
  const [messagesWithAugmentationData, setMessagesWithAugmentationData] =
    useState<messageWithAugmentationData[]>([]);
  useEffect(() => {
    if (messages.length && augmentationDataArray.length) {
      var i = 0;
      messages.forEach(message => {
        if (message.role === 'assistant' && augmentationDataArray.length) {
          message.augmentationData = augmentationDataArray[i];
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
          } my-2 p-3 rounded shadow-md hover:shadow-lg transition-shadow duration-200 flex items-center slide-in-bottom bg-gray-800 border border-gray-600 message-glow`}
        >
          <div className="rounded-tl-lg bg-gray-800 p-2 border-r border-gray-600 flex items-center">
            {msg.role === 'assistant' ? '🤖' : '🧑‍💻'}
          </div>
          <div className="flex flex-col">
            <div
              className={`ml-2 flex items-center ${msg.role === 'assistant' ? 'text-gray-200' : 'text-gray-400'} `}
            >
              {msg.content}
            </div>

            {msg.augmentationData && (
              <Accordion type="single" collapsible>
                <AccordionItem
                  value="item-1"
                  className="text-xs text-gray-200 p-3"
                >
                  <AccordionTrigger className="font-bold">
                    Metadata
                  </AccordionTrigger>
                  <AccordionContent>
                    {msg.augmentationData.map((augmentationData, i) => (
                      <div key={i}>
                        <div className="text-xs text-gray-200 font-bold">
                          Source: {augmentationData?.metadata.source}
                        </div>
                        <div className="text-xs text-gray-200 font-bold pb-1">
                          Page: {augmentationData?.metadata.page}
                        </div>
                        <div className="text-xs text-gray-200 pb-4">
                          Page Content: {augmentationData?.page_content}
                        </div>
                      </div>
                    ))}
                  </AccordionContent>
                </AccordionItem>
              </Accordion>
            )}
          </div>
        </div>
      ))}
      <div ref={messagesEndRef} />
    </div>
  );
}
