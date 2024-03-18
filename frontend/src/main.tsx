import App from './App.tsx'
import './index.css'
import { createRoot } from 'react-dom/client'

const container = document.getElementById('app')
const root = createRoot(container!) // createRoot(container!) if you use TypeScript
root.render(<App />)
