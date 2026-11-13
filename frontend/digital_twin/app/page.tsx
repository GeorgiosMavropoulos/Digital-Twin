"use client";

import { useEffect, useRef, useState } from "react";

const introChunks = [
  "Hello! I'm Georgios Mavropoulos, and welcome to my digital world.",
  "I'm an AI engineer who loves turning ideas into systems that actually work.",
  "Most of my time goes into building LLM-powered applications,",
  "designing retrieval pipelines, and making models useful in the real world.",
  "I'm drawn to the gap between a promising demo and a reliable product,",
  "and I enjoy closing it with solid evaluation, careful design, and clean code.",
  "I keep up with new models, agents, and research,",
  "then test what really holds up in practice.",
  "This website is my digital twin, a way for you",
  "to get to know me through a conversation. Feel free to ask me anything!",
];

const suggestions = [
  "Tell me about yourself",
  "What kind of AI systems do you build?",
  "What motivates you?",
  "What are you working on?",
];

export default function Home() {
  // Typewriter state
  const introRef = useRef<HTMLElement>(null);
  const [chunkIndex, setChunkIndex] = useState(0);
  const [charIndex, setCharIndex] = useState(0);
  const [started, setStarted] = useState(false);

  // Chat state
  const [message, setMessage] = useState("");
  const [messages, setMessages] = useState<
    { role: "user" | "assistant"; content: string }[]
  >([
    {
      role: "assistant",
      content:
        "Hey! Welcome to my digital twin. Ask me anything about my background, interests, experiences, or the way I think.",
    },
  ]);

  // Start the typewriter when the intro scrolls into view.
  // Falls back to starting immediately if IntersectionObserver is unavailable.
  useEffect(() => {
    const element = introRef.current;
    if (!element) return;

    if (typeof IntersectionObserver === "undefined") {
      setStarted(true);
      return;
    }

    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          setStarted(true);
          observer.disconnect();
        }
      },
      { threshold: 0.1 }
    );

    observer.observe(element);
    return () => observer.disconnect();
  }, []);

  // Single typewriter loop: type characters, pause, then move to the next sentence
  useEffect(() => {
    if (!started || chunkIndex >= introChunks.length) return;

    const currentText = introChunks[chunkIndex];

    if (charIndex < currentText.length) {
      const timer = setTimeout(() => {
        setCharIndex((i) => i + 1);
      }, 30);
      return () => clearTimeout(timer);
    }

    const timer = setTimeout(() => {
      setChunkIndex((c) => c + 1);
      setCharIndex(0);
    }, 900);
    return () => clearTimeout(timer);
  }, [started, chunkIndex, charIndex]);

  const isDone = chunkIndex >= introChunks.length;

  function sendMessage(text = message) {
    const trimmed = text.trim();
    if (!trimmed) return;

    setMessages((current) => [...current, { role: "user", content: trimmed }]);
    setMessage("");

    // Replace this with your Python backend API
    setTimeout(() => {
      setMessages((current) => [
        ...current,
        {
          role: "assistant",
          content:
            "That's a great question! Connect your AI backend here so I can answer using Georgios's knowledge, memories, and personality.",
        },
      ]);
    }, 700);
  }

  return (
    <main className="site-shell">
      {/* NAVIGATION */}
      <nav className="navbar">
        <a href="#" className="brand">
          <span className="brand-icon">✳</span>
          GEORGIOS MAVROPOULOS AI
        </a>

        <div className="nav-right">
          <span className="online-dot" />
          AI AVAILABLE
        </div>
      </nav>

      {/* HERO SECTION */}
      <section className="hero">
        <div className="hero-copy">
          <span className="eyebrow">
            <span className="sparkle">✦</span>
            A DIGITAL VERSION OF ME
          </span>

          <h1>
            More than a profile.
            <br />
            <span>A conversation.</span>
          </h1>

          <p className="hero-description">
            A little window into who I am, what I believe in,
            what I do, and what makes me tick. Explore my
            world through my digital twin.
          </p>

          <a href="#chat" className="primary-button">
            Start a conversation <span>↗</span>
          </a>
        </div>

        {/* PROFILE PICTURE */}
        <div className="profile-card">
          <div className="profile-image">
            <img
              src="/me.jpg"
              alt="Georgios Mavropoulos"
              onError={(e) => {
                e.currentTarget.style.display = "none";
              }}
            />
          </div>

          <div className="profile-caption">
            <div>
              <span className="caption-label">THE HUMAN BEHIND THE AI</span>
              <h3>Nice to meet you.</h3>
            </div>

            <span className="profile-symbol">✳</span>
          </div>
        </div>
      </section>

      {/* INTRODUCTION SECTION */}
      <section className="intro-section" id="intro" ref={introRef}>
        <div className="section-heading">
          <span className="eyebrow">01 — GET TO KNOW ME</span>

          <h2>A story, told one piece at a time.</h2>

          <p>
            Instead of a traditional biography, here's a
            little introduction that unfolds as you explore.
          </p>
        </div>

        <div className="story-card">
          {/* INTRO HEADER */}
          <div className="story-top">
            <span className="story-icon">✧</span>

            <span>MY INTRODUCTION</span>

            <span className="story-count">
              {String(chunkIndex).padStart(2, "0")} /{" "}
              {String(introChunks.length).padStart(2, "0")}
            </span>
          </div>

          {/* TYPEWRITER TEXT */}
          <div className="story-content">
            {introChunks.slice(0, chunkIndex).map((chunk, i) => (
              <p key={i} className="story-chunk completed">
                {chunk}
              </p>
            ))}

            {!isDone && (
              <p className="story-chunk typing">
                {started ? introChunks[chunkIndex].slice(0, charIndex) : ""}
                <span className="typing-cursor">|</span>
              </p>
            )}
          </div>

          {/* PROGRESS BAR */}
          <div className="progress-track">
            <div
              className="progress-fill"
              style={{
                width: `${(chunkIndex / introChunks.length) * 100}%`,
              }}
            />
          </div>
        </div>
      </section>

      {/* DIGITAL TWIN CHAT */}
      <section className="chat-section" id="chat">
        <div className="chat-heading">
          <span className="eyebrow">02 — MEET MY DIGITAL TWIN</span>

          <h2>Curious about me?</h2>

          <p>
            Don't just read about me. Ask questions and
            explore a conversation with my AI twin.
          </p>
        </div>

        <div className="chat-window">
          {/* CHAT HEADER */}
          <div className="chat-header">
            <div className="bot-avatar">✳</div>

            <div>
              <strong>Georgios's Digital Twin</strong>

              <span>
                <i /> Online and ready to chat
              </span>
            </div>

            <span className="ai-tag">AI POWERED</span>
          </div>

          {/* CHAT MESSAGES */}
          <div className="chat-messages">
            {messages.map((msg, i) => (
              <div key={i} className={`message-row ${msg.role}`}>
                {msg.role === "assistant" && (
                  <div className="message-avatar">✳</div>
                )}

                <div className="message-bubble">{msg.content}</div>
              </div>
            ))}
          </div>

          {/* SUGGESTED QUESTIONS */}
          <div className="suggestions">
            {suggestions.map((item) => (
              <button key={item} onClick={() => sendMessage(item)}>
                {item} ↗
              </button>
            ))}
          </div>

          {/* MESSAGE INPUT */}
          <form
            className="chat-input"
            onSubmit={(e) => {
              e.preventDefault();
              sendMessage();
            }}
          >
            <input
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              placeholder="Ask me anything..."
            />

            <button type="submit" aria-label="Send message">
              ↑
            </button>
          </form>

          <div className="chat-disclaimer">
            AI-generated responses from a digital representation.
          </div>
        </div>
      </section>

      {/* FOOTER */}
      <footer>
        <span>✳ Georgios Mavropoulos AI</span>

        <span>A little more personal. A little more human.</span>
      </footer>
    </main>
  );
}