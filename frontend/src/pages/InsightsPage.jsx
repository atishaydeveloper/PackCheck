import React, { useMemo } from 'react';
import {
  Box,
  Container,
  Typography,
  Grid,
  Card,
  CardContent,
  Chip,
  Avatar,
  Paper,
  LinearProgress,
} from '@mui/material';
import {
  TrendingUp,
  CalendarToday,
  Restaurant,
  FitnessCenter,
  LocalFireDepartment,
  EmojiEvents,
} from '@mui/icons-material';
import { motion } from 'framer-motion';
import {
  LineChart,
  Line,
  BarChart,
  Bar,
  PieChart,
  Pie,
  Cell,
  AreaChart,
  Area,
  RadarChart,
  Radar,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts';
import { useAuth } from '../contexts/AuthContext';
import { useGamification } from '../contexts/GamificationContext';
import { gradients } from '../theme';

const InsightsPage = () => {
  const { user } = useAuth();
  const { gamification } = useGamification();

  // Generate weekly data
  const weeklyData = useMemo(() => {
    const days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];
    return days.map((day, index) => {
      const baseCalories = 2000;
      const variance = Math.random() * 500 - 250;
      return {
        day,
        calories: Math.round(baseCalories + variance),
        protein: Math.round(120 + Math.random() * 40),
        carbs: Math.round(250 + Math.random() * 100),
        fats: Math.round(60 + Math.random() * 30),
        goal: baseCalories,
      };
    });
  }, []);

  // Monthly calories trend
  const monthlyData = useMemo(() => {
    const weeks = ['Week 1', 'Week 2', 'Week 3', 'Week 4'];
    return weeks.map((week) => ({
      week,
      avgCalories: Math.round(1900 + Math.random() * 300),
      avgProtein: Math.round(110 + Math.random() * 30),
      scans: Math.round(15 + Math.random() * 10),
    }));
  }, []);

  // Macronutrient breakdown
  const macroData = useMemo(() => {
    const totalCalories = 2200;
    return [
      { name: 'Protein', value: 550, calories: 550, color: '#10b981' }, // 25%
      { name: 'Carbs', value: 1100, calories: 1100, color: '#6366f1' }, // 50%
      { name: 'Fats', value: 550, calories: 550, color: '#f59e0b' }, // 25%
    ];
  }, []);

  // Nutrition goals radar
  const goalsData = useMemo(() => {
    return [
      { metric: 'Calories', value: 95, fullMark: 100 },
      { metric: 'Protein', value: 110, fullMark: 100 },
      { metric: 'Carbs', value: 88, fullMark: 100 },
      { metric: 'Fats', value: 92, fullMark: 100 },
      { metric: 'Fiber', value: 75, fullMark: 100 },
      { metric: 'Sodium', value: 85, fullMark: 100 },
    ];
  }, []);

  // Scan activity by time of day
  const scanActivityData = useMemo(() => {
    return [
      { time: '6-9 AM', scans: 5 },
      { time: '9-12 PM', scans: 12 },
      { time: '12-3 PM', scans: 20 },
      { time: '3-6 PM', scans: 8 },
      { time: '6-9 PM', scans: 15 },
      { time: '9-12 AM', scans: 3 },
    ];
  }, []);

  const stats = [
    {
      label: 'Total Scans',
      value: gamification?.stats?.totalScans || 0,
      icon: <Restaurant />,
      color: '#6366f1',
      gradient: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    },
    {
      label: 'Current Streak',
      value: `${gamification?.streak || 0} days`,
      icon: <LocalFireDepartment />,
      color: '#f59e0b',
      gradient: 'linear-gradient(135deg, #fa709a 0%, #fee140 100%)',
    },
    {
      label: 'Points Earned',
      value: gamification?.points || 0,
      icon: <EmojiEvents />,
      color: '#10b981',
      gradient: 'linear-gradient(135deg, #10b981 0%, #059669 100%)',
    },
    {
      label: 'Goals Met',
      value: `${gamification?.stats?.goalsMetDays || 0} days`,
      icon: <FitnessCenter />,
      color: '#ec4899',
      gradient: 'linear-gradient(135deg, #ec4899 0%, #f43f5e 100%)',
    },
  ];

  return (
    <Container maxWidth="xl" sx={{ py: 4 }}>
      {/* Header */}
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" fontWeight="bold" gutterBottom>
          Nutrition Insights & Analytics
        </Typography>
        <Typography variant="body1" color="text.secondary">
          Visualize your nutrition journey with interactive charts and data
        </Typography>
      </Box>

      {/* Stats Cards */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        {stats.map((stat, index) => (
          <Grid item xs={12} sm={6} md={3} key={index}>
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: index * 0.1 }}
            >
              <Card
                sx={{
                  background: stat.gradient,
                  color: '#fff',
                  height: '100%',
                  position: 'relative',
                  overflow: 'hidden',
                  '&:hover': {
                    transform: 'translateY(-5px)',
                    boxShadow: '0 10px 30px rgba(0,0,0,0.2)',
                  },
                  transition: 'all 0.3s',
                }}
              >
                <CardContent>
                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                    <Avatar
                      sx={{
                        bgcolor: 'rgba(255,255,255,0.2)',
                        width: 56,
                        height: 56,
                      }}
                    >
                      {stat.icon}
                    </Avatar>
                    <Box>
                      <Typography variant="h4" fontWeight="bold">
                        {stat.value}
                      </Typography>
                      <Typography variant="body2" sx={{ opacity: 0.9 }}>
                        {stat.label}
                      </Typography>
                    </Box>
                  </Box>
                </CardContent>
              </Card>
            </motion.div>
          </Grid>
        ))}
      </Grid>

      {/* Weekly Calories & Macros */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} lg={8}>
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.6 }}
          >
            <Card sx={{ p: 3 }}>
              <Typography variant="h6" fontWeight="bold" gutterBottom>
                Weekly Calorie Intake
              </Typography>
              <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
                Track your daily calories vs. your goal
              </Typography>
              <ResponsiveContainer width="100%" height={300}>
                <AreaChart data={weeklyData}>
                  <defs>
                    <linearGradient id="colorCalories" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#6366f1" stopOpacity={0.8} />
                      <stop offset="95%" stopColor="#6366f1" stopOpacity={0} />
                    </linearGradient>
                  </defs>
                  <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
                  <XAxis dataKey="day" stroke="#6b7280" />
                  <YAxis stroke="#6b7280" />
                  <Tooltip
                    contentStyle={{
                      backgroundColor: '#fff',
                      border: '1px solid #e5e7eb',
                      borderRadius: '8px',
                    }}
                  />
                  <Legend />
                  <Area
                    type="monotone"
                    dataKey="calories"
                    stroke="#6366f1"
                    fillOpacity={1}
                    fill="url(#colorCalories)"
                    strokeWidth={2}
                  />
                  <Line
                    type="monotone"
                    dataKey="goal"
                    stroke="#10b981"
                    strokeDasharray="5 5"
                    strokeWidth={2}
                    dot={false}
                  />
                </AreaChart>
              </ResponsiveContainer>
            </Card>
          </motion.div>
        </Grid>

        <Grid item xs={12} lg={4}>
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.6 }}
          >
            <Card sx={{ p: 3, height: '100%' }}>
              <Typography variant="h6" fontWeight="bold" gutterBottom>
                Macronutrient Split
              </Typography>
              <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                Today's macro distribution
              </Typography>
              <ResponsiveContainer width="100%" height={240}>
                <PieChart>
                  <Pie
                    data={macroData}
                    cx="50%"
                    cy="50%"
                    innerRadius={60}
                    outerRadius={90}
                    paddingAngle={5}
                    dataKey="value"
                    label={({ name, percent }) =>
                      `${name} ${(percent * 100).toFixed(0)}%`
                    }
                    labelLine={false}
                  >
                    {macroData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.color} />
                    ))}
                  </Pie>
                  <Tooltip />
                </PieChart>
              </ResponsiveContainer>
              <Box sx={{ mt: 2 }}>
                {macroData.map((macro, index) => (
                  <Box
                    key={index}
                    sx={{
                      display: 'flex',
                      justifyContent: 'space-between',
                      mb: 1,
                    }}
                  >
                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                      <Box
                        sx={{
                          width: 12,
                          height: 12,
                          borderRadius: '50%',
                          bgcolor: macro.color,
                        }}
                      />
                      <Typography variant="body2">{macro.name}</Typography>
                    </Box>
                    <Typography variant="body2" fontWeight="bold">
                      {macro.calories} cal
                    </Typography>
                  </Box>
                ))}
              </Box>
            </Card>
          </motion.div>
        </Grid>
      </Grid>

      {/* Weekly Macros Breakdown */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} lg={8}>
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.2 }}
          >
            <Card sx={{ p: 3 }}>
              <Typography variant="h6" fontWeight="bold" gutterBottom>
                Weekly Macronutrients
              </Typography>
              <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
                Your protein, carbs, and fats intake over the week
              </Typography>
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={weeklyData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
                  <XAxis dataKey="day" stroke="#6b7280" />
                  <YAxis stroke="#6b7280" />
                  <Tooltip
                    contentStyle={{
                      backgroundColor: '#fff',
                      border: '1px solid #e5e7eb',
                      borderRadius: '8px',
                    }}
                  />
                  <Legend />
                  <Bar dataKey="protein" fill="#10b981" radius={[8, 8, 0, 0]} />
                  <Bar dataKey="carbs" fill="#6366f1" radius={[8, 8, 0, 0]} />
                  <Bar dataKey="fats" fill="#f59e0b" radius={[8, 8, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </Card>
          </motion.div>
        </Grid>

        <Grid item xs={12} lg={4}>
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.3 }}
          >
            <Card sx={{ p: 3 }}>
              <Typography variant="h6" fontWeight="bold" gutterBottom>
                Nutrition Goals
              </Typography>
              <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
                Your adherence to daily targets
              </Typography>
              <ResponsiveContainer width="100%" height={280}>
                <RadarChart data={goalsData}>
                  <PolarGrid stroke="#e5e7eb" />
                  <PolarAngleAxis dataKey="metric" stroke="#6b7280" />
                  <PolarRadiusAxis stroke="#6b7280" />
                  <Radar
                    name="Achievement"
                    dataKey="value"
                    stroke="#6366f1"
                    fill="#6366f1"
                    fillOpacity={0.6}
                  />
                  <Tooltip />
                </RadarChart>
              </ResponsiveContainer>
            </Card>
          </motion.div>
        </Grid>
      </Grid>

      {/* Monthly Trends & Scan Activity */}
      <Grid container spacing={3}>
        <Grid item xs={12} md={6}>
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.4 }}
          >
            <Card sx={{ p: 3 }}>
              <Typography variant="h6" fontWeight="bold" gutterBottom>
                Monthly Trends
              </Typography>
              <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
                Average weekly performance
              </Typography>
              <ResponsiveContainer width="100%" height={250}>
                <LineChart data={monthlyData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
                  <XAxis dataKey="week" stroke="#6b7280" />
                  <YAxis yAxisId="left" stroke="#6b7280" />
                  <YAxis yAxisId="right" orientation="right" stroke="#6b7280" />
                  <Tooltip
                    contentStyle={{
                      backgroundColor: '#fff',
                      border: '1px solid #e5e7eb',
                      borderRadius: '8px',
                    }}
                  />
                  <Legend />
                  <Line
                    yAxisId="left"
                    type="monotone"
                    dataKey="avgCalories"
                    stroke="#6366f1"
                    strokeWidth={3}
                    dot={{ r: 5 }}
                  />
                  <Line
                    yAxisId="right"
                    type="monotone"
                    dataKey="scans"
                    stroke="#10b981"
                    strokeWidth={3}
                    dot={{ r: 5 }}
                  />
                </LineChart>
              </ResponsiveContainer>
            </Card>
          </motion.div>
        </Grid>

        <Grid item xs={12} md={6}>
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.5 }}
          >
            <Card sx={{ p: 3 }}>
              <Typography variant="h6" fontWeight="bold" gutterBottom>
                Scan Activity by Time
              </Typography>
              <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
                When you scan products most
              </Typography>
              <ResponsiveContainer width="100%" height={250}>
                <BarChart data={scanActivityData} layout="horizontal">
                  <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
                  <XAxis type="number" stroke="#6b7280" />
                  <YAxis dataKey="time" type="category" stroke="#6b7280" />
                  <Tooltip
                    contentStyle={{
                      backgroundColor: '#fff',
                      border: '1px solid #e5e7eb',
                      borderRadius: '8px',
                    }}
                  />
                  <Bar dataKey="scans" fill="#ec4899" radius={[0, 8, 8, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </Card>
          </motion.div>
        </Grid>
      </Grid>
    </Container>
  );
};

export default InsightsPage;
