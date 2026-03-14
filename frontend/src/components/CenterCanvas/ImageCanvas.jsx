import { useState, useRef, useEffect } from 'react'
import './ImageCanvas.css'

export default function ImageCanvas({
    book,
    session,
    setSession,
    pageAnalysis,
    setPageAnalysis,
    settings,
    appendTranscript,
    onVisualRequest,
    onOpenVisualPanel,
    transcript
}) {
    const [imageLoaded, setImageLoaded] = useState(false)
    const imageRef = useRef(null)

    useEffect(() => {
        setImageLoaded(false)
        setPageAnalysis(null)
    }, [book?.id, setPageAnalysis])

    const handleImageLoad = () => {
        setImageLoaded(true)
        
        // Notify the Gemini Live session locally that a new page (image) is showing
        if (imageRef.current) {
            try {
                // Draw to a temporary canvas to get a clean JPEG base64
                const canvas = document.createElement('canvas')
                canvas.width = imageRef.current.naturalWidth
                canvas.height = imageRef.current.naturalHeight
                const ctx = canvas.getContext('2d')
                ctx.drawImage(imageRef.current, 0, 0)
                const base64 = canvas.toDataURL('image/jpeg', 0.6).split(',')[1]

                window.dispatchEvent(new CustomEvent('page-changed-live', {
                    detail: { 
                        pageNumber: 1, 
                        pageText: "[The student uploaded an image for homework review.]", 
                        imageBase64: base64 
                    }
                }))
            } catch (err) {
                console.warn('[ImageCanvas] Could not extract base64 for Live session', err)
            }
        }
    }

    // Trigger an explicit vision analysis using standard REST API
    const analyzeHomework = async () => {
        if (!imageRef.current) return

        appendTranscript('system', '⏳ Sending homework to AI for review...')

        try {
            const canvas = document.createElement('canvas')
            canvas.width = imageRef.current.naturalWidth
            canvas.height = imageRef.current.naturalHeight
            const ctx = canvas.getContext('2d')
            ctx.drawImage(imageRef.current, 0, 0)
            const base64 = canvas.toDataURL('image/jpeg', 0.8).split(',')[1]

            // If we're in a live session, just tell Gemini to look at the screen
            if (session.isLive) {
                 window.dispatchEvent(new CustomEvent('send-vision-frame', { detail: base64 }))
                // Send a client content message to prompt the tutor
                window.dispatchEvent(new CustomEvent('trigger-client-message', { 
                    detail: "Please review the homework image I just uploaded and tell me if my answers are correct."
                }))
                return
            }

            // Fallback for non-live mode: we shouldn't really hit this heavily but good to have
            const res = await fetch('/api/vision-chat', {
                 method: 'POST',
                 headers: { 'Content-Type': 'application/json' },
                 body: JSON.stringify({
                     message: "Please review this homework assignment and provide corrections or feedback.",
                     image_b64: base64,
                     history: []
                 })
            })
            if (res.ok) {
                const data = await res.json()
                appendTranscript('ai', data.response)
            } else {
                 appendTranscript('system', '❌ Error reviewing homework.')
            }

        } catch (err) {
            console.error('Homework analysis failed', err)
            appendTranscript('system', '❌ Error reviewing homework.')
        }
    }

    if (!book) {
        return (
            <main className="center-canvas empty-state">
                <div className="empty-content">
                    <span className="empty-icon">🖼️</span>
                    <h2>No Image Selected</h2>
                    <p className="text-muted">Upload an image from the library on the left.</p>
                </div>
            </main>
        )
    }

    return (
        <main className="center-canvas image-canvas">
            <div className="canvas-header">
                <div className="canvas-title">
                    <h2>{book.title}</h2>
                    <span className="tag tag-blue">Image Review</span>
                </div>
                <div className="canvas-actions">
                    <button className="btn btn-primary btn-sm" onClick={analyzeHomework}>
                        <span className="btn-icon">👁️</span>
                        Review Homework
                    </button>
                    <button className="btn btn-secondary btn-sm" onClick={() => onOpenVisualPanel()}>
                        <span className="btn-icon">🎨</span>
                        Explain Visually
                    </button>
                </div>
            </div>

            <div className="canvas-body">
                <div className="image-container">
                    {!imageLoaded && <div className="spinner image-loader" />}
                    <img 
                        ref={imageRef}
                        src={book.localUrl} 
                        alt={book.title}
                        className={`homework-image ${imageLoaded ? 'loaded' : ''}`}
                        onLoad={handleImageLoad}
                    />
                </div>
            </div>
            
            <div className="transcript-overlay">
                <div className="transcript-messages">
                    {transcript.slice(-3).map((msg, i) => (
                        <div key={i} className={`transcript-msg ${msg.role}`}>
                            <span className="msg-icon">
                                {msg.role === 'user' ? '👤' : msg.role === 'ai' ? '🤖' : '⚙️'}
                            </span>
                            <span className="msg-text">{msg.text}</span>
                        </div>
                    ))}
                </div>
            </div>
        </main>
    )
}
