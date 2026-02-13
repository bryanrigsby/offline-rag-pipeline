import { useState } from 'react'
import './App.css'

type Message = {
  question: string
  answer: string
  sources: { document: string; page: number }[]
}

function App() {
  const [question, setQuestion] = useState('')
  const [loading, setLoading] = useState(false)
  const [messages, setMessages] = useState<Message[]>([])

  const sendQuery = async () => {
    if (question.trim().length < 10) return

    setLoading(true)
    const currentQuestion = question
    setQuestion('')
    try {
      //Build history from previous messages
      const history = messages.map(m => ({
        question: m.question,
        answer: m.answer
      }))

      const response = await fetch('http://localhost:8000/query', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-API-Key': import.meta.env.VITE_API_KEY
        },
        body: JSON.stringify({ question: currentQuestion, history }),
      })
      const data = await response.json()

      console.log('data', data)

      // add new message to thread
      setMessages(prev => [...prev, {
        question: currentQuestion,
        answer: data.answer,
        sources: data.sources
      }])
    } catch (error) {
      console.error('Error sending query:', error)
    }
    setLoading(false)
  }

  return (
    <>
      <div className="header">
        <h1>Offline RAG Pipeline</h1>
        <p>Ask questions about your documents using AI that runs entirely on your machine (air-gapped)</p>
      </div>

      <div className="chat-container">
        {messages.length === 0 && !loading && (
          <div className="empty-state">Ask a question to get started</div>
        )}
        {messages.map((msg, i) => (
          <div key={i} className="message">
            <div className="user-message">{msg.question}</div>
            <div className="assistant-message">
              {msg?.answer}
              {msg?.sources?.length > 0 && (
                <details>
                  <summary>Sources ({msg.sources.length})</summary>
                  {msg.sources.map((s, j) => (
                    <p key={j} className="source">{s.document} - Page {s.page}</p>
                  ))}
                </details>
              )}
            </div>
          </div>
        ))}
        {loading && <div className="loading">Thinking...</div>}
      </div>

      <div className="input-area">
        <form onSubmit={(e) => { e.preventDefault(); sendQuery(); }}>
          <textarea
            rows={2}
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            placeholder="Ask a question..."
          />
          <button type="submit" disabled={question.trim().length < 10 || loading}>
            Send
          </button>
          {messages.length > 0 && (
            <button type="button" onClick={() => setMessages([])}>
              New Chat
            </button>
          )}
        </form>
      </div>
    </>
  )
}

export default App
