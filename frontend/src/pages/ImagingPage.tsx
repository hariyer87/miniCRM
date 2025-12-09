import { useEffect, useState } from 'react'
import { Paper, Typography, Table, TableHead, TableRow, TableCell, TableBody } from '@mui/material'
import axios from 'axios'
import { ImagingStudy } from '../types/models'

interface Props { token: string }

export default function ImagingPage({ token }: Props) {
  const [studies, setStudies] = useState<ImagingStudy[]>([])

  const load = async () => {
    const res = await axios.get('http://localhost:8000/imaging-studies', { headers: { Authorization: `Bearer ${token}` } })
    setStudies(res.data)
  }

  useEffect(() => { load() }, [])

  return (
    <Paper sx={{ p: 2 }}>
      <Typography variant="h6" gutterBottom>Imaging Studies</Typography>
      <Table>
        <TableHead>
          <TableRow>
            <TableCell>ID</TableCell>
            <TableCell>Modality</TableCell>
            <TableCell>Date</TableCell>
            <TableCell>Description</TableCell>
            <TableCell>File</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {studies.map(study => (
            <TableRow key={study.id}>
              <TableCell>{study.id}</TableCell>
              <TableCell>{study.modality}</TableCell>
              <TableCell>{study.study_date}</TableCell>
              <TableCell>{study.description}</TableCell>
              <TableCell><a href={study.dicom_file_path} target="_blank" rel="noreferrer">Download</a></TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </Paper>
  )
}
