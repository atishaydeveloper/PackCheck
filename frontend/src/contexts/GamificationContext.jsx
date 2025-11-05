import React, { createContext, useContext, useState, useEffect } from 'react';
import { useAuth } from './AuthContext';
import confetti from 'canvas-confetti';

const GamificationContext = createContext(null);

export const useGamification = () => useContext(GamificationContext);

// Achievement definitions
const ACHIEVEMENTS = [
  { id: 'first_scan', name: 'First Steps', description: 'Scan your first product', points: 10, icon: '🎯' },
  { id: 'scan_5', name: 'Scanner', description: 'Scan 5 products', points: 25, icon: '📸' },
  { id: 'scan_10', name: 'Product Hunter', description: 'Scan 10 products', points: 50, icon: '🔍' },
  { id: 'scan_50', name: 'Label Master', description: 'Scan 50 products', points: 200, icon: '👑' },
  { id: 'streak_3', name: 'Consistent', description: '3 day streak', points: 30, icon: '🔥' },
  { id: 'streak_7', name: 'Week Warrior', description: '7 day streak', points: 70, icon: '⚡' },
  { id: 'streak_30', name: 'Monthly Legend', description: '30 day streak', points: 300, icon: '🏆' },
  { id: 'goal_met', name: 'Goal Getter', description: 'Meet all daily goals', points: 50, icon: '✨' },
  { id: 'goal_week', name: 'Weekly Champion', description: 'Meet goals for 7 days', points: 150, icon: '💪' },
  { id: 'protein_king', name: 'Protein King', description: 'Hit protein goal 10 times', points: 100, icon: '🥩' },
  { id: 'healthy_choice', name: 'Healthy Choice', description: 'Scan 10 compliant products', points: 80, icon: '🥗' },
];

// Level thresholds
const LEVELS = [
  { level: 1, minPoints: 0, maxPoints: 100, title: 'Beginner', color: '#9E9E9E' },
  { level: 2, minPoints: 100, maxPoints: 250, title: 'Novice', color: '#8BC34A' },
  { level: 3, minPoints: 250, maxPoints: 500, title: 'Explorer', color: '#4CAF50' },
  { level: 4, minPoints: 500, maxPoints: 1000, title: 'Expert', color: '#2196F3' },
  { level: 5, minPoints: 1000, maxPoints: 2000, title: 'Master', color: '#9C27B0' },
  { level: 6, minPoints: 2000, maxPoints: 5000, title: 'Champion', color: '#FF9800' },
  { level: 7, minPoints: 5000, maxPoints: 10000, title: 'Legend', color: '#F44336' },
  { level: 8, minPoints: 10000, maxPoints: Infinity, title: 'Nutrition God', color: '#FFD700' },
];

export const GamificationProvider = ({ children }) => {
  const { user, updateUser } = useAuth();
  const [showLevelUp, setShowLevelUp] = useState(false);
  const [newAchievement, setNewAchievement] = useState(null);

  useEffect(() => {
    if (user && !user.gamification) {
      // Initialize gamification data
      updateUser({
        gamification: {
          points: 0,
          level: 1,
          achievements: [],
          streak: 0,
          lastActive: new Date().toISOString().split('T')[0],
          stats: {
            totalScans: 0,
            goalsMetDays: 0,
            proteinGoalsHit: 0,
            compliantProducts: 0
          }
        }
      });
    }
  }, [user]);

  const fireConfetti = () => {
    confetti({
      particleCount: 100,
      spread: 70,
      origin: { y: 0.6 }
    });
  };

  const fireLevelUpConfetti = () => {
    const duration = 3 * 1000;
    const end = Date.now() + duration;

    const frame = () => {
      confetti({
        particleCount: 2,
        angle: 60,
        spread: 55,
        origin: { x: 0 },
        colors: ['#FFD700', '#FFA500', '#FF4500']
      });
      confetti({
        particleCount: 2,
        angle: 120,
        spread: 55,
        origin: { x: 1 },
        colors: ['#FFD700', '#FFA500', '#FF4500']
      });

      if (Date.now() < end) {
        requestAnimationFrame(frame);
      }
    };
    frame();
  };

  const getLevelInfo = (points) => {
    return LEVELS.find(l => points >= l.minPoints && points < l.maxPoints) || LEVELS[LEVELS.length - 1];
  };

  const addPoints = (points, reason = '') => {
    if (!user?.gamification) return;

    const newPoints = user.gamification.points + points;
    const oldLevel = getLevelInfo(user.gamification.points).level;
    const newLevel = getLevelInfo(newPoints).level;

    updateUser({
      gamification: {
        ...user.gamification,
        points: newPoints
      }
    });

    if (newLevel > oldLevel) {
      setShowLevelUp(true);
      fireLevelUpConfetti();
      setTimeout(() => setShowLevelUp(false), 3000);
    } else {
      fireConfetti();
    }
  };

  const unlockAchievement = (achievementId) => {
    if (!user?.gamification) return;

    const achievement = ACHIEVEMENTS.find(a => a.id === achievementId);
    if (!achievement) return;

    const alreadyUnlocked = user.gamification.achievements.includes(achievementId);
    if (alreadyUnlocked) return;

    updateUser({
      gamification: {
        ...user.gamification,
        achievements: [...user.gamification.achievements, achievementId],
        points: user.gamification.points + achievement.points
      }
    });

    setNewAchievement(achievement);
    fireConfetti();
    setTimeout(() => setNewAchievement(null), 4000);
  };

  const updateStreak = () => {
    if (!user?.gamification) return;

    const today = new Date().toISOString().split('T')[0];
    const lastActive = user.gamification.lastActive;

    const yesterday = new Date();
    yesterday.setDate(yesterday.getDate() - 1);
    const yesterdayStr = yesterday.toISOString().split('T')[0];

    let newStreak = user.gamification.streak;

    if (lastActive === today) {
      // Already logged today
      return;
    } else if (lastActive === yesterdayStr) {
      // Consecutive day
      newStreak++;
    } else {
      // Streak broken
      newStreak = 1;
    }

    updateUser({
      gamification: {
        ...user.gamification,
        streak: newStreak,
        lastActive: today
      }
    });

    // Check streak achievements
    if (newStreak === 3) unlockAchievement('streak_3');
    if (newStreak === 7) unlockAchievement('streak_7');
    if (newStreak === 30) unlockAchievement('streak_30');
  };

  const onScan = (scanResult) => {
    if (!user?.gamification) return;

    const newStats = {
      ...user.gamification.stats,
      totalScans: user.gamification.stats.totalScans + 1
    };

    if (scanResult.compliance?.fssai_verification?.overall_compliance) {
      newStats.compliantProducts++;
    }

    updateUser({
      gamification: {
        ...user.gamification,
        stats: newStats
      }
    });

    updateStreak();
    addPoints(5, 'Product scanned');

    // Check scan achievements
    const scans = newStats.totalScans;
    if (scans === 1) unlockAchievement('first_scan');
    if (scans === 5) unlockAchievement('scan_5');
    if (scans === 10) unlockAchievement('scan_10');
    if (scans === 50) unlockAchievement('scan_50');
    if (newStats.compliantProducts === 10) unlockAchievement('healthy_choice');
  };

  const onGoalsMet = () => {
    if (!user?.gamification) return;

    const newStats = {
      ...user.gamification.stats,
      goalsMetDays: user.gamification.stats.goalsMetDays + 1
    };

    updateUser({
      gamification: {
        ...user.gamification,
        stats: newStats
      }
    });

    addPoints(20, 'Daily goals met!');
    unlockAchievement('goal_met');

    if (newStats.goalsMetDays === 7) unlockAchievement('goal_week');
  };

  const onProteinGoal = () => {
    if (!user?.gamification) return;

    const newStats = {
      ...user.gamification.stats,
      proteinGoalsHit: user.gamification.stats.proteinGoalsHit + 1
    };

    updateUser({
      gamification: {
        ...user.gamification,
        stats: newStats
      }
    });

    if (newStats.proteinGoalsHit === 10) unlockAchievement('protein_king');
  };

  const value = {
    gamification: user?.gamification,
    levelInfo: getLevelInfo(user?.gamification?.points || 0),
    achievements: ACHIEVEMENTS,
    addPoints,
    unlockAchievement,
    onScan,
    onGoalsMet,
    onProteinGoal,
    updateStreak,
    showLevelUp,
    newAchievement,
    LEVELS
  };

  return (
    <GamificationContext.Provider value={value}>
      {children}
    </GamificationContext.Provider>
  );
};
