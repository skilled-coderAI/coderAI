import { useState, useEffect } from "react";
import "./App.css";
import axios from "axios";
import ReactMarkdown from "react-markdown";
import Footer from "./Footer";
import ShareButtons from "./components/ShareButtons";
import CodeAnalysis from "./components/CodeAnalysis";
import { FaMicrophone, FaPaperPlane, FaVolumeUp } from "react-icons/fa";

const cache = new Map();

function App() {
  const [question, setQuestion] = useState("");
  const [chatHistory, setChatHistory] = useState([]);
  const [generatingAnswer, setGeneratingAnswer] = useState(false);
  const [isListening, setIsListening] = useState(false);
  const [recognition, setRecognition] = useState(null);
  const [isSpeaking, setIsSpeaking] = useState(false);
  const [mode, setMode] = useState("chat"); // "chat" or "code"
  const [isEmbedded, setIsEmbedded] = useState(false);

  useEffect(() => {
    // Check if running in an iframe
    setIsEmbedded(window.self !== window.top);

    if ("webkitSpeechRecognition" in window) {
      const recognition = new window.webkitSpeechRecognition();
      recognition.continuous = false;
      recognition.interimResults = false;
      recognition.lang = "en-US";

      recognition.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        setQuestion(transcript);
        setIsListening(false);
      };

      recognition.onerror = (event) => {
        console.error("Speech recognition error:", event.error);
        setIsListening(false);
      };

      recognition.onend = () => {
        setIsListening(false);
      };

      setRecognition(recognition);
    }
  }, []);

  const toggleListening = () => {
    if (isListening) {
      recognition.stop();
      setIsListening(false);
    } else {
      recognition.start();
      setIsListening(true);
    }
  };

  const toggleSpeaking = (text) => {
    if (isSpeaking) {
      window.speechSynthesis.cancel();
      setIsSpeaking(false);
    } else {
      const utterance = new SpeechSynthesisUtterance(text);
      utterance.lang = "en-US";
      utterance.onend = () => setIsSpeaking(false);
      setIsSpeaking(true);
      window.speechSynthesis.speak(utterance);
    }
  };

  async function generateAnswer(e) {
    e.preventDefault();
    if (!question.trim()) return;

    if (generatingAnswer) {
      console.log("Already generating an answer. Please wait...");
      return;
    }

    setGeneratingAnswer(true);

    if (cache.has(question)) {
      console.log("Fetching from cache...");
      setChatHistory((prevChat) => [
        ...prevChat,
        { type: "question", text: question },
        { type: "answer", text: cache.get(question) },
      ]);
      setQuestion("");
      setGeneratingAnswer(false);
      return;
    }

    const apiKey = import.meta.env.VITE_API_GENERATIVE_LANGUAGE_CLIENT;

    let attempts = 0;
    const maxAttempts = 3;
    let delay = 2000;

    while (attempts < maxAttempts) {
      try {
        const response = await axios({
          url: `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=${apiKey}`,
          method: "post",
          headers: { 'Content-Type': 'application/json' },
          data: { contents: [{ parts: [{ text: question }] }] },
        });

        if (response.data?.candidates?.length > 0) {
          const fullAnswer = response.data.candidates[0].content.parts[0].text;

          cache.set(question, fullAnswer);

          setChatHistory((prevChat) => [
            ...prevChat,
            { type: "question", text: question },
            { type: "answer", text: fullAnswer },
          ]);

          setQuestion("");
        } else {
          throw new Error("Invalid API response structure");
        }
        break;
      } catch (error) {
        console.error("API Error:", error);

        if (error.response?.status === 429) {
          if (attempts < maxAttempts - 1) {
            console.warn(`Rate limit hit. Retrying in ${delay / 1000} seconds...`);
            await new Promise((resolve) => setTimeout(resolve, delay));
            delay *= 2;
            attempts++;
          } else {
            setChatHistory((prevChat) => [
              ...prevChat,
              { type: "answer", text: "Rate limit exceeded. Please try again later." },
            ]);
            break;
          }
        } else {
          setChatHistory((prevChat) => [
            ...prevChat,
            { type: "answer", text: "Sorry, something went wrong. Please try again!" },
          ]);
          break;
        }
      }
    }

    setGeneratingAnswer(false);
  }

  return (
    <div className={`flex flex-col ${isEmbedded ? 'h-screen' : 'min-h-screen'} bg-gray-950 text-white`}>
      <nav className="p-2 bg-[#040E23]">
        <div className="flex justify-between items-center max-w-4xl mx-auto">
          <h1 className="text-xl font-bold">Helpmate AI</h1>
          <div className="flex gap-2">
            <button
              onClick={() => setMode("chat")}
              className={`px-3 py-1 rounded-lg ${mode === "chat" ? "bg-blue-600" : "bg-gray-700"} text-white transition-colors text-sm`}
            >
              Chat
            </button>
            <button
              onClick={() => setMode("code")}
              className={`px-3 py-1 rounded-lg ${mode === "code" ? "bg-blue-600" : "bg-gray-700"} text-white transition-colors text-sm`}
            >
              Code Analysis
            </button>
          </div>
        </div>
      </nav>
      <div className="flex-grow p-2">
        {mode === "chat" ? (
          <div className="chat-display space-y-2">
            {chatHistory.map((chat, index) => (
              <div
                key={index}
                className={`p-2 rounded-lg ${
                  chat.type === "question"
                    ? "bg-blue-600 text-white self-end text-right w-fit max-w-[90%] ml-auto"
                    : "bg-gray-800 text-white self-start text-left w-fit max-w-[90%]"
                }`}
              >
                <ReactMarkdown className="markdown-body">{chat.text}</ReactMarkdown>
                {chat.type === "answer" && (
                  <div className="flex flex-wrap justify-end mt-1 space-x-1">
                    <button onClick={() => toggleSpeaking(chat.text)} className="flex items-center text-gray-300 mt-1 mr-1">
                      <FaVolumeUp className="mr-1" />
                    </button>
                    <ShareButtons answer={chat.text} />
                  </div>
                )}
              </div>
            ))}
            {generatingAnswer && (
              <div className="p-2 rounded-lg bg-gray-900 animate-pulse">
                <div className="h-3 bg-gray-700 rounded w-3/4 mb-1"></div>
                <div className="h-3 bg-gray-700 rounded w-2/3 mb-1"></div>
                <div className="h-3 bg-gray-700 rounded w-1/2"></div>
              </div>
            )}
          </div>
        ) : (
          <CodeAnalysis />
        )}
      </div>
      {mode === "chat" && (
        <div>
          <form onSubmit={generateAnswer} className="flex items-center w-full bg-gray-900 p-2">
            <textarea
              required
              className="border border-gray-800 bg-gray-800 text-white rounded-lg w-full p-1 h-10 resize-none focus:border-blue-500 outline-none"
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              placeholder="Your AI mate is here to help!"
            />
            <div className="flex items-center space-x-1 ml-2">
              {recognition && (
                <button
                  type="button"
                  onClick={toggleListening}
                  className={`p-1 rounded-full transition-transform duration-300 ease-in-out ${
                    isListening ? "bg-red-500" : "bg-blue-500"
                  } hover:opacity-80`}
                >
                  <FaMicrophone className="text-white" />
                </button>
              )}
              <button
                type="submit"
                className="p-1 rounded-full bg-blue-600 hover:bg-blue-700"
                disabled={generatingAnswer}
              >
                <FaPaperPlane className={`text-white ${generatingAnswer ? "send-animation" : ""}`} />
              </button>
            </div>
          </form>
          <Footer />
        </div>
      )}
    </div>
  );
}

export default App;