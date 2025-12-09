import { Grid, Paper, Typography } from '@mui/material'

export default function Dashboard() {
  const cards = [
    { label: "Today's visits", value: 0 },
    { label: 'Pending samples', value: 0 },
    { label: 'In process', value: 0 },
    { label: 'Reports ready', value: 0 },
  ]

  return (
    <Grid container spacing={2}>
      {cards.map(card => (
        <Grid item xs={12} md={3} key={card.label}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="subtitle2">{card.label}</Typography>
            <Typography variant="h5">{card.value}</Typography>
          </Paper>
        </Grid>
      ))}
    </Grid>
  )
}
