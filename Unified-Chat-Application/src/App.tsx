import { useEffect, useMemo, useState } from 'react';

type AgentOption = {
  id: string;
  label: string;
  description: string;
};

type ChatMessage = {
  role: 'user' | 'assistant';
  content: string;
};

type ChatResponsePayload = {
  agent: string;
  reply: string;
  placeholder: boolean;
};

type AgentsPayload = {
  agents: AgentOption[];
};

const initialMessages: ChatMessage[] = [
  { role: 'assistant', content: 'Select an agent and start the conversation.' },
];

const apiBaseUrl = (import.meta.env.VITE_API_BASE_URL ?? '/api').replace(/\/$/, '');

const App = () => {
  const [agent, setAgent] = useState('');
  const [availableAgents, setAvailableAgents] = useState<AgentOption[]>([]);
  const [agentsLoading, setAgentsLoading] = useState(true);
  const [agentsError, setAgentsError] = useState<string | null>(null);
  const [messages, setMessages] = useState<ChatMessage[]>(initialMessages);
  const [input, setInput] = useState('');

  const agentInfo = useMemo(
    () => availableAgents.find((item) => item.id === agent) ?? null,
    [availableAgents, agent]
  );

  useEffect(() => {
    const controller = new AbortController();

    const loadAgents = async () => {
      setAgentsLoading(true);
      setAgentsError(null);

      try {
        const response = await fetch(`${apiBaseUrl}/agents`, { signal: controller.signal });
        if (!response.ok) {
          throw new Error(`Request failed with status ${response.status}`);
        }

        const payload = (await response.json()) as Partial<AgentsPayload>;
        const agentList = Array.isArray(payload.agents)
          ? payload.agents.filter(
              (item): item is AgentOption =>
                typeof item.id === 'string' &&
                typeof item.label === 'string' &&
                typeof item.description === 'string'
            )
          : [];

        if (agentList.length === 0) {
          throw new Error('No agents available');
        }

        setAvailableAgents(agentList);
        setAgent((current) => {
          if (current && agentList.some((item) => item.id === current)) {
            return current;
          }
          return agentList[0].id;
        });
      } catch (error) {
        if (error instanceof DOMException && error.name === 'AbortError') {
          return;
        }

        const message = error instanceof Error ? error.message : 'Unexpected error';
        setAgentsError(message);
        setAvailableAgents([]);
        setAgent('');
      } finally {
        setAgentsLoading(false);
      }
    };

    void loadAgents();

    return () => {
      controller.abort();
    };
  }, []);

  const handleAgentChange = (value: string) => {
    const selectedAgent = availableAgents.find((item) => item.id === value);
    setAgent(value);
    setMessages([
      {
        role: 'assistant',
        content: `Agent switched to ${selectedAgent?.label ?? value}. Start a new conversation.`,
      },
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
    if (!content || !agent) return;

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
              <select
                value={agent}
                onChange={(event) => handleAgentChange(event.target.value)}
                disabled={agentsLoading || availableAgents.length === 0}
              >
                {agentsLoading && <option value="">Loading agents...</option>}
                {!agentsLoading && availableAgents.length === 0 && (
                  <option value="">No agents available</option>
                )}
                {availableAgents.map((item) => (
                  <option key={item.id} value={item.id}>{item.label}</option>
                ))}
              </select>
            </label>
            <button type="button" className="clear-button" onClick={handleClear}>
              Clear Chat
            </button>
          </div>
          <p className="active-agent-inline">
            {agentInfo ? (
              <>
                <span>{agentInfo.description}</span>
              </>
            ) : (
              <span>{agentsError ? `Unable to load agents: ${agentsError}` : 'Loading available agents...'}</span>
            )}
          </p>
        </header>

        <section className="conversation-panel">
          <main className="message-list" aria-live="polite">
            {messages.map((message, index) => (
              <article key={`${message.role}-${index}`} className={`message ${message.role}`}>
                <span className="message-role">{message.role === 'user' ? 'You' : 'Agent'}</span>
                <p>{message.content}</p>
              </article>
            ))}
          </main>

          <form className="message-form" onSubmit={handleSubmit}>
            <label htmlFor="chat-input" className="sr-only">Message input</label>
            <textarea
              id="chat-input"
              rows={2}
              value={input}
              onChange={(event) => setInput(event.target.value)}
            />
            <button type="submit" className="send-button" disabled={isLoading || !agent}>
              {isLoading ? '...' : 'Send'}
            </button>
          </form>
        </section>

        <footer className="payload-panel">
          <h3>Payload preview</h3>
          <pre>{JSON.stringify(conversationPayload, null, 2)}</pre>
        </footer>
      </div>
    </div>
  );
};

export default App;
