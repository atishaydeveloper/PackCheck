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
  Divider
} from '@mui/material';
import {
  CameraAlt,
  Upload,
  CheckCircle,
  Warning,
  Error as ErrorIcon
} from '@mui/icons-material';
import axios from 'axios';

function ScanPage() {
  const [selectedImage, setSelectedImage] = useState(null);
  const [imagePreview, setImagePreview] = useState(null);
  const [scanning, setScanning] = useState(false);
  const [scanResult, setScanResult] = useState(null);
  const [error, setError] = useState(null);
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

    try {
      const response = await axios.post('/api/scan/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      setScanResult(response.data);
    } catch (err) {
      setError(err.response?.data?.message || 'Error scanning image. Please try again.');
    } finally {
      setScanning(false);
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
        Upload or capture a food label image to extract nutrition information and verify FSSAI compliance
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

              {/* Overall Confidence */}
              <Box sx={{ mb: 3 }}>
                <Typography variant="body2" gutterBottom>
                  Overall Confidence
                </Typography>
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                  <LinearProgress
                    variant="determinate"
                    value={scanResult.overall_confidence * 100}
                    color={getConfidenceColor(scanResult.overall_confidence)}
                    sx={{ flexGrow: 1, height: 10, borderRadius: 5 }}
                  />
                  <Typography variant="body2" fontWeight="bold">
                    {(scanResult.overall_confidence * 100).toFixed(0)}%
                  </Typography>
                </Box>
              </Box>

              {/* Recommendation */}
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

              <Divider sx={{ my: 2 }} />

              {/* Nutrition Facts */}
              <Typography variant="subtitle1" fontWeight="bold" gutterBottom>
                Nutrition Facts
              </Typography>
              <Grid container spacing={1}>
                {Object.entries(scanResult.ocr_results.nutrition_facts).map(([key, value]) => (
                  <Grid item xs={6} key={key}>
                    <Chip
                      label={`${key.charAt(0).toUpperCase() + key.slice(1)}: ${value}g`}
                      size="small"
                      sx={{ width: '100%' }}
                    />
                  </Grid>
                ))}
              </Grid>

              <Divider sx={{ my: 2 }} />

              {/* FSSAI Verification */}
              <Typography variant="subtitle1" fontWeight="bold" gutterBottom>
                FSSAI Verification
              </Typography>
              <Box sx={{ mb: 2 }}>
                <Chip
                  label={
                    scanResult.fssai_verification.overall_compliance
                      ? 'Compliant'
                      : 'Non-Compliant'
                  }
                  color={
                    scanResult.fssai_verification.overall_compliance
                      ? 'success'
                      : 'error'
                  }
                  size="small"
                />
                <Chip
                  label={`Trust Score: ${(scanResult.fssai_verification.trust_score * 100).toFixed(0)}%`}
                  size="small"
                  sx={{ ml: 1 }}
                />
              </Box>

              {/* Verification Details */}
              {Object.entries(scanResult.fssai_verification.verifications).map(
                ([nutrient, verification]) => (
                  <Box key={nutrient} sx={{ mb: 1 }}>
                    <Typography variant="caption" color="text.secondary">
                      {nutrient.toUpperCase()}
                    </Typography>
                    <Typography variant="body2">{verification.message}</Typography>
                  </Box>
                )
              )}

              {/* Allergen Info */}
              {scanResult.allergen_info?.allergens_detected?.length > 0 && (
                <>
                  <Divider sx={{ my: 2 }} />
                  <Typography variant="subtitle1" fontWeight="bold" gutterBottom>
                    Allergen Warning
                  </Typography>
                  <Alert severity="warning">
                    Contains: {scanResult.allergen_info.allergens_detected.join(', ')}
                  </Alert>
                </>
              )}

              {/* Recommendations */}
              {scanResult.fssai_verification.recommendations?.length > 0 && (
                <>
                  <Divider sx={{ my: 2 }} />
                  <Typography variant="subtitle1" fontWeight="bold" gutterBottom>
                    Recommendations
                  </Typography>
                  {scanResult.fssai_verification.recommendations.map((rec, idx) => (
                    <Typography key={idx} variant="body2" sx={{ mb: 0.5 }}>
                      • {rec}
                    </Typography>
                  ))}
                </>
              )}
            </Paper>
          )}
        </Grid>
      </Grid>
    </Box>
  );
}

export default ScanPage;
