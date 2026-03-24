"""
Database utilities for Plant Disease Detection System
Now supports MySQL (preferred) with fallback to SQLite.
"""

import os
from datetime import datetime
from typing import List, Dict, Optional, Any

import pandas as pd
import sqlite3

try:
    import pymysql  # type: ignore
except Exception:  # pragma: no cover - optional dependency
    pymysql = None

from config import DATABASE_PATH, MYSQL_CONFIG

class PlantDiseaseDB:
    """Database handler for plant disease predictions"""
    
    def __init__(self, db_path: str = DATABASE_PATH):
        self.db_path = db_path
        self.backend = 'sqlite'
        self.mysql_conn = None  # type: Optional[Any]
        self._init_backend()
        self.init_database()

    def _init_backend(self):
        """Attempt to connect to MySQL; fall back to SQLite on failure."""
        if pymysql is None:
            return  # SQLite only
        try:
            # First connect to server to ensure DB exists
            server_conn = pymysql.connect(
                host=MYSQL_CONFIG['host'],
                port=MYSQL_CONFIG.get('port', 3306),
                user=MYSQL_CONFIG['user'],
                password=MYSQL_CONFIG['password'],
                cursorclass=pymysql.cursors.DictCursor,
                autocommit=True,
            )
            with server_conn.cursor() as cur:
                cur.execute(
                    f"CREATE DATABASE IF NOT EXISTS `{MYSQL_CONFIG['database']}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
                )
            server_conn.close()

            # Connect to target database
            self.mysql_conn = pymysql.connect(
                host=MYSQL_CONFIG['host'],
                port=MYSQL_CONFIG.get('port', 3306),
                user=MYSQL_CONFIG['user'],
                password=MYSQL_CONFIG['password'],
                database=MYSQL_CONFIG['database'],
                cursorclass=pymysql.cursors.DictCursor,
                autocommit=True,
            )
            self.backend = 'mysql'
        except Exception:
            # Fall back silently to SQLite
            self.backend = 'sqlite'
    
    def init_database(self):
        """Initialize the database with required tables for the active backend."""
        if self.backend == 'mysql' and self.mysql_conn is not None:
            with self.mysql_conn.cursor() as cursor:
                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS predictions (
                        id INT PRIMARY KEY AUTO_INCREMENT,
                        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        image_path TEXT,
                        predicted_class VARCHAR(255),
                        confidence DOUBLE,
                        top_3_predictions TEXT,
                        user_feedback TEXT,
                        treatment_applied TEXT,
                        notes TEXT
                    )
                    """
                )
                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS disease_info (
                        id INT PRIMARY KEY AUTO_INCREMENT,
                        disease_name VARCHAR(255) UNIQUE,
                        description TEXT,
                        treatment TEXT,
                        prevention TEXT,
                        severity_level VARCHAR(50),
                        common_plants TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                    """
                )
                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS user_feedback (
                        id INT PRIMARY KEY AUTO_INCREMENT,
                        prediction_id INT,
                        feedback_type VARCHAR(50),
                        feedback_text TEXT,
                        accuracy_rating INT,
                        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (prediction_id) REFERENCES predictions(id)
                    )
                    """
                )
            return

        # SQLite fallback
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS predictions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    image_path TEXT,
                    predicted_class TEXT,
                    confidence REAL,
                    top_3_predictions TEXT,
                    user_feedback TEXT,
                    treatment_applied TEXT,
                    notes TEXT
                )
            ''')
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS disease_info (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    disease_name TEXT UNIQUE,
                    description TEXT,
                    treatment TEXT,
                    prevention TEXT,
                    severity_level TEXT,
                    common_plants TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS user_feedback (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    prediction_id INTEGER,
                    feedback_type TEXT,
                    feedback_text TEXT,
                    accuracy_rating INTEGER,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (prediction_id) REFERENCES predictions (id)
                )
            ''')
            conn.commit()
    
    def log_prediction(self, 
                      image_path: str,
                      predicted_class: str,
                      confidence: float,
                      top_3_predictions: List[tuple],
                      user_feedback: str = None,
                      treatment_applied: str = None,
                      notes: str = None) -> int:
        """
        Log a prediction to the database
        
        Args:
            image_path (str): Path to the input image
            predicted_class (str): Predicted disease class
            confidence (float): Confidence score
            top_3_predictions (List[tuple]): Top 3 predictions with scores
            user_feedback (str): User feedback on the prediction
            treatment_applied (str): Treatment that was applied
            notes (str): Additional notes
            
        Returns:
            int: ID of the inserted prediction
        """
        top_3_str = str(top_3_predictions)
        if self.backend == 'mysql' and self.mysql_conn is not None:
            with self.mysql_conn.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO predictions
                    (image_path, predicted_class, confidence, top_3_predictions,
                     user_feedback, treatment_applied, notes)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """,
                    (image_path, predicted_class, float(confidence), top_3_str,
                     user_feedback, treatment_applied, notes),
                )
                return cursor.lastrowid
        # SQLite
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                '''INSERT INTO predictions 
                (image_path, predicted_class, confidence, top_3_predictions, 
                 user_feedback, treatment_applied, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?)''',
                (image_path, predicted_class, float(confidence), top_3_str,
                 user_feedback, treatment_applied, notes),
            )
            pid = cursor.lastrowid
            conn.commit()
            return pid
    
    def get_predictions(self, limit: int = 100, 
                       disease_filter: str = None,
                       date_from: str = None,
                       date_to: str = None) -> pd.DataFrame:
        """
        Retrieve predictions from the database
        
        Args:
            limit (int): Maximum number of records to return
            disease_filter (str): Filter by disease name
            date_from (str): Filter from date (YYYY-MM-DD)
            date_to (str): Filter to date (YYYY-MM-DD)
            
        Returns:
            pd.DataFrame: Predictions data
        """
        if self.backend == 'mysql' and self.mysql_conn is not None:
            clauses = ["1=1"]
            params = []
            if disease_filter:
                clauses.append("predicted_class LIKE %s")
                params.append(f"%{disease_filter}%")
            if date_from:
                clauses.append("DATE(timestamp) >= %s")
                params.append(date_from)
            if date_to:
                clauses.append("DATE(timestamp) <= %s")
                params.append(date_to)
            sql = (
                "SELECT id, timestamp, image_path, predicted_class, confidence, "
                "top_3_predictions, user_feedback, treatment_applied, notes "
                f"FROM predictions WHERE {' AND '.join(clauses)} "
                "ORDER BY timestamp DESC LIMIT %s"
            )
            params.append(int(limit))
            with self.mysql_conn.cursor() as cur:
                cur.execute(sql, params)
                rows = cur.fetchall()
            return pd.DataFrame(rows)

        # SQLite
        with sqlite3.connect(self.db_path) as conn:
            query = (
                'SELECT id, timestamp, image_path, predicted_class, '
                'confidence, top_3_predictions, user_feedback, '
                'treatment_applied, notes FROM predictions WHERE 1=1'
            )
            params = []
            if disease_filter:
                query += ' AND predicted_class LIKE ?'
                params.append(f'%{disease_filter}%')
            if date_from:
                query += ' AND DATE(timestamp) >= ?'
                params.append(date_from)
            if date_to:
                query += ' AND DATE(timestamp) <= ?'
                params.append(date_to)
            query += ' ORDER BY timestamp DESC LIMIT ?'
            params.append(int(limit))
            return pd.read_sql_query(query, conn, params=params)
    
    def add_user_feedback(self, prediction_id: int, 
                         feedback_type: str,
                         feedback_text: str = None,
                         accuracy_rating: int = None) -> int:
        """
        Add user feedback for a prediction
        
        Args:
            prediction_id (int): ID of the prediction
            feedback_type (str): Type of feedback (correct, incorrect, etc.)
            feedback_text (str): Text feedback
            accuracy_rating (int): Rating from 1-5
            
        Returns:
            int: ID of the inserted feedback
        """
        if self.backend == 'mysql' and self.mysql_conn is not None:
            with self.mysql_conn.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO user_feedback
                    (prediction_id, feedback_type, feedback_text, accuracy_rating)
                    VALUES (%s, %s, %s, %s)
                    """,
                    (prediction_id, feedback_type, feedback_text, accuracy_rating),
                )
                return cursor.lastrowid
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                '''INSERT INTO user_feedback 
                (prediction_id, feedback_type, feedback_text, accuracy_rating)
                VALUES (?, ?, ?, ?)''',
                (prediction_id, feedback_type, feedback_text, accuracy_rating),
            )
            fid = cursor.lastrowid
            conn.commit()
            return fid
    
    def get_disease_statistics(self) -> Dict:
        """
        Get statistics about predicted diseases
        
        Returns:
            Dict: Disease statistics
        """
        if self.backend == 'mysql' and self.mysql_conn is not None:
            with self.mysql_conn.cursor() as cursor:
                cursor.execute(
                    '''SELECT predicted_class, COUNT(*) as count, AVG(confidence) as avg_confidence
                       FROM predictions GROUP BY predicted_class ORDER BY count DESC'''
                )
                disease_stats = [tuple(d.values()) for d in cursor.fetchall()]
                cursor.execute('SELECT COUNT(*) AS c FROM predictions')
                total_predictions = cursor.fetchone()['c']
                cursor.execute('SELECT AVG(confidence) AS a FROM predictions')
                avg_confidence = cursor.fetchone()['a'] or 0
            return {
                'total_predictions': total_predictions,
                'average_confidence': avg_confidence,
                'disease_distribution': disease_stats,
            }
        # SQLite
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT predicted_class, COUNT(*) as count, 
                       AVG(confidence) as avg_confidence
                FROM predictions
                GROUP BY predicted_class
                ORDER BY count DESC
            ''')
            disease_stats = cursor.fetchall()
            cursor.execute('SELECT COUNT(*) FROM predictions')
            total_predictions = cursor.fetchone()[0]
            cursor.execute('SELECT AVG(confidence) FROM predictions')
            avg_confidence = cursor.fetchone()[0] or 0
            return {
                'total_predictions': total_predictions,
                'average_confidence': avg_confidence,
                'disease_distribution': disease_stats
            }
    
    def get_accuracy_metrics(self) -> Dict:
        """
        Get accuracy metrics based on user feedback
        
        Returns:
            Dict: Accuracy metrics
        """
        if self.backend == 'mysql' and self.mysql_conn is not None:
            with self.mysql_conn.cursor() as cursor:
                cursor.execute('SELECT feedback_type, COUNT(*) as count FROM user_feedback GROUP BY feedback_type')
                rows = cursor.fetchall()
                feedback_stats = {r['feedback_type']: r['count'] for r in rows}
                cursor.execute('SELECT AVG(accuracy_rating) AS a FROM user_feedback WHERE accuracy_rating IS NOT NULL')
                avg_rating = cursor.fetchone()['a'] or 0
            return {'feedback_distribution': feedback_stats, 'average_rating': avg_rating}
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT feedback_type, COUNT(*) as count FROM user_feedback GROUP BY feedback_type')
            feedback_stats = dict(cursor.fetchall())
            cursor.execute('SELECT AVG(accuracy_rating) FROM user_feedback WHERE accuracy_rating IS NOT NULL')
            avg_rating = cursor.fetchone()[0] or 0
            return {'feedback_distribution': feedback_stats, 'average_rating': avg_rating}
    
    def update_disease_info(self, disease_name: str, 
                           description: str = None,
                           treatment: str = None,
                           prevention: str = None,
                           severity_level: str = None,
                           common_plants: str = None):
        """
        Update or insert disease information
        
        Args:
            disease_name (str): Name of the disease
            description (str): Disease description
            treatment (str): Treatment information
            prevention (str): Prevention measures
            severity_level (str): Severity level
            common_plants (str): Common plants affected
        """
        if self.backend == 'mysql' and self.mysql_conn is not None:
            with self.mysql_conn.cursor() as cursor:
                cursor.execute(
                    '''REPLACE INTO disease_info
                       (disease_name, description, treatment, prevention, severity_level, common_plants)
                       VALUES (%s, %s, %s, %s, %s, %s)''',
                    (disease_name, description, treatment, prevention, severity_level, common_plants),
                )
            return
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                '''INSERT OR REPLACE INTO disease_info 
                (disease_name, description, treatment, prevention, 
                 severity_level, common_plants)
                VALUES (?, ?, ?, ?, ?, ?)''',
                (disease_name, description, treatment, prevention, severity_level, common_plants),
            )
            conn.commit()
    
    def get_disease_info(self, disease_name: str) -> Optional[Dict]:
        """
        Get information about a specific disease
        
        Args:
            disease_name (str): Name of the disease
            
        Returns:
            Dict: Disease information or None if not found
        """
        if self.backend == 'mysql' and self.mysql_conn is not None:
            with self.mysql_conn.cursor() as cursor:
                cursor.execute(
                    '''SELECT disease_name, description, treatment, prevention, severity_level, common_plants
                       FROM disease_info WHERE disease_name = %s''',
                    (disease_name,),
                )
                row = cursor.fetchone()
                if row:
                    return dict(row)
            return None
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                '''SELECT disease_name, description, treatment, prevention,
                       severity_level, common_plants FROM disease_info WHERE disease_name = ?''',
                (disease_name,),
            )
            result = cursor.fetchone()
            if result:
                return {
                    'disease_name': result[0],
                    'description': result[1],
                    'treatment': result[2],
                    'prevention': result[3],
                    'severity_level': result[4],
                    'common_plants': result[5],
                }
            return None
    
    def export_data(self, output_path: str, format: str = 'csv'):
        """
        Export database data to file
        
        Args:
            output_path (str): Output file path
            format (str): Export format ('csv' or 'excel')
        """
        predictions_df = self.get_predictions(limit=10000)
        
        if format.lower() == 'csv':
            predictions_df.to_csv(output_path, index=False)
        elif format.lower() == 'excel':
            predictions_df.to_excel(output_path, index=False)
        else:
            raise ValueError("Format must be 'csv' or 'excel'")
        
        print(f"Data exported to {output_path}")
    
    def cleanup_old_data(self, days_old: int = 365):
        """
        Clean up old prediction data
        
        Args:
            days_old (int): Delete data older than this many days
        """
        if self.backend == 'mysql' and self.mysql_conn is not None:
            with self.mysql_conn.cursor() as cursor:
                cursor.execute(
                    f"DELETE FROM predictions WHERE timestamp < DATE_SUB(NOW(), INTERVAL {int(days_old)} DAY)"
                )
                deleted_count = cursor.rowcount
            print(f"Deleted {deleted_count} old prediction records")
            return
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                f"""
                DELETE FROM predictions 
                WHERE timestamp < datetime('now', '-{int(days_old)} days')
                """
            )
            deleted_count = cursor.rowcount
            conn.commit()
            print(f"Deleted {deleted_count} old prediction records")

def main():
    """Test the database functionality"""
    db = PlantDiseaseDB()
    
    # Test logging a prediction
    prediction_id = db.log_prediction(
        image_path="test_image.jpg",
        predicted_class="Tomato___Early_blight",
        confidence=0.95,
        top_3_predictions=[
            ("Tomato___Early_blight", 0.95),
            ("Tomato___Late_blight", 0.03),
            ("Tomato___healthy", 0.02)
        ],
        notes="Test prediction"
    )
    
    print(f"Logged prediction with ID: {prediction_id}")
    
    # Test retrieving predictions
    predictions = db.get_predictions(limit=10)
    print(f"Retrieved {len(predictions)} predictions")
    
    # Test disease statistics
    stats = db.get_disease_statistics()
    print(f"Total predictions: {stats['total_predictions']}")
    print(f"Average confidence: {stats['average_confidence']:.3f}")

if __name__ == "__main__":
    main()
