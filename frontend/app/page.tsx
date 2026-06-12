'use client'

import { useMemo, useRef, useState } from 'react'
import { motion } from 'framer-motion'
import Hero from '@/components/Hero'
import InputSection from '@/components/InputSection'
import ReasoningSteps from '@/components/ReasoningSteps'
import Results from '@/components/Results'
import type { AnalysisResult } from '@/types'

const sampleResume = `Senior software engineer with 8 years of experience building customer-facing web apps, APIs, and automation tools. Core skills include React, TypeScript, Next.js, Node.js, Python, Flask, SQL, REST APIs, CI/CD, agile delivery, and stakeholder communication.`

const sampleJobDescription = `We are looking for an experienced full-stack engineer to own the product roadmap, design scalable web applications, build backend services in Python and Node.js, and collaborate with product and design teams. Required skills: React, Next.js, Flask, PostgreSQL, cloud deployment, GitHub Actions, strong problem solving, and team communication.`

export default function HomePage() {
  const [resume, setResume] = useState('')
  const [jobDescription, setJobDescription] = useState('')
  const [githubUsername, setGithubUsername] = useState('')
  const [resumeFileName, setResumeFileName] = useState<string | null>(null)
  const [result, setResult] = useState<AnalysisResult | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const resultsRef = useRef<HTMLDivElement | null>(null)

  const stats = useMemo(() => {
    if (!result) return null
    return {
      totalResumeSkills: result.resume_skills?.length ?? 0,
      totalRequiredSkills: result.required_skills?.length ?? 0,
      gapsFound: result.gap_skills?.length ?? 0,
    }
  }, [result])

  const apiUrl = process.env.NEXT_PUBLIC_API_URL ?? 'http://127.0.0.1:5000'

  const handleSubmit = async () => {
    setError(null)
    setResult(null)

    const fileInput = document.getElementById('resume-file') as HTMLInputElement | null
    const file = fileInput?.files?.[0] ?? null
    const resumeText = resume.trim()
    const jobDescText = jobDescription.trim()
    const gitUsername = githubUsername.trim()

    // Validate inputs
    if (!file && resumeText.length < 20 && gitUsername.length < 3) {
      setError('Please provide a resume (text, PDF, or GitHub profile) with sufficient content.')
      return
    }

    if (jobDescText.length < 50) {
      setError('Please provide a job description with at least 50 characters.')
      return
    }

    setLoading(true)
    try {
      let response
      if (file) {
        const form = new FormData()
        form.append('resume_file', file, file.name)
        form.append('job_description', jobDescText)
        if (gitUsername) {
          form.append('github_username', gitUsername)
        }

        response = await fetch(`${apiUrl}/api/analyze`, {
          method: 'POST',
          body: form,
        })
      } else {
        const payload: any = {
          job_description: jobDescText,
        }
        
        if (resumeText) {
          payload.resume_text = resumeText
        }
        
        if (gitUsername) {
          payload.github_username = gitUsername
        }
        
        response = await fetch(`${apiUrl}/api/analyze`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload),
        })
      }

      if (!response.ok) {
        const payload = await response.json()
        setError(payload.error || `Server error: ${response.status}`)
        console.error('API error:', payload)
        return
      }

      const payload = await response.json()
      setResult(payload)
      setTimeout(() => {
        resultsRef.current?.scrollIntoView({ behavior: 'smooth' })
      }, 100)
    } catch (err) {
      const msg = err instanceof Error ? err.message : 'Unknown error'
      setError(`Analysis failed: ${msg}. Ensure the backend is running on ${apiUrl}`)
      console.error('Submission error:', err)
    } finally {
      setLoading(false)
    }
  }

  const fillSample = () => {
    setResume(sampleResume)
    setJobDescription(sampleJobDescription)
    setError(null)
    setResumeFileName(null)
  }

  return (
    <main className="min-h-screen px-4 py-12 sm:px-6 lg:px-8">
      <div className="mx-auto max-w-7xl">
        <Hero />

        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.3 }}
          className="mt-16 sm:mt-20"
        >
          <InputSection
            resume={resume}
            jobDescription={jobDescription}
            githubUsername={githubUsername}
            onResumeChange={setResume}
            onJobDescriptionChange={setJobDescription}
            onGithubUsernameChange={setGithubUsername}
            onAnalyze={handleSubmit}
            onTrySample={fillSample}
            loading={loading}
            resumeLength={resume.length}
            jobDescriptionLength={jobDescription.length}
            resumeFileName={resumeFileName}
            onFileSelect={(file) => setResumeFileName(file ? file.name : null)}
          />
        </motion.div>

        {error ? (
          <motion.div
            initial={{ opacity: 0, y: 16, scale: 0.95 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            transition={{ type: 'spring', stiffness: 200 }}
            className="mt-8 rounded-2xl border border-rose-500/50 bg-gradient-to-r from-rose-500/20 to-rose-500/5 px-6 py-5 text-rose-100 backdrop-blur-sm font-medium"
            role="alert"
          >
            ❌ {error}
          </motion.div>
        ) : null}

        {loading && !result && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.4, delay: 0.3 }}
            className="mt-12 sm:mt-16"
          >
            <ReasoningSteps isVisible={true} />
          </motion.div>
        )}

        <div ref={resultsRef} className="mt-20 sm:mt-24 scroll-mt-24">
          {result ? <Results result={result} stats={stats} /> : null}
        </div>

        <motion.footer 
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.6, delay: 0.8 }}
          className="mt-24 border-t border-border/30 pt-8 text-center text-sm text-muted/60"
        >
          <p className="mb-2">✨ Built with GitHub Copilot for Microsoft Agents League Hackathon 2026</p>
          <p className="text-xs">Powered by LLaMA 3.3 70B • AI-Driven Skill Gap Analysis</p>
        </motion.footer>
      </div>
    </main>
  )
}
