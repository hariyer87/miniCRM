import { useEffect, useState } from 'react'
import { Typography, Paper, Table, TableHead, TableRow, TableCell, TableBody, TextField, Button, Stack } from '@mui/material'
import axios from 'axios'
import { Patient } from '../types/models'

interface Props {
  token: string
}

export default function PatientsPage({ token }: Props) {
  const [patients, setPatients] = useState<Patient[]>([])
  const [search, setSearch] = useState('')

  const load = async () => {
    const res = await axios.get('http://localhost:8000/patients', { params: { search }, headers: { Authorization: `Bearer ${token}` } })
    setPatients(res.data)
  }

  useEffect(() => { load() }, [])

  return (
    <Paper sx={{ p: 2 }}>
      <Stack direction="row" spacing={2} sx={{ mb: 2 }}>
        <TextField label="Search" value={search} onChange={e => setSearch(e.target.value)} />
        <Button variant="contained" onClick={load}>Search</Button>
      </Stack>
      <Typography variant="h6" gutterBottom>Patients</Typography>
      <Table>
        <TableHead>
          <TableRow>
            <TableCell>Code</TableCell>
            <TableCell>Name</TableCell>
            <TableCell>Phone</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {patients.map(p => (
            <TableRow key={p.id}>
              <TableCell>{p.patient_code}</TableCell>
              <TableCell>{p.first_name} {p.last_name}</TableCell>
              <TableCell>{p.phone}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </Paper>
  )
}
