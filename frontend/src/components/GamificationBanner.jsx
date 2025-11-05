import React from 'react';
import { Box, Grid, Typography, LinearProgress, Chip, Avatar } from '@mui/material';
import { motion } from 'framer-motion';
import { useGamification } from '../contexts/GamificationContext';
import { EmojiEvents, LocalFireDepartment, Star } from '@mui/icons-material';

function GamificationBanner() {
  const { gamification, levelInfo, achievements } = useGamification();

  if (!gamification) return null;

  const progressToNext = ((gamification.points - levelInfo.minPoints) /
    (levelInfo.maxPoints - levelInfo.minPoints)) * 100;

  const unlockedAchievements = achievements.filter(a =>
    gamification.achievements.includes(a.id)
  );

  return (
    <motion.div
      initial={{ opacity: 0, y: -20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      <Box
        sx={{
          background: 'linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #ec4899 100%)',
          borderRadius: 4,
          p: 3,
          color: '#fff',
          mb: 4,
          boxShadow: '0 10px 40px rgba(99, 102, 241, 0.3)',
          position: 'relative',
          overflow: 'hidden',
        }}
      >
        {/* Animated background effect */}
        <Box
          sx={{
            position: 'absolute',
            top: 0,
            left: 0,
            right: 0,
            bottom: 0,
            opacity: 0.1,
            background: 'radial-gradient(circle at 20% 50%, white 0%, transparent 50%)',
          }}
        />

        <Grid container spacing={3} alignItems="center" sx={{ position: 'relative' }}>
          {/* Level Badge */}
          <Grid item xs={12} sm={6} md={3}>
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
              <motion.div
                animate={{ rotate: [0, 360] }}
                transition={{ duration: 20, repeat: Infinity, ease: 'linear' }}
              >
                <Avatar
                  sx={{
                    width: 70,
                    height: 70,
                    bgcolor: 'rgba(255, 255, 255, 0.2)',
                    fontSize: '2rem',
                  }}
                >
                  <EmojiEvents sx={{ fontSize: '2rem' }} />
                </Avatar>
              </motion.div>
              <Box>
                <Typography variant="caption" sx={{ opacity: 0.9 }}>
                  Level {levelInfo.level}
                </Typography>
                <Typography variant="h5" fontWeight="bold">
                  {levelInfo.title}
                </Typography>
                <Typography variant="caption" sx={{ opacity: 0.8 }}>
                  {gamification.points} points
                </Typography>
              </Box>
            </Box>
          </Grid>

          {/* Progress to Next Level */}
          <Grid item xs={12} sm={6} md={4}>
            <Typography variant="caption" sx={{ opacity: 0.9, mb: 1, display: 'block' }}>
              Progress to Level {levelInfo.level + 1}
            </Typography>
            <LinearProgress
              variant="determinate"
              value={progressToNext}
              sx={{
                height: 12,
                borderRadius: 6,
                backgroundColor: 'rgba(255, 255, 255, 0.2)',
                '& .MuiLinearProgress-bar': {
                  background: 'linear-gradient(90deg, #FFD700 0%, #FFA500 100%)',
                  borderRadius: 6,
                },
              }}
            />
            <Typography variant="caption" sx={{ opacity: 0.8, mt: 0.5, display: 'block' }}>
              {gamification.points - levelInfo.minPoints} / {levelInfo.maxPoints - levelInfo.minPoints} XP
            </Typography>
          </Grid>

          {/* Streak */}
          <Grid item xs={6} sm={6} md={2}>
            <Box sx={{ textAlign: 'center' }}>
              <motion.div
                animate={{ scale: [1, 1.1, 1] }}
                transition={{ duration: 2, repeat: Infinity }}
              >
                <LocalFireDepartment sx={{ fontSize: '3rem', color: '#FFD700' }} />
              </motion.div>
              <Typography variant="h4" fontWeight="bold">
                {gamification.streak}
              </Typography>
              <Typography variant="caption" sx={{ opacity: 0.9 }}>
                Day Streak
              </Typography>
            </Box>
          </Grid>

          {/* Achievements */}
          <Grid item xs={6} sm={6} md={3}>
            <Box>
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 1 }}>
                <Star sx={{ color: '#FFD700' }} />
                <Typography variant="body2" fontWeight="bold">
                  {unlockedAchievements.length}/{achievements.length} Achievements
                </Typography>
              </Box>
              <Box sx={{ display: 'flex', gap: 0.5, flexWrap: 'wrap' }}>
                {unlockedAchievements.slice(0, 6).map((achievement) => (
                  <motion.div
                    key={achievement.id}
                    whileHover={{ scale: 1.2 }}
                    whileTap={{ scale: 0.9 }}
                  >
                    <Chip
                      label={achievement.icon}
                      size="small"
                      sx={{
                        bgcolor: 'rgba(255, 255, 255, 0.2)',
                        color: '#fff',
                        fontWeight: 'bold',
                      }}
                    />
                  </motion.div>
                ))}
                {unlockedAchievements.length > 6 && (
                  <Chip
                    label={`+${unlockedAchievements.length - 6}`}
                    size="small"
                    sx={{
                      bgcolor: 'rgba(255, 255, 255, 0.2)',
                      color: '#fff',
                    }}
                  />
                )}
              </Box>
            </Box>
          </Grid>
        </Grid>
      </Box>
    </motion.div>
  );
}

export default GamificationBanner;
