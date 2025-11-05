import React, { useState } from 'react';
import {
  Box, Typography, Paper, TextField, Button, Grid, MenuItem, Divider, Alert
} from '@mui/material';
import { Save } from '@mui/icons-material';
import { useAuth } from '../contexts/AuthContext';

function ProfilePage() {
  const { user, updateUser } = useAuth();
  const [profile, setProfile] = useState({
    name: user?.name || '',
    weight: user?.weight || '',
    height: user?.height || '',
    age: user?.age || '',
    fitnessGoal: user?.fitnessGoal || 'maintain'
  });
  const [goals, setGoals] = useState(user?.dailyGoals || {
    calories: 2000, protein: 50, carbs: 250, fat: 70
  });
  const [saved, setSaved] = useState(false);

  const handleSave = () => {
    updateUser({ ...profile, dailyGoals: goals });
    setSaved(true);
    setTimeout(() => setSaved(false), 3000);
  };

  return (
    <Box>
      <Typography variant="h4" fontWeight="bold" gutterBottom>
        Profile Settings
      </Typography>

      <Paper sx={{ p: 3, mb: 3 }}>
        <Typography variant="h6" gutterBottom>Personal Information</Typography>
        <Grid container spacing={2}>
          <Grid item xs={12} sm={6}>
            <TextField fullWidth label="Name" value={profile.name}
              onChange={(e) => setProfile({...profile, name: e.target.value})} />
          </Grid>
          <Grid item xs={12} sm={6}>
            <TextField fullWidth label="Age" type="number" value={profile.age}
              onChange={(e) => setProfile({...profile, age: e.target.value})} />
          </Grid>
          <Grid item xs={12} sm={6}>
            <TextField fullWidth label="Weight (kg)" type="number" value={profile.weight}
              onChange={(e) => setProfile({...profile, weight: e.target.value})} />
          </Grid>
          <Grid item xs={12} sm={6}>
            <TextField fullWidth label="Height (cm)" type="number" value={profile.height}
              onChange={(e) => setProfile({...profile, height: e.target.value})} />
          </Grid>
          <Grid item xs={12}>
            <TextField select fullWidth label="Fitness Goal" value={profile.fitnessGoal}
              onChange={(e) => setProfile({...profile, fitnessGoal: e.target.value})}>
              <MenuItem value="lose_weight">Lose Weight</MenuItem>
              <MenuItem value="maintain">Maintain Weight</MenuItem>
              <MenuItem value="gain_muscle">Gain Muscle</MenuItem>
              <MenuItem value="general_health">General Health</MenuItem>
            </TextField>
          </Grid>
        </Grid>
      </Paper>

      <Paper sx={{ p: 3, mb: 3 }}>
        <Typography variant="h6" gutterBottom>Daily Nutrition Goals</Typography>
        <Grid container spacing={2}>
          <Grid item xs={6} sm={3}>
            <TextField fullWidth label="Calories" type="number" value={goals.calories}
              onChange={(e) => setGoals({...goals, calories: parseInt(e.target.value)})} />
          </Grid>
          <Grid item xs={6} sm={3}>
            <TextField fullWidth label="Protein (g)" type="number" value={goals.protein}
              onChange={(e) => setGoals({...goals, protein: parseInt(e.target.value)})} />
          </Grid>
          <Grid item xs={6} sm={3}>
            <TextField fullWidth label="Carbs (g)" type="number" value={goals.carbs}
              onChange={(e) => setGoals({...goals, carbs: parseInt(e.target.value)})} />
          </Grid>
          <Grid item xs={6} sm={3}>
            <TextField fullWidth label="Fat (g)" type="number" value={goals.fat}
              onChange={(e) => setGoals({...goals, fat: parseInt(e.target.value)})} />
          </Grid>
        </Grid>
      </Paper>

      <Button variant="contained" startIcon={<Save />} onClick={handleSave} size="large">
        Save Changes
      </Button>

      {saved && <Alert severity="success" sx={{ mt: 2 }}>Profile updated successfully!</Alert>}
    </Box>
  );
}

export default ProfilePage;
