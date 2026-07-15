import { useMemo, useState } from 'react';

type AgentId = 'rest' | 'keyword' | 'semantic' | 'tools' | 'mcp' | 'orchestration';

type ChatMessage = {
  role: 'user' | 'assistant';
  content: string;
};

type ChatResponsePayload = {
  agent: string;
  reply: string;
  placeholder: boolean;
};

const agents: Record<AgentId, { label: string; description: string }> = {
  rest: { label: 'REST API Agent', description: 'Inference via REST API backend' },
  keyword: { label: 'Keyword Search Agent', description: 'Simple RAG with keyword search' },
  semantic: { label: 'Semantic Search Agent', description: 'RAG with semantic search' },
  tools: { label: 'Tool Agent', description: 'RAG with tool calling capability' },
  mcp: { label: 'MCP Agent', description: 'RAG with MCP integration' },
  orchestration: { label: 'Orchestration Agent', description: 'Multi-agent orchestration' },
};

const initialMessages: ChatMessage[] = [
  { role: 'assistant', content: 'Select an agent and start the conversation.' },
];

const apiBaseUrl = (import.meta.env.VITE_API_BASE_URL ?? '/api').replace(/\/$/, '');

const App = () => {
  const [agent, setAgent] = useState<AgentId>('rest');
  const [messages, setMessages] = useState<ChatMessage[]>(initialMessages);
  const [input, setInput] = useState('');

  const agentInfo = agents[agent];

  const handleAgentChange = (value: AgentId) => {
    setAgent(value);
    setMessages([
      { role: 'assistant', content: `Agent switched to ${agents[value].label}. Start a new conversation.` },
    ]);
    setInput('');
  };

  const handleClear = () => {
    setMessages(initialMessages);
    setInput('');
  };

  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const content = input.trim();
    if (!content) return;

    const userMessage = { role: 'user' as const, content };
    const nextHistory = [...messages, userMessage];
    setMessages((current) => [...current, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      const response = await fetch(`${apiBaseUrl}/agents/${agent}/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: content, history: nextHistory }),
      });

      if (!response.ok) {
        throw new Error(`Request failed with status ${response.status}`);
      }

      const payload = (await response.json()) as ChatResponsePayload;
      setMessages((current) => [
        ...current,
        { role: 'assistant', content: payload.reply },
      ]);
    } catch (error) {
      const message = error instanceof Error ? error.message : 'Unexpected error';
      setMessages((current) => [
        ...current,
        { role: 'assistant', content: `Request failed: ${message}` },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  const conversationPayload = useMemo(
    () => ({ agent, history: messages }),
    [agent, messages]
  );

  return (
    <div className="page-shell">
      <div className="chat-card">
        <header className="chat-header">
          <div>
            <p className="eyebrow">Foundation AI Lab</p>
            <h1>AI Agent Chat</h1>
            <p className="subtitle">Choose an agent, send a message, and keep the active conversation.</p>
          </div>
          <div className="controls-row">
            <label className="select-label">
              Agent
              <select
                value={agent}
                onChange={(event) => handleAgentChange(event.target.value as AgentId)}
              >
                {Object.entries(agents).map(([key, value]) => (
                  <option key={key} value={key}>{value.label}</option>
                ))}
              </select>
            </label>
            <button type="button" className="clear-button" onClick={handleClear}>
              Clear Chat
            </button>
          </div>
        </header>

        <section className="agent-card">
          <div>
            <p className="agent-label">Active agent</p>
            <h2>{agentInfo.label}</h2>
            <p>{agentInfo.description}</p>
          </div>
        </section>

        <main className="message-list" aria-live="polite">
          {messages.map((message, index) => (
            <article key={`${message.role}-${index}`} className={`message ${message.role}`}>
              <span className="message-role">{message.role === 'user' ? 'You' : 'Agent'}</span>
              <p>{message.content}</p>
            </article>
          ))}
        </main>

        <form className="message-form" onSubmit={handleSubmit}>
          <label htmlFor="chat-input" className="sr-only">Type your message</label>
          <textarea
            id="chat-input"
            rows={3}
            value={input}
            onChange={(event) => setInput(event.target.value)}
            placeholder="Ask the current agent anything..."
          />
          <button type="submit" className="send-button" disabled={isLoading}>
            {isLoading ? 'Thinking…' : 'Send'}
          </button>
        </form>

        <footer className="payload-panel">
          <h3>Payload preview</h3>
          <pre>{JSON.stringify(conversationPayload, null, 2)}</pre>
        </footer>
      </div>
    </div>
  );
};

export default App;
