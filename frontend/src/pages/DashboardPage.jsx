import React, { useState, useEffect } from 'react';
import {
  Box,
  Grid,
  Paper,
  Typography,
  Card,
  CardContent,
  LinearProgress,
  Chip,
  Button
} from '@mui/material';
import {
  TrendingUp,
  LocalFireDepartment,
  FitnessCenter,
  Restaurant,
  Water,
  Fastfood,
  Assessment,
  History,
  Add
} from '@mui/icons-material';
import { useAuth } from '../contexts/AuthContext';
import { useNavigate } from 'react-router-dom';
import GamificationBanner from '../components/GamificationBanner';
import { motion } from 'framer-motion';

function DashboardPage() {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [todayIntake, setTodayIntake] = useState(null);
  const [weeklyProgress, setWeeklyProgress] = useState([]);

  useEffect(() => {
    if (user) {
      const today = new Date().toISOString().split('T')[0];
      const intake = user.dailyIntake?.[today] || {
        calories: 0,
        protein: 0,
        carbs: 0,
        fat: 0,
        fiber: 0,
        sodium: 0,
        items: []
      };
      setTodayIntake(intake);

      // Calculate weekly progress
      const weekData = [];
      for (let i = 6; i >= 0; i--) {
        const date = new Date();
        date.setDate(date.getDate() - i);
        const dateKey = date.toISOString().split('T')[0];
        const dayIntake = user.dailyIntake?.[dateKey];
        weekData.push({
          date: dateKey,
          day: date.toLocaleDateString('en-US', { weekday: 'short' }),
          calories: dayIntake?.calories || 0,
          goal: user.dailyGoals.calories
        });
      }
      setWeeklyProgress(weekData);
    }
  }, [user]);

  if (!user) {
    return (
      <Box sx={{ textAlign: 'center', py: 8 }}>
        <Typography variant="h5" gutterBottom>
          Please log in to view your dashboard
        </Typography>
        <Button variant="contained" onClick={() => navigate('/login')}>
          Login
        </Button>
      </Box>
    );
  }

  if (!todayIntake) return null;

  const getProgress = (current, goal) => {
    return Math.min((current / goal) * 100, 100);
  };

  const getProgressColor = (percentage) => {
    if (percentage < 50) return 'error';
    if (percentage < 80) return 'warning';
    if (percentage <= 100) return 'success';
    return 'error';
  };

  const NutrientCard = ({ icon, label, current, goal, unit }) => {
    const progress = getProgress(current, goal);
    const color = getProgressColor(progress);

    return (
      <Card>
        <CardContent>
          <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
            {icon}
            <Typography variant="h6" sx={{ ml: 1 }}>
              {label}
            </Typography>
          </Box>
          <Typography variant="h4" fontWeight="bold">
            {current.toFixed(0)}
            <Typography component="span" variant="h6" color="text.secondary">
              /{goal}{unit}
            </Typography>
          </Typography>
          <LinearProgress
            variant="determinate"
            value={progress}
            color={color}
            sx={{ mt: 2, height: 8, borderRadius: 4 }}
          />
          <Typography variant="caption" color="text.secondary" sx={{ mt: 1, display: 'block' }}>
            {progress.toFixed(0)}% of daily goal
          </Typography>
        </CardContent>
      </Card>
    );
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      <Box>
        {/* Gamification Banner */}
        <GamificationBanner />

        {/* Header */}
        <Box sx={{ mb: 4 }}>
          <Typography variant="h4" fontWeight="bold" gutterBottom>
            Welcome back, {user.name}!
          </Typography>
          <Typography variant="body1" color="text.secondary">
            Track your nutrition goals and stay healthy
          </Typography>
        </Box>

      {/* Quick Actions */}
      <Grid container spacing={2} sx={{ mb: 4 }}>
        <Grid item xs={12} sm={4}>
          <Button
            fullWidth
            variant="contained"
            size="large"
            startIcon={<Add />}
            onClick={() => navigate('/scan')}
          >
            Scan New Product
          </Button>
        </Grid>
        <Grid item xs={12} sm={4}>
          <Button
            fullWidth
            variant="outlined"
            size="large"
            startIcon={<History />}
            onClick={() => navigate('/history')}
          >
            View History
          </Button>
        </Grid>
        <Grid item xs={12} sm={4}>
          <Button
            fullWidth
            variant="outlined"
            size="large"
            startIcon={<Assessment />}
            onClick={() => navigate('/tracker')}
          >
            Detailed Tracker
          </Button>
        </Grid>
      </Grid>

      {/* Today's Intake */}
      <Typography variant="h5" fontWeight="bold" gutterBottom sx={{ mb: 2 }}>
        Today's Nutrition
      </Typography>

      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} sm={6} md={4}>
          <NutrientCard
            icon={<LocalFireDepartment color="error" />}
            label="Calories"
            current={todayIntake.calories}
            goal={user.dailyGoals.calories}
            unit=" kcal"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={4}>
          <NutrientCard
            icon={<FitnessCenter color="primary" />}
            label="Protein"
            current={todayIntake.protein}
            goal={user.dailyGoals.protein}
            unit="g"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={4}>
          <NutrientCard
            icon={<Restaurant color="warning" />}
            label="Carbs"
            current={todayIntake.carbs}
            goal={user.dailyGoals.carbs}
            unit="g"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={4}>
          <NutrientCard
            icon={<Fastfood color="info" />}
            label="Fat"
            current={todayIntake.fat}
            goal={user.dailyGoals.fat}
            unit="g"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={4}>
          <NutrientCard
            icon={<Water color="success" />}
            label="Fiber"
            current={todayIntake.fiber}
            goal={user.dailyGoals.fiber}
            unit="g"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={4}>
          <Paper sx={{ p: 3 }}>
            <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
              <Restaurant />
              <Typography variant="h6" sx={{ ml: 1 }}>
                Items Logged
              </Typography>
            </Box>
            <Typography variant="h3" fontWeight="bold">
              {todayIntake.items.length}
            </Typography>
            <Typography variant="caption" color="text.secondary">
              products scanned today
            </Typography>
          </Paper>
        </Grid>
      </Grid>

      {/* Weekly Progress */}
      <Typography variant="h5" fontWeight="bold" gutterBottom sx={{ mb: 2 }}>
        Weekly Progress
      </Typography>

      <Paper sx={{ p: 3, mb: 4 }}>
        <Grid container spacing={2}>
          {weeklyProgress.map((day, index) => {
            const percentage = (day.calories / day.goal) * 100;
            const isToday = index === 6;

            return (
              <Grid item xs key={day.date}>
                <Box sx={{ textAlign: 'center' }}>
                  <Typography
                    variant="caption"
                    fontWeight={isToday ? 'bold' : 'normal'}
                    color={isToday ? 'primary' : 'text.secondary'}
                  >
                    {day.day}
                  </Typography>
                  <Box
                    sx={{
                      height: 120,
                      width: '100%',
                      bgcolor: '#f5f5f5',
                      borderRadius: 1,
                      mt: 1,
                      position: 'relative',
                      overflow: 'hidden'
                    }}
                  >
                    <Box
                      sx={{
                        position: 'absolute',
                        bottom: 0,
                        left: 0,
                        right: 0,
                        height: `${Math.min(percentage, 100)}%`,
                        bgcolor: percentage > 100 ? '#f44336' : '#4caf50',
                        transition: 'height 0.3s'
                      }}
                    />
                  </Box>
                  <Typography
                    variant="caption"
                    sx={{ mt: 1, display: 'block' }}
                  >
                    {day.calories}
                  </Typography>
                </Box>
              </Grid>
            );
          })}
        </Grid>
        <Typography variant="caption" color="text.secondary" sx={{ mt: 2, display: 'block', textAlign: 'center' }}>
          Daily calorie intake vs goal ({user.dailyGoals.calories} kcal)
        </Typography>
      </Paper>

      {/* Recent Scans */}
      {user.history && user.history.length > 0 && (
        <>
          <Typography variant="h5" fontWeight="bold" gutterBottom sx={{ mb: 2 }}>
            Recent Scans
          </Typography>
          <Grid container spacing={2}>
            {user.history.slice(0, 3).map((item) => (
              <Grid item xs={12} md={4} key={item.id}>
                <Card>
                  <CardContent>
                    <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start', mb: 2 }}>
                      <Typography variant="h6">
                        Product Scan
                      </Typography>
                      <Chip
                        label={item.compliance?.fssai_verification?.overall_compliance ? 'Compliant' : 'Check'}
                        color={item.compliance?.fssai_verification?.overall_compliance ? 'success' : 'warning'}
                        size="small"
                      />
                    </Box>
                    <Typography variant="body2" color="text.secondary" gutterBottom>
                      {new Date(item.timestamp).toLocaleDateString()} at{' '}
                      {new Date(item.timestamp).toLocaleTimeString()}
                    </Typography>
                    {item.extraction?.nutrition_data && (
                      <Box sx={{ mt: 2 }}>
                        <Typography variant="caption" color="text.secondary">
                          Nutrition (per serving):
                        </Typography>
                        <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap', mt: 1 }}>
                          {item.extraction.nutrition_data.protein && (
                            <Chip label={`${item.extraction.nutrition_data.protein}g protein`} size="small" />
                          )}
                          {item.extraction.nutrition_data.carbohydrates && (
                            <Chip label={`${item.extraction.nutrition_data.carbohydrates}g carbs`} size="small" />
                          )}
                        </Box>
                      </Box>
                    )}
                  </CardContent>
                </Card>
              </Grid>
            ))}
          </Grid>
        </>
      )}
      </Box>
    </motion.div>
  );
}

export default DashboardPage;
