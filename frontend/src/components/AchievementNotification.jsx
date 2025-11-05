import React from 'react';
import { Box, Typography } from '@mui/material';
import { motion, AnimatePresence } from 'framer-motion';
import { useGamification } from '../contexts/GamificationContext';

function AchievementNotification() {
  const { newAchievement } = useGamification();

  return (
    <AnimatePresence>
      {newAchievement && (
        <motion.div
          initial={{ opacity: 0, x: 300 }}
          animate={{ opacity: 1, x: 0 }}
          exit={{ opacity: 0, x: 300 }}
          transition={{ type: 'spring', stiffness: 100 }}
          style={{
            position: 'fixed',
            top: 80,
            right: 20,
            zIndex: 9999,
          }}
        >
          <Box
            sx={{
              background: 'linear-gradient(135deg, #6366f1 0%, #ec4899 100%)',
              borderRadius: 3,
              p: 2,
              boxShadow: '0 10px 40px rgba(99, 102, 241, 0.4)',
              minWidth: 280,
              border: '2px solid rgba(255, 255, 255, 0.3)',
            }}
          >
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
              <Typography variant="h3">{newAchievement.icon}</Typography>
              <Box>
                <Typography
                  variant="caption"
                  sx={{ color: '#fff', opacity: 0.9, textTransform: 'uppercase', fontWeight: 700 }}
                >
                  Achievement Unlocked!
                </Typography>
                <Typography variant="h6" fontWeight="bold" sx={{ color: '#fff' }}>
                  {newAchievement.name}
                </Typography>
                <Typography variant="body2" sx={{ color: '#fff', opacity: 0.9 }}>
                  {newAchievement.description}
                </Typography>
                <Typography variant="caption" sx={{ color: '#FFD700', fontWeight: 700 }}>
                  +{newAchievement.points} points
                </Typography>
              </Box>
            </Box>
          </Box>
        </motion.div>
      )}
    </AnimatePresence>
  );
}

export default AchievementNotification;
