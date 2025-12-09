export interface User {
  id: number
  username: string
  full_name: string
  role: string
  is_active: boolean
}

export interface Patient {
  id: number
  patient_code: string
  first_name: string
  last_name: string
  phone?: string
}

export interface ImagingStudy {
  id: number
  modality?: string
  study_date?: string
  description?: string
  dicom_file_path: string
}
