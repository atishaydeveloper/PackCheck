import React from 'react';
import {
  Box,
  Typography,
  Grid,
  Card,
  CardContent,
  Paper
} from '@mui/material';
import {
  TrendingUp,
  LocalDining,
  FitnessCenter,
  CheckCircle
} from '@mui/icons-material';

function DashboardPage() {
  // Mock data - would come from API in production
  const stats = {
    totalScans: 45,
    verifiedProducts: 32,
    avgProtein: 18.5,
    compliantProducts: 38
  };

  const StatCard = ({ icon, title, value, subtitle }) => (
    <Card elevation={3}>
      <CardContent>
        <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
          {icon}
          <Typography variant="h6" sx={{ ml: 1 }}>
            {title}
          </Typography>
        </Box>
        <Typography variant="h3" color="primary" gutterBottom>
          {value}
        </Typography>
        <Typography variant="body2" color="text.secondary">
          {subtitle}
        </Typography>
      </CardContent>
    </Card>
  );

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Dashboard
      </Typography>
      <Typography variant="body1" color="text.secondary" paragraph>
        Your nutrition tracking and scanning statistics
      </Typography>

      <Grid container spacing={3}>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            icon={<TrendingUp color="primary" />}
            title="Total Scans"
            value={stats.totalScans}
            subtitle="Labels scanned"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            icon={<CheckCircle color="success" />}
            title="Verified"
            value={stats.verifiedProducts}
            subtitle="FSSAI compliant"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            icon={<FitnessCenter color="primary" />}
            title="Avg Protein"
            value={`${stats.avgProtein}g`}
            subtitle="Per product"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            icon={<LocalDining color="primary" />}
            title="Compliant"
            value={`${((stats.compliantProducts / stats.totalScans) * 100).toFixed(0)}%`}
            subtitle="Meet standards"
          />
        </Grid>
      </Grid>

      <Paper elevation={3} sx={{ mt: 4, p: 3 }}>
        <Typography variant="h6" gutterBottom>
          Recent Scans
        </Typography>
        <Typography variant="body2" color="text.secondary">
          Your recent scanned products will appear here...
        </Typography>
      </Paper>
    </Box>
  );
}

export default DashboardPage;
