import React, { useState, useRef } from 'react';
import { motion } from 'framer-motion';
import './LandingPage.css';

export default function LandingPage({ onEnter, theme, toggleTheme }) {
    const [accessCode, setAccessCode] = useState('');
    const [accessError, setAccessError] = useState(false);
    const heroInputRef = useRef(null);

    const handleAccessSubmit = async () => {
        try {
            const response = await fetch(`${import.meta.env.VITE_API_URL || ''}/api/auth/verify`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ access_code: accessCode })
            });

            if (response.ok) {
                onEnter();
            } else {
                setAccessError(true);
                setTimeout(() => setAccessError(false), 2000);
            }
        } catch (error) {
            console.error('Auth error:', error);
            setAccessError(true);
            setTimeout(() => setAccessError(false), 2000);
        }
    };

    return (
        <div className="landing-container">
            {/* Background Orbs Elements */}
            <div className="landing-bg">
                <div className="bg-orb orb-1"></div>
                <div className="bg-orb orb-2"></div>
                <div className="bg-orb orb-3"></div>
            </div>

            {/* Navigation Header */}
            <header className="landing-nav">
                <div className="nav-logo">
                    <span className="nav-icon">🤖</span>
                    <span className="nav-title">Shivy AI</span>
                </div>
                <div className="nav-actions">
                    <button className="btn-icon btn-ghost" onClick={toggleTheme} title="Toggle Theme" style={{ marginRight: 12 }}>
                        {theme === 'light' ? '🌙' : '☀️'}
                    </button>
                    <button className="btn-nav-cta" onClick={() => heroInputRef.current?.focus()}>
                        Open App
                    </button>
                </div>
            </header>

            <main className="landing-main">
                {/* Hero Section */}
                <section className="hero-section">
                    <motion.div
                        className="hero-content"
                        initial={{ opacity: 0, y: 30 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.8 }}
                    >
                        <h1 className="hero-headline">
                            The Future of School, <br />
                            <span className="text-gradient">Powered by AI</span>
                        </h1>
                        <p className="hero-subheadline">
                            Upload textbooks, practice with interactive quizzes, and talk naturally to Shivy AI.
                            Experience a truly personalized tutor that simplifies complex learning.
                        </p>
                        <div className="access-container">
                            <div className="access-input-group">
                                <input 
                                    ref={heroInputRef}
                                    type="text" 
                                    className={`access-input ${accessError ? 'error' : ''}`}
                                    placeholder="Enter Judge Access Code" 
                                    value={accessCode}
                                    onChange={(e) => setAccessCode(e.target.value)}
                                    onKeyDown={(e) => e.key === 'Enter' && handleAccessSubmit()}
                                />
                                <motion.button
                                    className="btn-primary-cta"
                                    onClick={handleAccessSubmit}
                                    whileHover={{ scale: 1.05 }}
                                    whileTap={{ scale: 0.95 }}
                                >
                                    Start Learning Free
                                </motion.button>
                            </div>
                            <div className={`access-error-msg ${accessError ? 'visible' : ''}`}>
                                Invalid access code
                            </div>
                        </div>
                    </motion.div>

                    <motion.div
                        className="hero-image-wrapper"
                        initial={{ opacity: 0, y: 50 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.8, delay: 0.2 }}
                    >
                        <div className="glass-mockup">
                            <div className="mockup-header">
                                <i className="dot red"></i>
                                <i className="dot yellow"></i>
                                <i className="dot green"></i>
                            </div>
                            <img src="/assets/shivy_ai.png" alt="Shivy AI Interface" className="mockup-img" />
                        </div>
                    </motion.div>
                </section>

                {/* Alternating Features Section */}
                <section className="features-section">
                    {/* Feature 1: Voice Tutor */}
                    <div className="feature-row">
                        <motion.div
                            className="feature-text-block"
                            initial={{ opacity: 0, x: -50 }}
                            whileInView={{ opacity: 1, x: 0 }}
                            viewport={{ once: true, margin: "-100px" }}
                        >
                            <div className="feature-badge">🗣️ Real-time Voice</div>
                            <h2>Meet Shivy AI Tutor</h2>
                            <p>
                                Practice with natural, back-and-forth conversations in English, Spanish, German, Hindi, Urdu, and Arabic.
                                The Voice Tutor actively listens, understands your context from the textbook, and guides you through complex topics.
                                Interrupt it anytime—it instantly adapts just like a human teacher.
                            </p>
                        </motion.div>
                        <motion.div
                            className="feature-image-block"
                            initial={{ opacity: 0, x: 50 }}
                            whileInView={{ opacity: 1, x: 0 }}
                            viewport={{ once: true, margin: "-100px" }}
                        >
                            <div className="glass-mockup feature-mockup">
                                <img src="/assets/landing_voice.webp" alt="Voice Tutor Interface Animation" />
                            </div>
                        </motion.div>
                    </div>

                    {/* Feature 2: Visuals (Reversed) */}
                    <div className="feature-row reversed">
                        <motion.div
                            className="feature-text-block"
                            initial={{ opacity: 0, x: 50 }}
                            whileInView={{ opacity: 1, x: 0 }}
                            viewport={{ once: true, margin: "-100px" }}
                        >
                            <div className="feature-badge">🎨 Smart Diagrams</div>
                            <h2>Automatic Visual Explanations</h2>
                            <p>
                                Some concepts are hard to grasp through text alone. As the tutor explains complex math equations or science theories,
                                it automatically generates helpful diagrams, charts, and image references to ensure you completely visualize the material.
                            </p>
                        </motion.div>
                        <motion.div
                            className="feature-image-block"
                            initial={{ opacity: 0, x: -50 }}
                            whileInView={{ opacity: 1, x: 0 }}
                            viewport={{ once: true, margin: "-100px" }}
                        >
                            <div className="glass-mockup feature-mockup">
                                <img src="/assets/landing_visuals.webp" alt="Visual Explanations Animation" />
                            </div>
                        </motion.div>
                    </div>

                    {/* Feature 3: Assessments */}
                    <div className="feature-row">
                        <motion.div
                            className="feature-text-block"
                            initial={{ opacity: 0, x: -50 }}
                            whileInView={{ opacity: 1, x: 0 }}
                            viewport={{ once: true, margin: "-100px" }}
                        >
                            <div className="feature-badge">📝 Test Your Knowledge</div>
                            <h2>Targeted Smart Assessments</h2>
                            <p>
                                Don't just read—test your understanding instantly. Shivy AI generates custom quizzes and revision flashcards
                                based exactly on the specific textbook pages and topics you are currently studying.
                            </p>
                        </motion.div>
                        <motion.div
                            className="feature-image-block"
                            initial={{ opacity: 0, x: 50 }}
                            whileInView={{ opacity: 1, x: 0 }}
                            viewport={{ once: true, margin: "-100px" }}
                        >
                            <div className="glass-mockup feature-mockup">
                                <img src="/assets/landing_assessment.webp" alt="Assessment Center Animation" />
                            </div>
                        </motion.div>
                    </div>
                </section>

                {/* Final CTA */}
                <section className="cta-section">
                    <motion.div
                        className="cta-box"
                        initial={{ opacity: 0, scale: 0.9 }}
                        whileInView={{ opacity: 1, scale: 1 }}
                        viewport={{ once: true }}
                    >
                        <h2>Ready to boost your grades?</h2>
                        <p>Join thousands of students learning smarter with Shivy AI.</p>
                        <div className="access-container" style={{ marginTop: '25px' }}>
                            <div className="access-input-group">
                                <input 
                                    type="text" 
                                    className={`access-input ${accessError ? 'error' : ''}`}
                                    placeholder="Enter Judge Access Code" 
                                    value={accessCode}
                                    onChange={(e) => setAccessCode(e.target.value)}
                                    onKeyDown={(e) => e.key === 'Enter' && handleAccessSubmit()}
                                />
                                <button className="btn-primary-cta" onClick={handleAccessSubmit}>
                                    Enter the Classroom
                                </button>
                            </div>
                            <div className={`access-error-msg ${accessError ? 'visible' : ''}`}>
                                Invalid access code
                            </div>
                        </div>
                    </motion.div>
                </section>
            </main>

            <footer className="landing-footer">
                <div className="footer-content">
                    <div className="footer-logo">
                        <span>🤖 Shivy AI</span>
                    </div>
                    <div className="footer-links">
                        <span>© 2026 Shivy AI</span>
                    </div>
                </div>
            </footer>
        </div>
    );
}
