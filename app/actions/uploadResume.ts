'use server'

import { writeFile } from 'fs/promises'
import { join } from 'path'

export async function uploadResume(formData: FormData) {
  const file = formData.get('resume') as File
  if (!file) {
    throw new Error('No file uploaded')
  }

  const bytes = await file.arrayBuffer()
  const buffer = Buffer.from(bytes)

  const path = join(process.cwd(), 'public', 'uploads', file.name)
  await writeFile(path, buffer)

  console.log(`File saved to ${path}`)
  return { success: true }
}
