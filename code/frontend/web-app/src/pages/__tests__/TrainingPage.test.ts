import { mount } from '@vue/test-utils'
import { describe, it, expect, vi, beforeEach } from 'vitest'
import TrainingPage from '../TrainingPage.vue'
import axios from 'axios'
import { Quasar } from 'quasar'


const wrapper = mount(TrainingPage, {
  global: {
    plugins: [Quasar],
  }
})

vi.mock('axios')

describe('TrainingPage.vue', () => {
  let wrapper: ReturnType<typeof mount>

  beforeEach(() => {
    wrapper = mount(TrainingPage, {
      global: {
        stubs: [
          'q-page', 'q-btn', 'q-card', 'q-dialog', 'q-input', 'q-icon',
          'q-checkbox', 'q-item', 'q-item-section', 'q-badge', 'q-chip', 'q-linear-progress', 'q-tooltip', 'q-select'
        ]
      }
    })
  })

  it('renders main title and upload button', () => {
    expect(wrapper.text()).toContain('Upload Training Data')
    expect(wrapper.text()).toContain('Upload Data')
    expect(wrapper.text()).toContain('Upload logs')
  })

  it('defaults to "Upload Data" tab', () => {
    expect((wrapper.vm as any).activeTab).toBe('uploadData')
  })

  it('switches to "Upload Logs" tab', async () => {
    (wrapper.vm as any).activeTab = 'uploadLogs'
    await (wrapper.vm as any).$nextTick()
    expect((wrapper.vm as any).activeTab).toBe('uploadLogs')
  })

  it('handles file upload simulation', async () => {
    const fakeFile = new File(['dummy content'], 'test-image.png', { type: 'image/png' })

    await (wrapper.vm as any).handleFileChange({ target: { files: [fakeFile] } })

    expect((wrapper.vm as any).uploadedFiles.length).toBe(1)
    expect((wrapper.vm as any).uploadedFiles[0].name).toBe('test-image.png')
    expect((wrapper.vm as any).uploadedFiles[0].status).toBe('uploading' || 'pending')
  })

  it('adds a tag to an uploaded file', async () => {
    const file = {
      id: 1,
      name: 'test-image.png',
      type: 'PNG',
      size: 5000,
      progress: 100,
      status: 'completed',
      raw: {},
      tags: []
    }
    (wrapper.vm as any).uploadedFiles = [file]
    (wrapper.vm as any).startTagEdit(file.id)
    (wrapper.vm as any).newTag = 'animal'
    await (wrapper.vm as any).addTag(file)

    expect(file.tags).toContain('animal')
    expect((wrapper.vm as any).editingFileId).toBe(null)
  })

  it('batch adds a tag to selected files', async () => {
    (wrapper.vm as any).uploadedFiles = [
      { id: 1, tags: [] },
      { id: 2, tags: [] }
    ]
    (wrapper.vm as any).selectedFiles = [1, 2]
    ((wrapper.vm as any) as any).batchTag = 'wildlife'

    await (wrapper.vm as any).addBatchTag()

    expect(((wrapper.vm as any) as any).uploadedFiles[0].tags).toContain('wildlife')
    expect((wrapper.vm as any).uploadedFiles[1].tags).toContain('wildlife')
    expect((wrapper.vm as any).selectedFiles.length).toBe(0)
  })

  it('deletes selected files in batch', async () => {
    (wrapper.vm as any).uploadedFiles = [
      { id: 1, tags: [] },
      { id: 2, tags: [] }
    ]
    (wrapper.vm as any).selectedFiles = [1]

    vi.stubGlobal('confirm', vi.fn(() => true)) // Auto-confirm dialog

    await (wrapper.vm as any).deleteSelectedFiles()

    expect((wrapper.vm as any).uploadedFiles.length).toBe(1)
    expect((wrapper.vm as any).uploadedFiles[0].id).toBe(2)
  })

  it('opens training modal and submits new model log', async () => {
    (wrapper.vm as any).uploadedFiles = [{ id: 1, name: 'file1.png' }]
    (wrapper.vm as any).modelVersion = 'v1.0'
    (wrapper.vm as any).siteId = 'Site A'

    await (wrapper.vm as any).submitModelTraining()

    expect((wrapper.vm as any).uploadLogs.length).toBe(1)
    expect((wrapper.vm as any).uploadLogs[0].modelVersion).toBe('v1.0')
    expect((wrapper.vm as any).uploadLogs[0].siteId).toBe('Site A')
    expect((wrapper.vm as any).uploadLogs[0].files).toContain('file1.png')
  })

  it('shows "No training records yet" when no logs', () => {
    (wrapper.vm as any).activeTab = 'uploadLogs'
    expect(wrapper.text()).toContain('No training records yet')
  })
})
