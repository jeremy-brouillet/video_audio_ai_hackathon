'use client'

import { useState } from 'react'
import { Button } from '@/components/ui/button'
import { Card, CardContent } from '@/components/ui/card'
import { PlayIcon, MonitorStopIcon as StopIcon } from 'lucide-react'
import { useAgents } from '../hooks/useAgents'

interface AgentWidgetProps {
  name: string
  description: string
  agentId: string
}

export default function AgentWidget({ name, description, agentId }: AgentWidgetProps) {
  const { activeAgent, startAgent, stopAgent } = useAgents()
  const [response, setResponse] = useState<string>('')

  const isActive = activeAgent === agentId
  const isDisabled = activeAgent !== null && activeAgent !== agentId

  const handleToggle = async () => {
    if (isActive) {
      stopAgent()
      setResponse('')
    } else {
      startAgent(agentId)
      setResponse('Analyzing resume...')
      // Simulating AI response generation
      setTimeout(() => {
        setResponse(`Hello! I'm the ${name}. I've analyzed your resume and I'm ready to provide feedback.`)
      }, 2000)
    }
  }

  return (
    <Card className="w-64 h-64 rounded-full flex flex-col items-center justify-center relative overflow-hidden">
      <div className="absolute inset-0 bg-gradient-to-br from-primary/20 to-primary-foreground/20"></div>
      <CardContent className="text-center z-10 flex flex-col items-center">
        <h3 className="font-bold text-lg mb-2">{name}</h3>
        <p className="text-sm text-muted-foreground mb-4">{description}</p>
        <Button
          onClick={handleToggle}
          disabled={isDisabled}
          variant="outline"
          size="icon"
          className={`rounded-full w-16 h-16 ${isActive ? 'bg-red-500 hover:bg-red-600' : 'bg-green-500 hover:bg-green-600'}`}
          aria-label={isActive ? `Stop ${name}` : `Start ${name}`}
        >
          {isActive ? (
            <StopIcon className="h-8 w-8 text-white" />
          ) : (
            <PlayIcon className="h-8 w-8 text-white" />
          )}
        </Button>
      </CardContent>
      {response && (
        <div className="absolute bottom-0 left-0 right-0 bg-background/80 p-2 text-xs text-center">
          {response}
        </div>
      )}
    </Card>
  )
}

