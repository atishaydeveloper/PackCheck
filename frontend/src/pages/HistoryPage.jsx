import React from 'react';
import { Box, Grid, Card, CardContent, Typography, Chip, Button } from '@mui/material';
import { useAuth } from '../contexts/AuthContext';
import { useNavigate } from 'react-router-dom';

function HistoryPage() {
  const { user } = useAuth();
  const navigate = useNavigate();

  if (!user?.history || user.history.length === 0) {
    return (
      <Box sx={{ textAlign: 'center', py: 8 }}>
        <Typography variant="h5" gutterBottom>No scan history yet</Typography>
        <Button variant="contained" onClick={() => navigate('/scan')}>
          Scan Your First Product
        </Button>
      </Box>
    );
  }

  return (
    <Box>
      <Typography variant="h4" fontWeight="bold" gutterBottom>
        Scan History
      </Typography>
      <Typography variant="body1" color="text.secondary" paragraph>
        View all your previously scanned products
      </Typography>

      <Grid container spacing={3}>
        {user.history.map((item) => (
          <Grid item xs={12} md={6} key={item.id}>
            <Card>
              <CardContent>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 2 }}>
                  <Typography variant="h6">Product Scan</Typography>
                  <Chip
                    label={item.compliance?.fssai_verification?.overall_compliance ? 'Compliant' : 'Check'}
                    color={item.compliance?.fssai_verification?.overall_compliance ? 'success' : 'warning'}
                    size="small"
                  />
                </Box>
                <Typography variant="body2" color="text.secondary" gutterBottom>
                  {new Date(item.timestamp).toLocaleString()}
                </Typography>
                {item.extraction?.nutrition_data && (
                  <Box sx={{ mt: 2, display: 'flex', gap: 1, flexWrap: 'wrap' }}>
                    {Object.entries(item.extraction.nutrition_data).map(([key, value]) => (
                      <Chip key={key} label={`${key}: ${value}${key === 'sodium' ? 'mg' : 'g'}`} size="small" />
                    ))}
                  </Box>
                )}
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>
    </Box>
  );
}

export default HistoryPage;
