'use client'

import { createContext, useContext, useState, ReactNode } from 'react'

interface AgentsContextType {
  activeAgent: string | null
  isLoading: boolean
  startAgent: (agentId: string) => void
  stopAgent: () => void
}

const AgentsContext = createContext<AgentsContextType | undefined>(undefined)

export function AgentsProvider({ children }: { children: ReactNode }) {
  const [activeAgent, setActiveAgent] = useState<string | null>(null)
  const [isLoading, setIsLoading] = useState(false)

  const startAgent = (agentId: string) => {
    setIsLoading(true)
    setActiveAgent(agentId)
    setTimeout(() => setIsLoading(false), 1000) // Simulate loading
  }

  const stopAgent = () => {
    setActiveAgent(null)
    setIsLoading(false)
  }

  const contextValue: AgentsContextType = {
    activeAgent,
    isLoading,
    startAgent,
    stopAgent
  }

  return (
    <AgentsContext.Provider value={contextValue}>
      {children}
    </AgentsContext.Provider>
  )
}

export function useAgents() {
  const context = useContext(AgentsContext)
  if (context === undefined) {
    throw new Error('useAgents must be used within an AgentsProvider')
  }
  return context
}

