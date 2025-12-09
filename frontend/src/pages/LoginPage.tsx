import { useState } from 'react'
import { Container, TextField, Button, Typography, Paper, Box } from '@mui/material'
import axios from 'axios'
import { User } from '../types/models'

interface Props {
  onLogin: (token: string, user: User) => void
}

export default function LoginPage({ onLogin }: Props) {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      const form = new URLSearchParams({ username, password })
      const res = await axios.post('http://localhost:8000/auth/login', form)
      onLogin(res.data.access_token, res.data.user)
    } catch (err) {
      setError('Invalid credentials')
    }
  }

  return (
    <Container maxWidth="sm" sx={{ mt: 8 }}>
      <Paper sx={{ p: 4 }}>
        <Typography variant="h5" gutterBottom>MiniCRM Login</Typography>
        <Box component="form" onSubmit={handleSubmit}>
          <TextField fullWidth label="Username" margin="normal" value={username} onChange={e => setUsername(e.target.value)} />
          <TextField fullWidth label="Password" type="password" margin="normal" value={password} onChange={e => setPassword(e.target.value)} />
          {error && <Typography color="error">{error}</Typography>}
          <Button type="submit" variant="contained" fullWidth sx={{ mt: 2 }}>Login</Button>
        </Box>
      </Paper>
    </Container>
  )
}
