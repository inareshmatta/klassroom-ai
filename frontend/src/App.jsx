import { useState, useCallback, useEffect } from 'react'
import { AnimatePresence } from 'framer-motion'
import LeftPanel from './components/LeftPanel/LeftPanel'
import CenterCanvas from './components/CenterCanvas/CenterCanvas'
import ImageCanvas from './components/CenterCanvas/ImageCanvas'
import RightPanel from './components/RightPanel/RightPanel'
import VisualPanel from './components/VisualPanel/VisualPanel'
import AssessmentPanel from './components/AssessmentPanel/AssessmentPanel'
import CurriculumPlanner from './components/CurriculumPlanner/CurriculumPlanner'
import LandingPage from './components/LandingPage/LandingPage'
import TopBar from './components/TopBar'
import './App.css'

export default function App() {
  // Theme state
  const [theme, setTheme] = useState(() => localStorage.getItem('shivy_theme') || 'light')

  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme)
    localStorage.setItem('shivy_theme', theme)
    localStorage.setItem('klassroom_theme', theme)
  }, [theme])

  const toggleTheme = () => setTheme(prev => prev === 'light' ? 'dark' : 'light')

  // Landing page state
  const [hasEntered, setHasEntered] = useState(false)

  // Session state
  const [session, setSession] = useState({
    isLive: false,
    orbState: 'idle',
  })

  // Multi-book library
  const [books, setBooks] = useState([])               // Array of book objects
  const [activeBookId, setActiveBookId] = useState(null) // Currently selected book
  const activeBook = books.find(b => b.id === activeBookId) || null

  // Page state (per book)
  const [currentPage, setCurrentPage] = useState(1)
  const [pageAnalysis, setPageAnalysis] = useState(null)


  // Visual panel state
  const [visualPanel, setVisualPanel] = useState({
    open: false,
    sessionId: null,
    currentImage: null,
    history: [],
  })

  // Assessment panel state
  const [assessmentOpen, setAssessmentOpen] = useState(false)
  const [assessmentData, setAssessmentData] = useState(null)

  // Curriculum Planner state
  const [plannerOpen, setPlannerOpen] = useState(false)

  // Discipline & Dictation
  const [disciplineLogs, setDisciplineLogs] = useState([])
  const [dictationWords, setDictationWords] = useState([])

  // Sidebar Toggle State
  const [leftPanelOpen, setLeftPanelOpen] = useState(true)
  const [rightPanelOpen, setRightPanelOpen] = useState(true)

  // Tutor settings
  const [settings, setSettings] = useState({
    voice: 'Kore',
    affectiveMode: true,
    bargeIn: true,
  })

  // Transcript
  const [transcript, setTranscript] = useState([])

  const appendTranscript = useCallback((role, text) => {
    setTranscript(prev => [...prev.slice(-100), { role, text, ts: Date.now() }])
  }, [])

  // Book management
  const addBook = useCallback((bookData) => {
    const id = crypto.randomUUID()
    const newBook = { ...bookData, id }
    setBooks(prev => [...prev, newBook])
    setActiveBookId(id)
    setCurrentPage(1)
    setPageAnalysis(null)

  }, [])

  const removeBook = useCallback((bookId) => {
    setBooks(prev => prev.filter(b => b.id !== bookId))
    if (activeBookId === bookId) {
      setActiveBookId(null)
      setPageAnalysis(null)

    }
  }, [activeBookId])

  const selectBook = useCallback((bookId) => {
    setActiveBookId(bookId)
    setCurrentPage(1)
    setPageAnalysis(null)

  }, [])

  // Visual panel
  const openVisualPanel = useCallback((image = null, initialTopic = '') => {
    setVisualPanel(prev => ({
      ...prev,
      open: true,
      sessionId: prev.sessionId || crypto.randomUUID(),
      currentImage: image || prev.currentImage,
      topic: initialTopic,
    }))
  }, [])

  const closeVisualPanel = useCallback(() => {
    setVisualPanel(prev => ({ ...prev, open: false }))
  }, [])

  const onVisualGenerated = useCallback((imageData) => {
    setVisualPanel(prev => ({
      ...prev,
      open: true,
      currentImage: imageData,
      history: [...prev.history, imageData],
    }))
  }, [])

  // Global loading state for agent tools
  const [agentLoadingMessage, setAgentLoadingMessage] = useState(null)

  // Listen for agent tool results to automatically open corresponding panels
  useEffect(() => {
    const handleToolStart = (e) => {
      const { tool } = e.detail
      const friendlyName = {
        generate_quiz: 'Generating Quiz...',
        lookup_word: 'Looking up definition...',
        generate_visual: 'Creating visual diagram...',
        create_bookmark: 'Saving to Knowledge Vault...',
        generate_flashcards: 'Creating flashcards...',
      }[tool] || 'Agent is working...'
      
      setAgentLoadingMessage(friendlyName)
    }

    const handleToolResult = (e) => {
      // Clear loading state
      setAgentLoadingMessage(null)

      const { tool, result, args } = e.detail
      if (tool === 'generate_visual') {
        // Open the visual panel with the generated image
        if (result && result.image_b64) {
          onVisualGenerated(result)
        } else {
          openVisualPanel(null, args?.topic || '')
        }
      } else if (tool === 'generate_quiz' || tool === 'generate_flashcards') {
        // Open the assessment panel when a quiz or flashcards are generated
        setAssessmentData(result)
        setAssessmentOpen(true)
      } else if (tool === 'lookup_word') {
        // Dispatch a custom event so CenterCanvas can show the tooltip
        window.dispatchEvent(new CustomEvent('voice-lookup-word', {
          detail: { word: args?.word || '', definition: result?.definition || result }
        }))
      } else if (tool === 'log_discipline') {
        setDisciplineLogs(prev => [...prev.slice(-4), { ts: Date.now(), issue: args?.issue, note: args?.note }])
      } else if (tool === 'save_dictation_words') {
        setDictationWords(args?.words || [])
      }
    }

    window.addEventListener('agent-tool-start', handleToolStart)
    window.addEventListener('agent-tool-result', handleToolResult)
    return () => {
      window.removeEventListener('agent-tool-start', handleToolStart)
      window.removeEventListener('agent-tool-result', handleToolResult)
    }
  }, [openVisualPanel, onVisualGenerated])

  if (!hasEntered) {
    return <LandingPage onEnter={() => setHasEntered(true)} theme={theme} toggleTheme={toggleTheme} />
  }

  return (
    <div className="app-shell">
      <TopBar
        books={books}
        session={session}
        theme={theme}
        toggleTheme={toggleTheme}
        onEndSession={() => setSession(s => ({ ...s, isLive: false, orbState: 'idle' }))}
      />

      <div className={`app-body ${!leftPanelOpen ? 'left-closed' : ''} ${!rightPanelOpen ? 'right-closed' : ''}`}>
        
        {/* Left Toggle Button (desktop only) */}
        <button 
          className="sidebar-toggle left-toggle" 
          onClick={() => setLeftPanelOpen(!leftPanelOpen)}
          title={leftPanelOpen ? "Collapse Menu" : "Expand Menu"}
        >
          {leftPanelOpen ? '◀' : '▶'}
        </button>

        <div className={`panel-container left-container ${!leftPanelOpen ? 'collapsed' : ''}`}>
          <LeftPanel
            session={session}
            setSession={setSession}
          books={books}
          activeBook={activeBook}
          addBook={addBook}
          removeBook={removeBook}
          selectBook={selectBook}
          settings={settings}
          setSettings={setSettings}
          pageAnalysis={pageAnalysis}
          onOpenVisualPanel={openVisualPanel}
          onOpenAssessment={() => setAssessmentOpen(true)}
            onOpenPlanner={() => setPlannerOpen(true)}
            appendTranscript={appendTranscript}
            currentPage={currentPage}
          />
        </div>

        {activeBook?.mimeType?.includes('image/') ? (
          <ImageCanvas
            book={activeBook}
            session={session}
            setSession={setSession}
            pageAnalysis={pageAnalysis}
            setPageAnalysis={setPageAnalysis}
            settings={settings}
            appendTranscript={appendTranscript}
            onVisualRequest={onVisualGenerated}
            onOpenVisualPanel={openVisualPanel}
            transcript={transcript}
          />
        ) : (
          <CenterCanvas
            book={activeBook}
            currentPage={currentPage}
            setCurrentPage={setCurrentPage}
            session={session}
            setSession={setSession}
            pageAnalysis={pageAnalysis}
            setPageAnalysis={setPageAnalysis}
            settings={settings}
            appendTranscript={appendTranscript}
            onVisualRequest={onVisualGenerated}
            onOpenVisualPanel={openVisualPanel}
            transcript={transcript}
          />
        )}

        {/* Right Toggle Button (desktop only) */}
        <button 
          className="sidebar-toggle right-toggle" 
          onClick={() => setRightPanelOpen(!rightPanelOpen)}
          title={rightPanelOpen ? "Collapse Vault" : "Expand Vault"}
        >
          {rightPanelOpen ? '▶' : '◀'}
        </button>

        <div className={`panel-container right-container ${!rightPanelOpen ? 'collapsed' : ''}`}>
          <RightPanel
            pageAnalysis={pageAnalysis}
            currentPage={currentPage}
            subject={activeBook?.subject || 'General'}
            appendTranscript={appendTranscript}
            onOpenAssessment={() => setAssessmentOpen(true)}
            disciplineLogs={disciplineLogs}
            dictationWords={dictationWords}
          />
        </div>
      </div>

      {agentLoadingMessage && (
        <div className="agent-loading-toast">
          <div className="spinner"></div>
          <span>{agentLoadingMessage}</span>
        </div>
      )}

      {/* Full-screen overlays */}
      <AnimatePresence>
        {visualPanel.open && (
          <VisualPanel
            {...visualPanel}
            subject={activeBook?.subject || 'General'}
            initialTopic={visualPanel.topic}
            onClose={closeVisualPanel}
            onVisualGenerated={onVisualGenerated}
          />
        )}
      </AnimatePresence>

      <AnimatePresence>
        {assessmentOpen && (
          <AssessmentPanel
            books={books}
            activeBook={activeBook}
            pageAnalysis={pageAnalysis}
            currentPage={currentPage}
            initialData={assessmentData}
            onClose={() => {
              setAssessmentOpen(false)
              setAssessmentData(null)
            }}
          />
        )}
      </AnimatePresence>

      <AnimatePresence>
        {plannerOpen && (
          <CurriculumPlanner
            books={books}
            onClose={() => setPlannerOpen(false)}
          />
        )}
      </AnimatePresence>
    </div>
  )
}
