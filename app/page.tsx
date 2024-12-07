import { Suspense } from 'react'
import FileUpload from './components/FileUpload'
import AgentWidget from './components/AgentWidget'
import { AgentsProvider } from './hooks/useAgents'

export default function Home() {
  return (
    <AgentsProvider>
      <main className="container mx-auto p-4">
        <h1 className="text-2xl font-bold mb-4">Resume Analyzer</h1>
        <Suspense fallback={<div>Loading...</div>}>
          <FileUpload />
        </Suspense>
        <div className="mt-8 flex flex-wrap justify-center gap-16">
          <AgentWidget
            name="Professional Agent"
            description="Formal feedback"
            agentId="professional"
          />
          <AgentWidget
            name="Casual Agent"
            description="Friendly insights"
            agentId="casual"
          />
        </div>
      </main>
    </AgentsProvider>
  )
}

