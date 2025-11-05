import React, { useState, useEffect } from 'react';
import {
  Box, Grid, Paper, Typography, Button, TextField, Dialog, DialogTitle,
  DialogContent, DialogActions, MenuItem, IconButton, Chip, Card, CardContent
} from '@mui/material';
import { Add, Delete, Edit, LocalFireDepartment } from '@mui/icons-material';
import { useAuth } from '../contexts/AuthContext';

function TrackerPage() {
  const { user, updateDailyIntake, updateUser } = useAuth();
  const [selectedDate, setSelectedDate] = useState(new Date().toISOString().split('T')[0]);
  const [dayIntake, setDayIntake] = useState(null);
  const [openDialog, setOpenDialog] = useState(false);
  const [newItem, setNewItem] = useState({
    name: '',
    calories: '',
    protein: '',
    carbs: '',
    fat: ''
  });

  useEffect(() => {
    if (user) {
      const intake = user.dailyIntake?.[selectedDate] || {
        calories: 0, protein: 0, carbs: 0, fat: 0, fiber: 0, sodium: 0, items: []
      };
      setDayIntake(intake);
    }
  }, [user, selectedDate]);

  const handleAddItem = () => {
    const nutrition = {
      calories: parseFloat(newItem.calories) || 0,
      protein: parseFloat(newItem.protein) || 0,
      carbohydrates: parseFloat(newItem.carbs) || 0,
      fat: parseFloat(newItem.fat) || 0
    };

    updateDailyIntake(selectedDate, nutrition);
    setNewItem({ name: '', calories: '', protein: '', carbs: '', fat: '' });
    setOpenDialog(false);
  };

  if (!dayIntake) return null;

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h4" fontWeight="bold">
          Daily Tracker
        </Typography>
        <Button variant="contained" startIcon={<Add />} onClick={() => setOpenDialog(true)}>
          Add Entry
        </Button>
      </Box>

      <TextField
        type="date"
        value={selectedDate}
        onChange={(e) => setSelectedDate(e.target.value)}
        sx={{ mb: 3 }}
      />

      <Grid container spacing={3}>
        <Grid item xs={12} md={8}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>Today's Entries</Typography>
            {dayIntake.items.length === 0 ? (
              <Typography color="text.secondary">No items logged yet</Typography>
            ) : (
              dayIntake.items.map((item, idx) => (
                <Card key={idx} sx={{ mb: 2 }}>
                  <CardContent>
                    <Typography variant="body1">
                      {new Date(item.timestamp).toLocaleTimeString()}
                    </Typography>
                    <Box sx={{ display: 'flex', gap: 1, mt: 1, flexWrap: 'wrap' }}>
                      <Chip label={`${item.nutrition.calories || 0} kcal`} size="small" />
                      <Chip label={`${item.nutrition.protein || 0}g protein`} size="small" />
                      <Chip label={`${item.nutrition.carbohydrates || 0}g carbs`} size="small" />
                    </Box>
                  </CardContent>
                </Card>
              ))
            )}
          </Paper>
        </Grid>

        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>Summary</Typography>
            <Box sx={{ mt: 2 }}>
              <Typography>Calories: {dayIntake.calories.toFixed(0)} / {user.dailyGoals.calories}</Typography>
              <Typography>Protein: {dayIntake.protein.toFixed(0)}g / {user.dailyGoals.protein}g</Typography>
              <Typography>Carbs: {dayIntake.carbs.toFixed(0)}g / {user.dailyGoals.carbs}g</Typography>
              <Typography>Fat: {dayIntake.fat.toFixed(0)}g / {user.dailyGoals.fat}g</Typography>
            </Box>
          </Paper>
        </Grid>
      </Grid>

      <Dialog open={openDialog} onClose={() => setOpenDialog(false)} maxWidth="sm" fullWidth>
        <DialogTitle>Add Food Entry</DialogTitle>
        <DialogContent>
          <TextField
            fullWidth
            label="Food Name"
            value={newItem.name}
            onChange={(e) => setNewItem({...newItem, name: e.target.value})}
            margin="normal"
          />
          <Grid container spacing={2} sx={{ mt: 1 }}>
            <Grid item xs={6}>
              <TextField
                fullWidth
                label="Calories"
                type="number"
                value={newItem.calories}
                onChange={(e) => setNewItem({...newItem, calories: e.target.value})}
              />
            </Grid>
            <Grid item xs={6}>
              <TextField
                fullWidth
                label="Protein (g)"
                type="number"
                value={newItem.protein}
                onChange={(e) => setNewItem({...newItem, protein: e.target.value})}
              />
            </Grid>
            <Grid item xs={6}>
              <TextField
                fullWidth
                label="Carbs (g)"
                type="number"
                value={newItem.carbs}
                onChange={(e) => setNewItem({...newItem, carbs: e.target.value})}
              />
            </Grid>
            <Grid item xs={6}>
              <TextField
                fullWidth
                label="Fat (g)"
                type="number"
                value={newItem.fat}
                onChange={(e) => setNewItem({...newItem, fat: e.target.value})}
              />
            </Grid>
          </Grid>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpenDialog(false)}>Cancel</Button>
          <Button onClick={handleAddItem} variant="contained">Add</Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
}

export default TrackerPage;
