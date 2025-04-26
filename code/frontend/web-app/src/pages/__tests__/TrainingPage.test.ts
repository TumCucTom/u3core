import { mount } from '@vue/test-utils'
import { describe, it, expect, vi, beforeEach } from 'vitest'
import TrainingPage from '../TrainingPage.vue'

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
    expect(wrapper.vm.activeTab).toBe('uploadData')
  })

  it('switches to "Upload Logs" tab', async () => {
    wrapper.vm.activeTab = 'uploadLogs'
    await wrapper.vm.$nextTick()
    expect(wrapper.vm.activeTab).toBe('uploadLogs')
  })

  it('handles file upload simulation', async () => {
    const fakeFile = new File(['dummy content'], 'test-image.png', { type: 'image/png' })

    await wrapper.vm.handleFileChange({ target: { files: [fakeFile] } })

    expect(wrapper.vm.uploadedFiles.length).toBe(1)
    expect(wrapper.vm.uploadedFiles[0].name).toBe('test-image.png')
    expect(wrapper.vm.uploadedFiles[0].status).toBe('uploading' || 'pending')
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
    wrapper.vm.uploadedFiles = [file]
    wrapper.vm.startTagEdit(file.id)
    wrapper.vm.newTag = 'animal'
    await wrapper.vm.addTag(file)

    expect(file.tags).toContain('animal')
    expect(wrapper.vm.editingFileId).toBe(null)
  })

  it('batch adds a tag to selected files', async () => {
    wrapper.vm.uploadedFiles = [
      { id: 1, tags: [] },
      { id: 2, tags: [] }
    ]
    wrapper.vm.selectedFiles = [1, 2]
    wrapper.vm.batchTag = 'wildlife'

    await wrapper.vm.addBatchTag()

    expect(wrapper.vm.uploadedFiles[0].tags).toContain('wildlife')
    expect(wrapper.vm.uploadedFiles[1].tags).toContain('wildlife')
    expect(wrapper.vm.selectedFiles.length).toBe(0)
  })

  it('deletes selected files in batch', async () => {
    wrapper.vm.uploadedFiles = [
      { id: 1, tags: [] },
      { id: 2, tags: [] }
    ]
    wrapper.vm.selectedFiles = [1]

    vi.stubGlobal('confirm', vi.fn(() => true)) // Auto-confirm dialog

    await wrapper.vm.deleteSelectedFiles()

    expect(wrapper.vm.uploadedFiles.length).toBe(1)
    expect(wrapper.vm.uploadedFiles[0].id).toBe(2)
  })

  it('opens training modal and submits new model log', async () => {
    wrapper.vm.uploadedFiles = [{ id: 1, name: 'file1.png' }]
    wrapper.vm.modelVersion = 'v1.0'
    wrapper.vm.siteId = 'Site A'

    await wrapper.vm.submitModelTraining()

    expect(wrapper.vm.uploadLogs.length).toBe(1)
    expect(wrapper.vm.uploadLogs[0].modelVersion).toBe('v1.0')
    expect(wrapper.vm.uploadLogs[0].siteId).toBe('Site A')
    expect(wrapper.vm.uploadLogs[0].files).toContain('file1.png')
  })

  it('shows "No training records yet" when no logs', () => {
    wrapper.vm.activeTab = 'uploadLogs'
    expect(wrapper.text()).toContain('No training records yet')
  })
})
