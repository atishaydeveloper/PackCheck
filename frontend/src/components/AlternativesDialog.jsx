import React, { useState } from 'react';
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  Box,
  Typography,
  CircularProgress,
  Alert,
  IconButton,
  Chip,
  Divider,
} from '@mui/material';
import CloseIcon from '@mui/icons-material/Close';
import SwapHorizIcon from '@mui/icons-material/SwapHoriz';
import TrendingUpIcon from '@mui/icons-material/TrendingUp';
import LocalGroceryStoreIcon from '@mui/icons-material/LocalGroceryStore';
import { motion, AnimatePresence } from 'framer-motion';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import axios from 'axios';
import { useAuth } from '../contexts/AuthContext';
import { API_URL } from '../config';

const AlternativesDialog = ({ open, onClose, scanResult }) => {
  const { user } = useAuth();
  const [loading, setLoading] = useState(false);
  const [alternatives, setAlternatives] = useState(null);
  const [error, setError] = useState(null);

  const fetchAlternatives = async () => {
    setLoading(true);
    setError(null);

    try {
      const response = await axios.post(`${API_URL}/api/scan/alternatives`, {
        nutrition_data: {
          ...scanResult.extraction.nutrition_data,
          product_name: scanResult.extraction.nutrition_data.product_name || 'Unknown Product',
          brand: scanResult.extraction.nutrition_data.brand || 'Unknown Brand',
          serving_size: scanResult.extraction.serving_size,
          net_weight: scanResult.extraction.net_weight,
          servings_per_container: scanResult.extraction.servings_per_container,
          ingredients: scanResult.extraction.ingredients,
          nutrition_facts: scanResult.extraction.nutrition_data,
        },
        fssai_verification: scanResult.compliance.fssai_verification,
        user_profile: user ? {
          fitness_goal: user.fitnessGoal,
          dietary_preference: user.dietaryPreference,
          age: user.age,
        } : null,
      });

      if (response.data.success) {
        setAlternatives(response.data.alternatives);
      } else {
        setError(response.data.error || 'Failed to fetch alternatives');
      }
    } catch (err) {
      setError(err.response?.data?.error || err.message || 'Failed to fetch alternatives');
    } finally {
      setLoading(false);
    }
  };

  React.useEffect(() => {
    if (open && !alternatives && !loading) {
      fetchAlternatives();
    }
  }, [open]);

  return (
    <Dialog
      open={open}
      onClose={onClose}
      maxWidth="md"
      fullWidth
      PaperProps={{
        sx: {
          borderRadius: 3,
          background: 'linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%)',
          maxHeight: '90vh',
        },
      }}
    >
      <DialogTitle
        sx={{
          background: 'linear-gradient(135deg, #10b981 0%, #059669 100%)',
          color: '#fff',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
        }}
      >
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
          <SwapHorizIcon />
          <Typography variant="h6" fontWeight="bold">
            Healthier Alternatives
          </Typography>
        </Box>
        <IconButton onClick={onClose} sx={{ color: '#fff' }}>
          <CloseIcon />
        </IconButton>
      </DialogTitle>

      <DialogContent sx={{ mt: 2 }}>
        <AnimatePresence mode="wait">
          {loading && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
            >
              <Box
                sx={{
                  display: 'flex',
                  flexDirection: 'column',
                  alignItems: 'center',
                  justifyContent: 'center',
                  py: 8,
                  gap: 2,
                }}
              >
                <CircularProgress size={60} sx={{ color: '#10b981' }} />
                <Typography variant="h6" color="text.secondary">
                  Finding better options for you...
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Analyzing nutrition data and searching for healthier alternatives
                </Typography>
              </Box>
            </motion.div>
          )}

          {error && !loading && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0 }}
            >
              <Alert severity="error" sx={{ mb: 2 }}>
                {error}
              </Alert>
              <Button
                variant="contained"
                onClick={fetchAlternatives}
                fullWidth
                sx={{
                  background: 'linear-gradient(135deg, #10b981 0%, #059669 100%)',
                }}
              >
                Try Again
              </Button>
            </motion.div>
          )}

          {alternatives && !loading && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0 }}
            >
              <Box
                sx={{
                  '& h1': {
                    fontSize: '1.5rem',
                    fontWeight: 'bold',
                    mt: 3,
                    mb: 2,
                    color: '#1f2937',
                  },
                  '& h2': {
                    fontSize: '1.25rem',
                    fontWeight: 'bold',
                    mt: 2.5,
                    mb: 1.5,
                    color: '#374151',
                    borderLeft: '4px solid #10b981',
                    pl: 2,
                  },
                  '& h3': {
                    fontSize: '1.1rem',
                    fontWeight: '600',
                    mt: 2,
                    mb: 1,
                    color: '#4b5563',
                  },
                  '& p': {
                    fontSize: '0.95rem',
                    lineHeight: 1.7,
                    mb: 1.5,
                    color: '#6b7280',
                  },
                  '& ul, & ol': {
                    pl: 3,
                    mb: 2,
                  },
                  '& li': {
                    mb: 0.5,
                    color: '#6b7280',
                    fontSize: '0.95rem',
                  },
                  '& table': {
                    width: '100%',
                    borderCollapse: 'collapse',
                    my: 2,
                    fontSize: '0.9rem',
                  },
                  '& th': {
                    background: 'linear-gradient(135deg, #10b981 0%, #059669 100%)',
                    color: '#fff',
                    padding: '12px',
                    textAlign: 'left',
                    fontWeight: 'bold',
                  },
                  '& td': {
                    padding: '10px 12px',
                    borderBottom: '1px solid #e5e7eb',
                  },
                  '& tr:nth-of-type(even)': {
                    background: '#f9fafb',
                  },
                  '& strong': {
                    color: '#1f2937',
                    fontWeight: '600',
                  },
                  '& hr': {
                    my: 3,
                    border: 'none',
                    borderTop: '2px solid #e5e7eb',
                  },
                  '& blockquote': {
                    borderLeft: '4px solid #10b981',
                    pl: 2,
                    py: 1,
                    my: 2,
                    background: '#f0fdf4',
                    fontStyle: 'italic',
                  },
                  '& code': {
                    background: '#f3f4f6',
                    padding: '2px 6px',
                    borderRadius: '4px',
                    fontSize: '0.9em',
                    color: '#10b981',
                  },
                }}
              >
                <ReactMarkdown remarkPlugins={[remarkGfm]}>
                  {alternatives}
                </ReactMarkdown>
              </Box>
            </motion.div>
          )}
        </AnimatePresence>
      </DialogContent>

      <DialogActions sx={{ px: 3, pb: 2 }}>
        <Button
          onClick={onClose}
          variant="contained"
          fullWidth
          sx={{
            background: 'linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%)',
            '&:hover': {
              background: 'linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%)',
            },
          }}
        >
          Close
        </Button>
      </DialogActions>
    </Dialog>
  );
};

export default AlternativesDialog;
