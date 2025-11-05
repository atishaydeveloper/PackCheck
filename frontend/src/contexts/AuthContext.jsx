import React, { createContext, useState, useContext, useEffect } from 'react';

const AuthContext = createContext(null);

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  // Load user from localStorage on mount
  useEffect(() => {
    const storedUser = localStorage.getItem('packcheck_user');
    if (storedUser) {
      setUser(JSON.parse(storedUser));
    }
    setLoading(false);
  }, []);

  const signup = (userData) => {
    // Get existing users
    const users = JSON.parse(localStorage.getItem('packcheck_users') || '[]');

    // Check if email already exists
    if (users.find(u => u.email === userData.email)) {
      throw new Error('Email already exists');
    }

    // Create new user with ID and timestamp
    const newUser = {
      id: Date.now().toString(),
      ...userData,
      createdAt: new Date().toISOString(),
      dailyGoals: {
        calories: 2000,
        protein: 50,
        carbs: 250,
        fat: 70,
        fiber: 25,
        sodium: 2000
      },
      preferences: {
        dietType: 'balanced',
        allergies: [],
        restrictions: [],
        fitnessGoal: 'maintain'
      },
      history: [],
      dailyIntake: {}
    };

    // Save user to users list
    users.push(newUser);
    localStorage.setItem('packcheck_users', JSON.stringify(users));

    // Set current user
    localStorage.setItem('packcheck_user', JSON.stringify(newUser));
    setUser(newUser);

    return newUser;
  };

  const login = (email, password) => {
    const users = JSON.parse(localStorage.getItem('packcheck_users') || '[]');
    const foundUser = users.find(u => u.email === email && u.password === password);

    if (!foundUser) {
      throw new Error('Invalid email or password');
    }

    localStorage.setItem('packcheck_user', JSON.stringify(foundUser));
    setUser(foundUser);
    return foundUser;
  };

  const logout = () => {
    localStorage.removeItem('packcheck_user');
    setUser(null);
  };

  const updateUser = (updates) => {
    const users = JSON.parse(localStorage.getItem('packcheck_users') || '[]');
    const updatedUsers = users.map(u =>
      u.id === user.id ? { ...u, ...updates } : u
    );

    const updatedUser = { ...user, ...updates };

    localStorage.setItem('packcheck_users', JSON.stringify(updatedUsers));
    localStorage.setItem('packcheck_user', JSON.stringify(updatedUser));
    setUser(updatedUser);

    return updatedUser;
  };

  const addToHistory = (scanResult) => {
    const historyItem = {
      id: Date.now().toString(),
      timestamp: new Date().toISOString(),
      ...scanResult
    };

    const updatedHistory = [historyItem, ...(user.history || [])];
    updateUser({ history: updatedHistory });
  };

  const updateDailyIntake = (date, nutrition) => {
    const dateKey = date || new Date().toISOString().split('T')[0];
    const currentIntake = user.dailyIntake || {};

    const todayIntake = currentIntake[dateKey] || {
      calories: 0,
      protein: 0,
      carbs: 0,
      fat: 0,
      fiber: 0,
      sodium: 0,
      items: []
    };

    // Add nutrition values
    const updatedIntake = {
      calories: (todayIntake.calories || 0) + (nutrition.calories || 0),
      protein: (todayIntake.protein || 0) + (nutrition.protein || 0),
      carbs: (todayIntake.carbs || 0) + (nutrition.carbohydrates || 0),
      fat: (todayIntake.fat || 0) + (nutrition.fat || 0),
      fiber: (todayIntake.fiber || 0) + (nutrition.fiber || 0),
      sodium: (todayIntake.sodium || 0) + (nutrition.sodium || 0),
      items: [...todayIntake.items, {
        timestamp: new Date().toISOString(),
        nutrition
      }]
    };

    updateUser({
      dailyIntake: {
        ...currentIntake,
        [dateKey]: updatedIntake
      }
    });
  };

  const value = {
    user,
    loading,
    signup,
    login,
    logout,
    updateUser,
    addToHistory,
    updateDailyIntake,
    isAuthenticated: !!user
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};
