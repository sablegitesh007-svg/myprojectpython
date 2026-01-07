"""
AI Model for Predicting Service Request Resolution Time
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
import joblib
import os


class ServiceRequestPredictor:
    """AI model to predict service request resolution time."""
    
    def __init__(self):
        self.model = None
        self.category_encoder = LabelEncoder()
        self.priority_encoder = LabelEncoder()
        self.assigned_team_encoder = LabelEncoder()
        self.model_file = 'service_request_model.pkl'
        self.encoders_file = 'encoders.pkl'
        
    def generate_sample_data(self, n_samples=500):
        """Generate sample training data for demonstration."""
        np.random.seed(42)
        
        categories = ['Hardware', 'Software', 'Network', 'Database', 'Security', 'Application']
        priorities = ['Low', 'Medium', 'High', 'Critical']
        assigned_teams = ['IT Support', 'Development', 'Network Team', 'Database Team', 'Security Team']
        
        data = {
            'category': np.random.choice(categories, n_samples),
            'priority': np.random.choice(priorities, n_samples),
            'assigned_team': np.random.choice(assigned_teams, n_samples),
            'complexity_score': np.random.uniform(1, 10, n_samples),
            'request_age_hours': np.random.uniform(0, 168, n_samples),  # 0-7 days
            'previous_interactions': np.random.randint(0, 10, n_samples),
        }
        
        df = pd.DataFrame(data)
        
        # Calculate resolution time based on features (simulating real-world patterns)
        base_time = 2.0  # base hours
        
        priority_multipliers = {
            'Critical': 0.5,  # Faster resolution
            'High': 1.0,
            'Medium': 2.0,
            'Low': 4.0
        }
        
        complexity_multipliers = {
            'Hardware': 1.5,
            'Software': 1.2,
            'Network': 2.0,
            'Database': 2.5,
            'Security': 3.0,
            'Application': 1.8
        }
        
        df['resolution_time_hours'] = (
            base_time * 
            df['priority'].map(priority_multipliers) *
            df['category'].map(complexity_multipliers) *
            (1 + df['complexity_score'] / 10) *
            (1 + df['previous_interactions'] / 20) +
            np.random.normal(0, 2, n_samples)  # Add some noise
        )
        
        # Ensure positive resolution times
        df['resolution_time_hours'] = np.maximum(df['resolution_time_hours'], 0.5)
        
        return df
    
    def prepare_features(self, df):
        """Prepare features for training/prediction."""
        df = df.copy()
        
        # Encode categorical variables
        if not hasattr(self, 'category_fitted'):
            df['category_encoded'] = self.category_encoder.fit_transform(df['category'])
            df['priority_encoded'] = self.priority_encoder.fit_transform(df['priority'])
            df['assigned_team_encoded'] = self.assigned_team_encoder.fit_transform(df['assigned_team'])
            self.category_fitted = True
        else:
            # Handle unseen categories
            try:
                df['category_encoded'] = self.category_encoder.transform(df['category'])
            except:
                df['category_encoded'] = 0
            
            try:
                df['priority_encoded'] = self.priority_encoder.transform(df['priority'])
            except:
                df['priority_encoded'] = 1
            
            try:
                df['assigned_team_encoded'] = self.assigned_team_encoder.transform(df['assigned_team'])
            except:
                df['assigned_team_encoded'] = 0
        
        # Select features for model
        feature_columns = [
            'category_encoded',
            'priority_encoded',
            'assigned_team_encoded',
            'complexity_score',
            'request_age_hours',
            'previous_interactions'
        ]
        
        return df[feature_columns]
    
    def train(self, df=None):
        """Train the prediction model."""
        if df is None:
            df = self.generate_sample_data()
        
        # Prepare features
        X = self.prepare_features(df)
        y = df['resolution_time_hours']
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Train model
        self.model = RandomForestRegressor(
            n_estimators=100,
            max_depth=10,
            random_state=42,
            n_jobs=-1
        )
        
        self.model.fit(X_train, y_train)
        
        # Evaluate
        train_score = self.model.score(X_train, y_train)
        test_score = self.model.score(X_test, y_test)
        
        print(f"Model trained successfully!")
        print(f"Training R² Score: {train_score:.4f}")
        print(f"Test R² Score: {test_score:.4f}")
        
        # Save model
        self.save_model()
        
        return train_score, test_score
    
    def predict(self, category, priority, assigned_team, complexity_score, 
                request_age_hours=0, previous_interactions=0):
        """Predict resolution time for a service request."""
        if self.model is None:
            # Load or train model if not available
            if not self.load_model():
                print("Training new model...")
                self.train()
        
        # Create input dataframe
        input_data = pd.DataFrame({
            'category': [category],
            'priority': [priority],
            'assigned_team': [assigned_team],
            'complexity_score': [complexity_score],
            'request_age_hours': [request_age_hours],
            'previous_interactions': [previous_interactions]
        })
        
        # Prepare features
        X = self.prepare_features(input_data)
        
        # Predict
        prediction = self.model.predict(X)[0]
        
        return max(prediction, 0.5)  # Ensure positive prediction
    
    def save_model(self):
        """Save the trained model and encoders."""
        if self.model is not None:
            joblib.dump(self.model, self.model_file)
            joblib.dump({
                'category': self.category_encoder,
                'priority': self.priority_encoder,
                'assigned_team': self.assigned_team_encoder
            }, self.encoders_file)
            print(f"Model saved to {self.model_file}")
    
    def load_model(self):
        """Load the trained model and encoders."""
        try:
            if os.path.exists(self.model_file) and os.path.exists(self.encoders_file):
                self.model = joblib.load(self.model_file)
                encoders = joblib.load(self.encoders_file)
                self.category_encoder = encoders['category']
                self.priority_encoder = encoders['priority']
                self.assigned_team_encoder = encoders['assigned_team']
                self.category_fitted = True
                print(f"Model loaded from {self.model_file}")
                return True
        except Exception as e:
            print(f"Error loading model: {e}")
        return False


# Initialize global predictor instance
predictor = ServiceRequestPredictor()

# Train model on startup if no saved model exists
if not os.path.exists('service_request_model.pkl'):
    print("No saved model found. Training new model...")
    predictor.train()


