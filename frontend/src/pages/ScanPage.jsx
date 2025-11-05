import React, { useState, useRef } from 'react';
import {
  Box,
  Paper,
  Typography,
  Button,
  Grid,
  Card,
  CardContent,
  Chip,
  Alert,
  CircularProgress,
  LinearProgress,
  Divider,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  Snackbar
} from '@mui/material';
import {
  CameraAlt,
  Upload,
  CheckCircle,
  Warning,
  Error as ErrorIcon,
  ExpandMore,
  AutoAwesome,
  Scale,
  LocalShipping,
  Restaurant,
  Add,
  Save,
  SwapHoriz
} from '@mui/icons-material';
import axios from 'axios';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { useAuth } from '../contexts/AuthContext';
import { useGamification } from '../contexts/GamificationContext';
import AlternativesDialog from '../components/AlternativesDialog';
import { API_URL } from '../config';

function ScanPage() {
  const { addToHistory, updateDailyIntake } = useAuth();
  const { onScan } = useGamification();
  const [selectedImage, setSelectedImage] = useState(null);
  const [imagePreview, setImagePreview] = useState(null);
  const [scanning, setScanning] = useState(false);
  const [scanResult, setScanResult] = useState(null);
  const [error, setError] = useState(null);
  const [snackbar, setSnackbar] = useState({ open: false, message: '' });
  const [alternativesOpen, setAlternativesOpen] = useState(false);
  const fileInputRef = useRef(null);

  const handleImageSelect = (event) => {
    const file = event.target.files[0];
    if (file) {
      setSelectedImage(file);
      const reader = new FileReader();
      reader.onloadend = () => {
        setImagePreview(reader.result);
      };
      reader.readAsDataURL(file);
      setScanResult(null);
      setError(null);
    }
  };

  const handleScan = async () => {
    if (!selectedImage) {
      setError('Please select an image first');
      return;
    }

    setScanning(true);
    setError(null);

    const formData = new FormData();
    formData.append('image', selectedImage);

    console.log('📤 Sending scan request to:', `${API_URL}/api/scan/`);
    console.log('📤 FormData has image:', formData.has('image'));
    console.log('📤 Selected file:', selectedImage.name, selectedImage.type, selectedImage.size, 'bytes');

    try {
      const response = await axios.post(`${API_URL}/api/scan/`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
        timeout: 180000, // 180 second timeout (3 minutes for OCR + AI processing on free tier)
      });

      console.log('✅ Scan result:', response.data);
      setScanResult(response.data);
      // Automatically save to history
      addToHistory(response.data);
      // Trigger gamification
      onScan(response.data);
    } catch (err) {
      console.error('❌ Scan error:', err);
      console.error('❌ Error response:', err.response?.data);
      console.error('❌ Error status:', err.response?.status);
      setError(err.response?.data?.error || err.response?.data?.message || err.message || 'Error scanning image. Please try again.');
    } finally {
      setScanning(false);
    }
  };

  const handleAddToTracker = () => {
    if (scanResult?.extraction?.nutrition_data) {
      updateDailyIntake(null, scanResult.extraction.nutrition_data);
      setSnackbar({ open: true, message: 'Added to daily tracker!' });
    }
  };

  const getConfidenceColor = (confidence) => {
    if (confidence >= 0.8) return 'success';
    if (confidence >= 0.5) return 'warning';
    return 'error';
  };

  const getRecommendationIcon = (level) => {
    switch (level) {
      case 'high':
        return <CheckCircle color="success" />;
      case 'medium':
        return <Warning color="warning" />;
      case 'low':
        return <ErrorIcon color="error" />;
      default:
        return null;
    }
  };

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Scan Food Label
      </Typography>
      <Typography variant="body1" color="text.secondary" paragraph>
        Upload a food label image • Tesseract extracts data • FSSAI verifies compliance • AI generates insights
      </Typography>

      <Grid container spacing={3}>
        <Grid item xs={12} md={6}>
          <Paper elevation={3} sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Upload Image
            </Typography>

            <Box
              sx={{
                border: '2px dashed #ccc',
                borderRadius: 2,
                p: 3,
                textAlign: 'center',
                cursor: 'pointer',
                '&:hover': {
                  backgroundColor: '#f5f5f5',
                },
              }}
              onClick={() => fileInputRef.current?.click()}
            >
              {imagePreview ? (
                <img
                  src={imagePreview}
                  alt="Preview"
                  style={{ maxWidth: '100%', maxHeight: '300px' }}
                />
              ) : (
                <Box>
                  <Upload sx={{ fontSize: 60, color: '#ccc', mb: 2 }} />
                  <Typography variant="body1">
                    Click to upload or drag and drop
                  </Typography>
                  <Typography variant="caption" color="text.secondary">
                    PNG, JPG, JPEG up to 16MB
                  </Typography>
                </Box>
              )}
            </Box>

            <input
              type="file"
              ref={fileInputRef}
              onChange={handleImageSelect}
              accept="image/*"
              style={{ display: 'none' }}
            />

            <Box sx={{ mt: 2, display: 'flex', gap: 2 }}>
              <Button
                variant="contained"
                fullWidth
                onClick={handleScan}
                disabled={!selectedImage || scanning}
                startIcon={scanning ? <CircularProgress size={20} /> : <CameraAlt />}
              >
                {scanning ? 'Scanning...' : 'Scan Label'}
              </Button>
            </Box>

            {scanning && (
              <Box sx={{ mt: 2 }}>
                <Typography variant="caption" color="text.secondary">
                  Processing your image with Tesseract OCR + AI analysis...
                </Typography>
                <Typography variant="caption" display="block" color="text.secondary" sx={{ mt: 0.5 }}>
                  This may take 1-2 minutes on free tier. Please be patient! ⏳
                </Typography>
                <LinearProgress sx={{ mt: 1 }} />
              </Box>
            )}

            {error && (
              <Alert severity="error" sx={{ mt: 2 }}>
                {error}
              </Alert>
            )}
          </Paper>
        </Grid>

        <Grid item xs={12} md={6}>
          {scanResult && (
            <Paper elevation={3} sx={{ p: 3 }}>
              <Typography variant="h6" gutterBottom>
                Scan Results
              </Typography>

              {/* Extraction Source */}
              <Chip
                label={`Extracted by: ${scanResult.extraction?.source || 'Unknown'}`}
                size="small"
                color="primary"
                sx={{ mb: 2 }}
              />

              {/* Overall Confidence */}
              {scanResult.extraction?.confidence?.overall !== undefined && (
                <Box sx={{ mb: 3 }}>
                  <Typography variant="body2" gutterBottom>
                    Overall Confidence
                  </Typography>
                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                    <LinearProgress
                      variant="determinate"
                      value={scanResult.extraction.confidence.overall * 100}
                      color={getConfidenceColor(scanResult.extraction.confidence.overall)}
                      sx={{ flexGrow: 1, height: 10, borderRadius: 5 }}
                    />
                    <Typography variant="body2" fontWeight="bold">
                      {(scanResult.extraction.confidence.overall * 100).toFixed(0)}%
                    </Typography>
                  </Box>
                </Box>
              )}

              {/* Recommendation */}
              {scanResult.recommendation && (
                <Alert
                  severity={
                    scanResult.recommendation.level === 'high'
                      ? 'success'
                      : scanResult.recommendation.level === 'medium'
                      ? 'warning'
                      : 'error'
                  }
                  icon={getRecommendationIcon(scanResult.recommendation.level)}
                  sx={{ mb: 3 }}
                >
                  <Typography variant="body2" fontWeight="bold">
                    {scanResult.recommendation.message}
                  </Typography>
                  <Typography variant="caption">
                    {scanResult.recommendation.action}
                  </Typography>
                </Alert>
              )}

              {/* Action Buttons */}
              <Grid container spacing={2} sx={{ mb: 2 }}>
                <Grid item xs={12} sm={6}>
                  <Button
                    variant="contained"
                    startIcon={<Add />}
                    onClick={handleAddToTracker}
                    fullWidth
                  >
                    Add to Tracker
                  </Button>
                </Grid>
                <Grid item xs={12} sm={6}>
                  <Button
                    variant="outlined"
                    startIcon={<Save />}
                    fullWidth
                    disabled
                  >
                    Saved to History
                  </Button>
                </Grid>
                <Grid item xs={12}>
                  <Button
                    variant="contained"
                    startIcon={<SwapHoriz />}
                    onClick={() => setAlternativesOpen(true)}
                    fullWidth
                    sx={{
                      background: 'linear-gradient(135deg, #10b981 0%, #059669 100%)',
                      '&:hover': {
                        background: 'linear-gradient(135deg, #059669 0%, #047857 100%)',
                      },
                    }}
                  >
                    Get Better Alternatives
                  </Button>
                </Grid>
              </Grid>

              <Divider sx={{ my: 2 }} />

              {/* Product Information */}
              {(scanResult.extraction?.serving_size || scanResult.extraction?.net_weight || scanResult.extraction?.servings_per_container) && (
                <>
                  <Typography variant="subtitle1" fontWeight="bold" gutterBottom>
                    Product Information
                  </Typography>
                  <Grid container spacing={1} sx={{ mb: 3 }}>
                    {scanResult.extraction.serving_size && (
                      <Grid item xs={12} sm={4}>
                        <Card variant="outlined" sx={{ bgcolor: '#f5f5f5' }}>
                          <CardContent sx={{ p: 1.5, '&:last-child': { pb: 1.5 } }}>
                            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                              <Restaurant fontSize="small" color="primary" />
                              <Box>
                                <Typography variant="caption" color="text.secondary">
                                  Serving Size
                                </Typography>
                                <Typography variant="body2" fontWeight="bold">
                                  {scanResult.extraction.serving_size}
                                </Typography>
                              </Box>
                            </Box>
                          </CardContent>
                        </Card>
                      </Grid>
                    )}
                    {scanResult.extraction.net_weight && (
                      <Grid item xs={12} sm={4}>
                        <Card variant="outlined" sx={{ bgcolor: '#f5f5f5' }}>
                          <CardContent sx={{ p: 1.5, '&:last-child': { pb: 1.5 } }}>
                            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                              <LocalShipping fontSize="small" color="primary" />
                              <Box>
                                <Typography variant="caption" color="text.secondary">
                                  Net Weight
                                </Typography>
                                <Typography variant="body2" fontWeight="bold">
                                  {scanResult.extraction.net_weight}
                                </Typography>
                              </Box>
                            </Box>
                          </CardContent>
                        </Card>
                      </Grid>
                    )}
                    {scanResult.extraction.servings_per_container && (
                      <Grid item xs={12} sm={4}>
                        <Card variant="outlined" sx={{ bgcolor: '#f5f5f5' }}>
                          <CardContent sx={{ p: 1.5, '&:last-child': { pb: 1.5 } }}>
                            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                              <Scale fontSize="small" color="primary" />
                              <Box>
                                <Typography variant="caption" color="text.secondary">
                                  Servings
                                </Typography>
                                <Typography variant="body2" fontWeight="bold">
                                  {scanResult.extraction.servings_per_container}
                                </Typography>
                              </Box>
                            </Box>
                          </CardContent>
                        </Card>
                      </Grid>
                    )}
                  </Grid>
                </>
              )}

              {/* Nutrition Facts */}
              <Typography variant="subtitle1" fontWeight="bold" gutterBottom>
                Nutrition Facts (per serving)
              </Typography>
              {scanResult.extraction?.nutrition_data && Object.keys(scanResult.extraction.nutrition_data).length > 0 ? (
                <Grid container spacing={1}>
                  {Object.entries(scanResult.extraction.nutrition_data).map(([key, value]) => (
                    <Grid item xs={6} key={key}>
                      <Chip
                        label={`${key.charAt(0).toUpperCase() + key.slice(1)}: ${value}${key === 'sodium' ? 'mg' : 'g'}`}
                        size="small"
                        sx={{ width: '100%' }}
                      />
                    </Grid>
                  ))}
                </Grid>
              ) : (
                <Typography variant="body2" color="text.secondary">
                  No nutrition data extracted
                </Typography>
              )}

              <Divider sx={{ my: 2 }} />

              {/* FSSAI Verification */}
              <Typography variant="subtitle1" fontWeight="bold" gutterBottom>
                FSSAI Compliance
              </Typography>
              {scanResult.compliance?.fssai_verification && (
                <>
                  <Box sx={{ mb: 2 }}>
                    <Chip
                      label={
                        scanResult.compliance.fssai_verification.overall_compliance
                          ? 'Compliant'
                          : 'Non-Compliant'
                      }
                      color={
                        scanResult.compliance.fssai_verification.overall_compliance
                          ? 'success'
                          : 'error'
                      }
                      size="small"
                    />
                    <Chip
                      label={`Trust Score: ${(scanResult.compliance.fssai_verification.trust_score * 100).toFixed(0)}%`}
                      size="small"
                      sx={{ ml: 1 }}
                    />
                  </Box>

                  {/* Verification Details */}
                  {scanResult.compliance.fssai_verification.verifications &&
                    Object.entries(scanResult.compliance.fssai_verification.verifications).map(
                      ([nutrient, verification]) => (
                        <Box key={nutrient} sx={{ mb: 1 }}>
                          <Typography variant="caption" color="text.secondary">
                            {nutrient.toUpperCase()}
                          </Typography>
                          <Typography variant="body2">{verification.message}</Typography>
                        </Box>
                      )
                    )
                  }

                  {/* Recommendations */}
                  {scanResult.compliance.fssai_verification.recommendations?.length > 0 && (
                    <Box sx={{ mt: 2 }}>
                      <Typography variant="subtitle2" gutterBottom>
                        Recommendations
                      </Typography>
                      {scanResult.compliance.fssai_verification.recommendations.map((rec, idx) => (
                        <Typography key={idx} variant="body2" sx={{ mb: 0.5 }}>
                          • {rec}
                        </Typography>
                      ))}
                    </Box>
                  )}
                </>
              )}

              {/* Allergen Info */}
              {scanResult.compliance?.allergen_info?.allergens_detected?.length > 0 && (
                <>
                  <Divider sx={{ my: 2 }} />
                  <Typography variant="subtitle1" fontWeight="bold" gutterBottom>
                    Allergen Warning
                  </Typography>
                  <Alert severity="warning">
                    Contains: {scanResult.compliance.allergen_info.allergens_detected.join(', ')}
                  </Alert>
                </>
              )}

              {/* AI Insights */}
              {scanResult.ai_insights && scanResult.ai_insights.available !== false && (
                <>
                  <Divider sx={{ my: 2 }} />
                  <Typography variant="subtitle1" fontWeight="bold" gutterBottom>
                    <AutoAwesome sx={{ fontSize: 20, mr: 1, verticalAlign: 'middle' }} />
                    AI Insights
                  </Typography>

                  {scanResult.ai_insights.comprehensive_report && (
                    <Accordion defaultExpanded>
                      <AccordionSummary
                        expandIcon={<ExpandMore />}
                        sx={{
                          bgcolor: '#f8f9fa',
                          '&:hover': { bgcolor: '#e9ecef' }
                        }}
                      >
                        <Typography variant="subtitle2" fontWeight="bold">
                          📊 Comprehensive Nutrition Report
                        </Typography>
                      </AccordionSummary>
                      <AccordionDetails sx={{ maxHeight: '600px', overflow: 'auto' }}>
                        <Box
                          sx={{
                            '& h2': {
                              fontSize: '1.25rem',
                              fontWeight: 'bold',
                              mt: 3,
                              mb: 2,
                              color: '#1976d2'
                            },
                            '& h3': {
                              fontSize: '1.1rem',
                              fontWeight: 'bold',
                              mt: 2,
                              mb: 1,
                              color: '#424242'
                            },
                            '& h4': {
                              fontSize: '1rem',
                              fontWeight: 'bold',
                              mt: 1.5,
                              mb: 1,
                              color: '#616161'
                            },
                            '& p': {
                              fontSize: '0.875rem',
                              lineHeight: 1.6,
                              mb: 1,
                              color: '#212121'
                            },
                            '& ul, & ol': {
                              fontSize: '0.875rem',
                              pl: 2,
                              mb: 2
                            },
                            '& li': {
                              mb: 0.5
                            },
                            '& table': {
                              width: '100%',
                              borderCollapse: 'collapse',
                              mb: 2,
                              fontSize: '0.875rem'
                            },
                            '& th': {
                              bgcolor: '#f5f5f5',
                              p: 1,
                              border: '1px solid #ddd',
                              fontWeight: 'bold',
                              textAlign: 'left'
                            },
                            '& td': {
                              p: 1,
                              border: '1px solid #ddd'
                            },
                            '& strong': {
                              fontWeight: 600,
                              color: '#1976d2'
                            },
                            '& blockquote': {
                              borderLeft: '4px solid #1976d2',
                              pl: 2,
                              ml: 0,
                              fontStyle: 'italic',
                              color: '#616161'
                            },
                            '& code': {
                              bgcolor: '#f5f5f5',
                              p: 0.5,
                              borderRadius: 1,
                              fontSize: '0.8rem',
                              fontFamily: 'monospace'
                            },
                            '& hr': {
                              my: 2,
                              border: 'none',
                              borderTop: '1px solid #ddd'
                            }
                          }}
                        >
                          <ReactMarkdown remarkPlugins={[remarkGfm]}>
                            {scanResult.ai_insights.comprehensive_report}
                          </ReactMarkdown>
                        </Box>
                      </AccordionDetails>
                    </Accordion>
                  )}

                  {scanResult.ai_insights.ingredient_analysis && (
                    <Accordion sx={{ mt: 1 }}>
                      <AccordionSummary
                        expandIcon={<ExpandMore />}
                        sx={{
                          bgcolor: '#f8f9fa',
                          '&:hover': { bgcolor: '#e9ecef' }
                        }}
                      >
                        <Typography variant="subtitle2" fontWeight="bold">
                          🔬 Ingredient Safety Analysis
                        </Typography>
                      </AccordionSummary>
                      <AccordionDetails sx={{ maxHeight: '400px', overflow: 'auto' }}>
                        <Box
                          sx={{
                            '& h2, & h3, & h4': {
                              fontWeight: 'bold',
                              mt: 2,
                              mb: 1
                            },
                            '& p': {
                              fontSize: '0.875rem',
                              lineHeight: 1.6,
                              mb: 1
                            },
                            '& ul, & ol': {
                              fontSize: '0.875rem',
                              pl: 2
                            },
                            '& strong': {
                              fontWeight: 600,
                              color: '#d32f2f'
                            }
                          }}
                        >
                          <ReactMarkdown remarkPlugins={[remarkGfm]}>
                            {scanResult.ai_insights.ingredient_analysis}
                          </ReactMarkdown>
                        </Box>
                      </AccordionDetails>
                    </Accordion>
                  )}
                </>
              )}

              {scanResult.ai_insights?.available === false && (
                <>
                  <Divider sx={{ my: 2 }} />
                  <Alert severity="info" icon={<AutoAwesome />}>
                    <Typography variant="body2">
                      {scanResult.ai_insights.message}
                    </Typography>
                    <Typography variant="caption">
                      Add GEMINI_API_KEY to enable AI-powered insights and recommendations
                    </Typography>
                  </Alert>
                </>
              )}
            </Paper>
          )}
        </Grid>
      </Grid>

      <Snackbar
        open={snackbar.open}
        autoHideDuration={3000}
        onClose={() => setSnackbar({ ...snackbar, open: false })}
        message={snackbar.message}
      />

      {/* Alternatives Dialog */}
      {scanResult && (
        <AlternativesDialog
          open={alternativesOpen}
          onClose={() => setAlternativesOpen(false)}
          scanResult={scanResult}
        />
      )}
    </Box>
  );
}

export default ScanPage;
