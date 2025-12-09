import { ReactNode } from 'react'
import { AppBar, Toolbar, Typography, Button, Drawer, List, ListItem, ListItemText, Box } from '@mui/material'
import { Link } from 'react-router-dom'
import { User } from '../types/models'

interface Props {
  children: ReactNode
  user: User | null
  onLogout: () => void
}

const navItems = [
  { label: 'Dashboard', path: '/' },
  { label: 'Patients', path: '/patients' },
  { label: 'Imaging', path: '/imaging' },
]

export default function Layout({ children, user, onLogout }: Props) {
  return (
    <Box sx={{ display: 'flex' }}>
      <AppBar position="fixed">
        <Toolbar>
          <Typography variant="h6" sx={{ flexGrow: 1 }}>
            MiniCRM Clinic
          </Typography>
          {user && <Typography sx={{ mr: 2 }}>{user.full_name}</Typography>}
          <Button color="inherit" onClick={onLogout}>Logout</Button>
        </Toolbar>
      </AppBar>
      <Drawer variant="permanent" sx={{ width: 200, [`& .MuiDrawer-paper`]: { width: 200, marginTop: 8 } }}>
        <List>
          {navItems.map(item => (
            <ListItem button component={Link} to={item.path} key={item.path}>
              <ListItemText primary={item.label} />
            </ListItem>
          ))}
        </List>
      </Drawer>
      <Box component="main" sx={{ flexGrow: 1, p: 3, mt: 8, ml: 25 }}>
        {children}
      </Box>
    </Box>
  )
}
