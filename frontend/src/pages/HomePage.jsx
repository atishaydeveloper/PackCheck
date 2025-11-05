import React from 'react';
import {
  Box,
  Container,
  Typography,
  Button,
  Grid,
  Card,
  CardContent,
  Avatar,
  Chip,
  alpha,
} from '@mui/material';
import {
  CameraAlt,
  VerifiedUser,
  AutoAwesome,
  TrendingUp,
  EmojiEvents,
  Restaurant,
  Spa,
  FitnessCenter,
  ArrowForward,
  CheckCircle,
} from '@mui/icons-material';
import { motion } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

const HomePage = () => {
  const navigate = useNavigate();
  const { user } = useAuth();

  const features = [
    {
      icon: <CameraAlt sx={{ fontSize: 48 }} />,
      title: 'Smart OCR Scanning',
      description: 'Advanced Tesseract OCR extracts every detail from food labels with multi-pass technology',
      gradient: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    },
    {
      icon: <VerifiedUser sx={{ fontSize: 48 }} />,
      title: 'FSSAI Compliance',
      description: 'Real-time verification against actual FSSAI and WHO regulations and standards',
      gradient: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
    },
    {
      icon: <AutoAwesome sx={{ fontSize: 48 }} />,
      title: 'AI Insights',
      description: 'Gemini AI generates comprehensive reports, alternatives, and personalized recommendations',
      gradient: 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)',
    },
    {
      icon: <EmojiEvents sx={{ fontSize: 48 }} />,
      title: 'Gamification',
      description: 'Earn points, unlock achievements, level up, and maintain streaks for healthy habits',
      gradient: 'linear-gradient(135deg, #fa709a 0%, #fee140 100%)',
    },
    {
      icon: <TrendingUp sx={{ fontSize: 48 }} />,
      title: 'Progress Tracking',
      description: 'Track daily nutrition, view trends, and monitor your fitness goals with interactive charts',
      gradient: 'linear-gradient(135deg, #30cfd0 0%, #330867 100%)',
    },
    {
      icon: <Restaurant sx={{ fontSize: 48 }} />,
      title: 'Food Database',
      description: 'Access comprehensive nutrition data, scan history, and build your personal food library',
      gradient: 'linear-gradient(135deg, #a8edea 0%, #fed6e3 100%)',
    },
  ];

  const benefits = [
    { icon: <CheckCircle />, text: 'Make informed food choices' },
    { icon: <CheckCircle />, text: 'Verify product claims instantly' },
    { icon: <CheckCircle />, text: 'Track nutrition goals effortlessly' },
    { icon: <CheckCircle />, text: 'Discover healthier alternatives' },
    { icon: <CheckCircle />, text: 'Build healthy eating habits' },
    { icon: <CheckCircle />, text: 'Achieve fitness goals faster' },
  ];

  const stats = [
    { icon: <CameraAlt />, value: '10,000+', label: 'Products Scanned' },
    { icon: <VerifiedUser />, value: '98%', label: 'Accuracy Rate' },
    { icon: <EmojiEvents />, value: '5,000+', label: 'Achievements Unlocked' },
    { icon: <TrendingUp />, value: '15k+', label: 'Daily Trackers' },
  ];

  return (
    <Box>
      {/* Hero Section */}
      <Box
        sx={{
          background: 'linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%)',
          color: '#fff',
          py: { xs: 8, md: 12 },
          position: 'relative',
          overflow: 'hidden',
        }}
      >
        {/* Animated Background Pattern */}
        <Box
          sx={{
            position: 'absolute',
            top: 0,
            left: 0,
            right: 0,
            bottom: 0,
            opacity: 0.1,
            backgroundImage: `radial-gradient(circle, #fff 1px, transparent 1px)`,
            backgroundSize: '50px 50px',
          }}
        />

        <Container maxWidth="lg" sx={{ position: 'relative', zIndex: 1 }}>
          <Grid container spacing={6} alignItems="center">
            <Grid item xs={12} md={6}>
              <motion.div
                initial={{ opacity: 0, x: -50 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.8 }}
              >
                <Chip
                  label="AI-Powered Nutrition Intelligence"
                  sx={{
                    mb: 3,
                    bgcolor: alpha('#fff', 0.2),
                    color: '#fff',
                    fontWeight: 'bold',
                    backdropFilter: 'blur(10px)',
                  }}
                />
                <Typography
                  variant="h2"
                  fontWeight="bold"
                  gutterBottom
                  sx={{
                    fontSize: { xs: '2.5rem', md: '3.5rem' },
                    lineHeight: 1.2,
                  }}
                >
                  Know What You Eat.
                  <br />
                  Eat What's Right.
                </Typography>
                <Typography
                  variant="h6"
                  sx={{
                    mb: 4,
                    opacity: 0.95,
                    fontSize: { xs: '1.1rem', md: '1.25rem' },
                    lineHeight: 1.6,
                  }}
                >
                  Scan food labels, verify compliance, get AI insights, and track your nutrition journey
                  with gamified goals. Your personal nutrition coach powered by AI.
                </Typography>

                <Box sx={{ display: 'flex', gap: 2, flexWrap: 'wrap' }}>
                  <Button
                    variant="contained"
                    size="large"
                    endIcon={<ArrowForward />}
                    onClick={() => navigate(user ? '/scan' : '/signup')}
                    sx={{
                      bgcolor: '#fff',
                      color: '#667eea',
                      px: 4,
                      py: 1.5,
                      fontSize: '1.1rem',
                      fontWeight: 'bold',
                      '&:hover': {
                        bgcolor: '#f0f0f0',
                        transform: 'translateY(-2px)',
                        boxShadow: '0 8px 20px rgba(0,0,0,0.2)',
                      },
                      transition: 'all 0.3s',
                    }}
                  >
                    {user ? 'Start Scanning' : 'Get Started Free'}
                  </Button>
                  <Button
                    variant="outlined"
                    size="large"
                    onClick={() => navigate('/dashboard')}
                    sx={{
                      borderColor: '#fff',
                      color: '#fff',
                      px: 4,
                      py: 1.5,
                      fontSize: '1.1rem',
                      fontWeight: 'bold',
                      '&:hover': {
                        borderColor: '#fff',
                        bgcolor: alpha('#fff', 0.1),
                      },
                    }}
                  >
                    View Dashboard
                  </Button>
                </Box>
              </motion.div>
            </Grid>

            <Grid item xs={12} md={6}>
              <motion.div
                initial={{ opacity: 0, x: 50 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.8, delay: 0.2 }}
              >
                <Box
                  sx={{
                    position: 'relative',
                    display: 'flex',
                    justifyContent: 'center',
                    alignItems: 'center',
                  }}
                >
                  {/* Decorative Elements */}
                  <Box
                    sx={{
                      position: 'absolute',
                      width: '100%',
                      height: '100%',
                      borderRadius: '50%',
                      background: alpha('#fff', 0.1),
                      filter: 'blur(50px)',
                      animation: 'pulse 3s ease-in-out infinite',
                      '@keyframes pulse': {
                        '0%, 100%': { transform: 'scale(1)' },
                        '50%': { transform: 'scale(1.1)' },
                      },
                    }}
                  />
                  <Box
                    sx={{
                      position: 'relative',
                      bgcolor: alpha('#fff', 0.15),
                      backdropFilter: 'blur(20px)',
                      borderRadius: 4,
                      p: 4,
                      border: `2px solid ${alpha('#fff', 0.3)}`,
                    }}
                  >
                    <Box
                      sx={{
                        fontSize: '180px',
                        textAlign: 'center',
                        animation: 'float 3s ease-in-out infinite',
                        '@keyframes float': {
                          '0%, 100%': { transform: 'translateY(0px)' },
                          '50%': { transform: 'translateY(-20px)' },
                        },
                      }}
                    >
                      🍎
                    </Box>
                    <Typography
                      variant="h6"
                      textAlign="center"
                      fontWeight="bold"
                      sx={{ mt: 2 }}
                    >
                      Scan • Verify • Track
                    </Typography>
                  </Box>
                </Box>
              </motion.div>
            </Grid>
          </Grid>
        </Container>
      </Box>

      {/* Stats Section */}
      <Container maxWidth="lg" sx={{ mt: -6, mb: 8, position: 'relative', zIndex: 2 }}>
        <Grid container spacing={3}>
          {stats.map((stat, index) => (
            <Grid item xs={6} md={3} key={index}>
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, delay: index * 0.1 }}
              >
                <Card
                  sx={{
                    textAlign: 'center',
                    p: 3,
                    background: 'linear-gradient(135deg, #fff 0%, #f8f9fa 100%)',
                    boxShadow: '0 10px 30px rgba(0,0,0,0.1)',
                    border: '1px solid rgba(0,0,0,0.05)',
                    '&:hover': {
                      transform: 'translateY(-8px)',
                      boxShadow: '0 15px 40px rgba(0,0,0,0.15)',
                    },
                    transition: 'all 0.3s',
                  }}
                >
                  <Avatar
                    sx={{
                      width: 60,
                      height: 60,
                      mx: 'auto',
                      mb: 2,
                      background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                    }}
                  >
                    {stat.icon}
                  </Avatar>
                  <Typography variant="h4" fontWeight="bold" color="primary" gutterBottom>
                    {stat.value}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    {stat.label}
                  </Typography>
                </Card>
              </motion.div>
            </Grid>
          ))}
        </Grid>
      </Container>

      {/* Features Section */}
      <Container maxWidth="lg" sx={{ py: 8 }}>
        <Box sx={{ textAlign: 'center', mb: 6 }}>
          <Typography variant="h3" fontWeight="bold" gutterBottom>
            Powerful Features
          </Typography>
          <Typography variant="h6" color="text.secondary" sx={{ maxWidth: 700, mx: 'auto' }}>
            Everything you need to make informed nutrition decisions and achieve your health goals
          </Typography>
        </Box>

        <Grid container spacing={4}>
          {features.map((feature, index) => (
            <Grid item xs={12} md={4} key={index}>
              <motion.div
                initial={{ opacity: 0, y: 30 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, delay: index * 0.1 }}
              >
                <Card
                  sx={{
                    height: '100%',
                    p: 3,
                    borderRadius: 3,
                    background: 'linear-gradient(135deg, #fff 0%, #f8f9fa 100%)',
                    border: '1px solid rgba(0,0,0,0.05)',
                    '&:hover': {
                      transform: 'translateY(-10px)',
                      boxShadow: '0 20px 40px rgba(0,0,0,0.12)',
                    },
                    transition: 'all 0.4s',
                  }}
                >
                  <Box
                    sx={{
                      width: 80,
                      height: 80,
                      borderRadius: 3,
                      background: feature.gradient,
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      color: '#fff',
                      mb: 3,
                    }}
                  >
                    {feature.icon}
                  </Box>
                  <Typography variant="h6" fontWeight="bold" gutterBottom>
                    {feature.title}
                  </Typography>
                  <Typography variant="body2" color="text.secondary" sx={{ lineHeight: 1.7 }}>
                    {feature.description}
                  </Typography>
                </Card>
              </motion.div>
            </Grid>
          ))}
        </Grid>
      </Container>

      {/* Benefits Section */}
      <Box
        sx={{
          background: 'linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%)',
          py: 8,
        }}
      >
        <Container maxWidth="lg">
          <Grid container spacing={6} alignItems="center">
            <Grid item xs={12} md={6}>
              <Typography variant="h3" fontWeight="bold" gutterBottom>
                Why Choose PackCheck?
              </Typography>
              <Typography variant="h6" color="text.secondary" paragraph>
                The complete nutrition solution for health-conscious individuals
              </Typography>
              <Grid container spacing={2} sx={{ mt: 2 }}>
                {benefits.map((benefit, index) => (
                  <Grid item xs={12} key={index}>
                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                      <Avatar
                        sx={{
                          bgcolor: '#10b981',
                          width: 40,
                          height: 40,
                        }}
                      >
                        {benefit.icon}
                      </Avatar>
                      <Typography variant="h6">{benefit.text}</Typography>
                    </Box>
                  </Grid>
                ))}
              </Grid>
            </Grid>
            <Grid item xs={12} md={6}>
              <Box
                sx={{
                  position: 'relative',
                  display: 'flex',
                  justifyContent: 'center',
                  alignItems: 'center',
                  gap: 2,
                }}
              >
                <Box sx={{ textAlign: 'center' }}>
                  <Box
                    sx={{
                      fontSize: '120px',
                      animation: 'bounce 2s ease-in-out infinite',
                      '@keyframes bounce': {
                        '0%, 100%': { transform: 'translateY(0)' },
                        '50%': { transform: 'translateY(-15px)' },
                      },
                    }}
                  >
                    🥗
                  </Box>
                  <Box
                    sx={{
                      fontSize: '120px',
                      animation: 'bounce 2s ease-in-out infinite 0.3s',
                    }}
                  >
                    🥑
                  </Box>
                </Box>
                <Box sx={{ textAlign: 'center' }}>
                  <Box
                    sx={{
                      fontSize: '120px',
                      animation: 'bounce 2s ease-in-out infinite 0.6s',
                    }}
                  >
                    🍇
                  </Box>
                  <Box
                    sx={{
                      fontSize: '120px',
                      animation: 'bounce 2s ease-in-out infinite 0.9s',
                    }}
                  >
                    🥦
                  </Box>
                </Box>
              </Box>
            </Grid>
          </Grid>
        </Container>
      </Box>

      {/* CTA Section */}
      <Container maxWidth="md" sx={{ py: 10, textAlign: 'center' }}>
        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.8 }}
        >
          <Box
            sx={{
              background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
              borderRadius: 4,
              p: 6,
              color: '#fff',
              position: 'relative',
              overflow: 'hidden',
            }}
          >
            <Box
              sx={{
                position: 'absolute',
                top: -50,
                right: -50,
                width: 200,
                height: 200,
                borderRadius: '50%',
                background: alpha('#fff', 0.1),
                filter: 'blur(50px)',
              }}
            />
            <Typography variant="h3" fontWeight="bold" gutterBottom>
              Ready to Transform Your Nutrition?
            </Typography>
            <Typography variant="h6" sx={{ mb: 4, opacity: 0.95 }}>
              Join thousands of users making smarter food choices every day
            </Typography>
            <Button
              variant="contained"
              size="large"
              endIcon={<ArrowForward />}
              onClick={() => navigate(user ? '/scan' : '/signup')}
              sx={{
                bgcolor: '#fff',
                color: '#667eea',
                px: 6,
                py: 2,
                fontSize: '1.2rem',
                fontWeight: 'bold',
                '&:hover': {
                  bgcolor: '#f0f0f0',
                  transform: 'scale(1.05)',
                  boxShadow: '0 10px 30px rgba(0,0,0,0.3)',
                },
                transition: 'all 0.3s',
              }}
            >
              {user ? 'Start Scanning Now' : 'Sign Up Free'}
            </Button>
          </Box>
        </motion.div>
      </Container>
    </Box>
  );
};

export default HomePage;
