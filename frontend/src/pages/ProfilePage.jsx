import React, { useState } from 'react';
import {
  Box,
  Typography,
  Paper,
  TextField,
  Button,
  Grid,
  MenuItem,
  Divider,
  Alert
} from '@mui/material';
import { Save } from '@mui/icons-material';

function ProfilePage() {
  const [profile, setProfile] = useState({
    userId: 'user123',
    fitnessGoal: 'muscle_building',
    weight: 70,
    height: 175,
    age: 25,
    gender: 'male'
  });

  const [saved, setSaved] = useState(false);

  const handleChange = (field) => (event) => {
    setProfile({ ...profile, [field]: event.target.value });
  };

  const handleSave = () => {
    // Would save to API in production
    console.log('Saving profile:', profile);
    setSaved(true);
    setTimeout(() => setSaved(false), 3000);
  };

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Profile Settings
      </Typography>
      <Typography variant="body1" color="text.secondary" paragraph>
        Configure your fitness goals and body metrics for personalized recommendations
      </Typography>

      <Paper elevation={3} sx={{ p: 3 }}>
        <Typography variant="h6" gutterBottom>
          Fitness Goals
        </Typography>

        <Grid container spacing={3}>
          <Grid item xs={12}>
            <TextField
              select
              fullWidth
              label="Fitness Goal"
              value={profile.fitnessGoal}
              onChange={handleChange('fitnessGoal')}
            >
              <MenuItem value="muscle_building">Muscle Building</MenuItem>
              <MenuItem value="weight_loss">Weight Loss</MenuItem>
              <MenuItem value="maintenance">Maintenance</MenuItem>
            </TextField>
          </Grid>
        </Grid>

        <Divider sx={{ my: 3 }} />

        <Typography variant="h6" gutterBottom>
          Body Metrics
        </Typography>

        <Grid container spacing={3}>
          <Grid item xs={12} sm={6}>
            <TextField
              fullWidth
              type="number"
              label="Weight (kg)"
              value={profile.weight}
              onChange={handleChange('weight')}
            />
          </Grid>
          <Grid item xs={12} sm={6}>
            <TextField
              fullWidth
              type="number"
              label="Height (cm)"
              value={profile.height}
              onChange={handleChange('height')}
            />
          </Grid>
          <Grid item xs={12} sm={6}>
            <TextField
              fullWidth
              type="number"
              label="Age"
              value={profile.age}
              onChange={handleChange('age')}
            />
          </Grid>
          <Grid item xs={12} sm={6}>
            <TextField
              select
              fullWidth
              label="Gender"
              value={profile.gender}
              onChange={handleChange('gender')}
            >
              <MenuItem value="male">Male</MenuItem>
              <MenuItem value="female">Female</MenuItem>
              <MenuItem value="other">Other</MenuItem>
            </TextField>
          </Grid>
        </Grid>

        <Box sx={{ mt: 3 }}>
          <Button
            variant="contained"
            startIcon={<Save />}
            onClick={handleSave}
          >
            Save Profile
          </Button>
        </Box>

        {saved && (
          <Alert severity="success" sx={{ mt: 2 }}>
            Profile saved successfully!
          </Alert>
        )}
      </Paper>

      <Paper elevation={3} sx={{ p: 3, mt: 3 }}>
        <Typography variant="h6" gutterBottom>
          Calculated Daily Targets
        </Typography>
        <Typography variant="body2" color="text.secondary" paragraph>
          Based on your profile, here are your recommended daily nutrition targets:
        </Typography>

        <Grid container spacing={2}>
          <Grid item xs={12} sm={6} md={3}>
            <Box sx={{ p: 2, backgroundColor: '#f5f5f5', borderRadius: 1 }}>
              <Typography variant="caption" color="text.secondary">
                Calories
              </Typography>
              <Typography variant="h5" color="primary">
                2400
              </Typography>
              <Typography variant="caption">kcal/day</Typography>
            </Box>
          </Grid>
          <Grid item xs={12} sm={6} md={3}>
            <Box sx={{ p: 2, backgroundColor: '#f5f5f5', borderRadius: 1 }}>
              <Typography variant="caption" color="text.secondary">
                Protein
              </Typography>
              <Typography variant="h5" color="primary">
                140
              </Typography>
              <Typography variant="caption">g/day</Typography>
            </Box>
          </Grid>
          <Grid item xs={12} sm={6} md={3}>
            <Box sx={{ p: 2, backgroundColor: '#f5f5f5', borderRadius: 1 }}>
              <Typography variant="caption" color="text.secondary">
                Carbs
              </Typography>
              <Typography variant="h5" color="primary">
                240
              </Typography>
              <Typography variant="caption">g/day</Typography>
            </Box>
          </Grid>
          <Grid item xs={12} sm={6} md={3}>
            <Box sx={{ p: 2, backgroundColor: '#f5f5f5', borderRadius: 1 }}>
              <Typography variant="caption" color="text.secondary">
                Fat
              </Typography>
              <Typography variant="h5" color="primary">
                67
              </Typography>
              <Typography variant="caption">g/day</Typography>
            </Box>
          </Grid>
        </Grid>
      </Paper>
    </Box>
  );
}

export default ProfilePage;
