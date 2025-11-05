import React from 'react';
import { Box, Typography, Fade } from '@mui/material';
import { motion, AnimatePresence } from 'framer-motion';
import { useGamification } from '../contexts/GamificationContext';

function LevelUpNotification() {
  const { showLevelUp, levelInfo } = useGamification();

  return (
    <AnimatePresence>
      {showLevelUp && (
        <motion.div
          initial={{ opacity: 0, scale: 0.5, y: 100 }}
          animate={{ opacity: 1, scale: 1, y: 0 }}
          exit={{ opacity: 0, scale: 0.5, y: -100 }}
          transition={{ type: 'spring', duration: 0.5 }}
          style={{
            position: 'fixed',
            top: '50%',
            left: '50%',
            transform: 'translate(-50%, -50%)',
            zIndex: 9999,
          }}
        >
          <Box
            sx={{
              background: 'linear-gradient(135deg, #FFD700 0%, #FFA500 100%)',
              borderRadius: 4,
              p: 4,
              textAlign: 'center',
              boxShadow: '0 20px 60px rgba(255, 215, 0, 0.5)',
              minWidth: 300,
            }}
          >
            <motion.div
              animate={{
                scale: [1, 1.2, 1],
                rotate: [0, 360, 0],
              }}
              transition={{
                duration: 1,
                repeat: Infinity,
                repeatDelay: 0.5,
              }}
            >
              <Typography variant="h1" sx={{ fontSize: '4rem' }}>
                🎉
              </Typography>
            </motion.div>
            <Typography
              variant="h4"
              fontWeight="bold"
              sx={{ color: '#fff', mb: 1 }}
            >
              LEVEL UP!
            </Typography>
            <Typography variant="h5" sx={{ color: '#fff', mb: 1 }}>
              Level {levelInfo?.level}
            </Typography>
            <Typography variant="h6" sx={{ color: '#fff', opacity: 0.9 }}>
              {levelInfo?.title}
            </Typography>
          </Box>
        </motion.div>
      )}
    </AnimatePresence>
  );
}

export default LevelUpNotification;
