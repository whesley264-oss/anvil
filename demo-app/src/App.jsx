import { useState } from 'react'
import './App.css'

function App() {
  const [count, setCount] = useState(0)

  return (
    <div className="app">
      <header className="header">
        <nav className="nav">
          <div className="logo">⚡ ANVIL</div>
          <div className="nav-links">
            <a href="#features">Features</a>
            <a href="#demo">Demo</a>
            <a href="#docs">Docs</a>
            <button className="btn-primary">Get Started</button>
          </div>
        </nav>
      </header>

      <main className="main">
        <section className="hero">
          <h1>Transform Websites into <span className="highlight">Mobile Apps</span></h1>
          <p className="subtitle">
            Build native Android APKs from any website in seconds. 
            No Android Studio required.
          </p>
          <div className="cta-buttons">
            <button className="btn-primary btn-large">Try Now →</button>
            <button className="btn-secondary btn-large">View Demo</button>
          </div>
          <div className="stats">
            <div className="stat">
              <span className="stat-value">50K+</span>
              <span className="stat-label">Downloads</span>
            </div>
            <div className="stat">
              <span className="stat-value">4.9★</span>
              <span className="stat-label">Rating</span>
            </div>
            <div className="stat">
              <span className="stat-value">99%</span>
              <span className="stat-label">Success</span>
            </div>
          </div>
        </section>

        <section id="features" className="features">
          <h2>Why Choose ANVIL?</h2>
          <div className="feature-grid">
            <div className="feature-card">
              <div className="feature-icon">🚀</div>
              <h3>Lightning Fast</h3>
              <p>Build APKs in under 2 minutes with our optimized pipeline.</p>
            </div>
            <div className="feature-card">
              <div className="feature-icon">🎨</div>
              <h3>Beautiful UI</h3>
              <p>Modern Material Design 3 components out of the box.</p>
            </div>
            <div className="feature-card">
              <div className="feature-icon">🔒</div>
              <h3>Secure</h3>
              <p>End-to-end encryption and secure APK signing.</p>
            </div>
            <div className="feature-card">
              <div className="feature-icon">☁️</div>
              <h3>Cloud Ready</h3>
              <p>Deploy anywhere with our CI/CD integration.</p>
            </div>
          </div>
        </section>

        <section id="demo" className="demo">
          <h2>See It In Action</h2>
          <div className="demo-preview">
            <div className="phone-frame">
              <div className="screen">
                <div className="app-preview">
                  <div className="preview-header">
                    <span className="preview-dots">● ● ●</span>
                  </div>
                  <div className="preview-content">
                    <h4>Welcome to ANVIL</h4>
                    <p>Your mobile app is ready!</p>
                    <div className="counter-demo">
                      <button onClick={() => setCount(c => c - 1)}>−</button>
                      <span>{count}</span>
                      <button onClick={() => setCount(c => c + 1)}>+</button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>
      </main>

      <footer className="footer">
        <p>© 2024 ANVIL • Built with ⚡</p>
      </footer>
    </div>
  )
}

export default App
