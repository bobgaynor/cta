# src/model.py

from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report, confusion_matrix

def train_model(X, y):
    """
    Splits data and trains a Decision Tree Classifier.
    """
    print("Splitting data for training and testing...")
    
    # Reserve 20% of the data for testing.
    # random_state=42 ensures that the split is the same every time.
    # stratify=y ensures the training and test sets have a similar
    # proportion of "Signal" (threats) to "Noise" (normal logs).
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    print(f"Training set size: {len(X_train)} logs")
    print(f"Test set size: {len(X_test)} logs")

    # Create and train the Decision Tree model.
    model = DecisionTreeClassifier(random_state=42)
    model.fit(X_train, y_train)
    
    print("--- Model Training Complete ---")
    
    # Return the trained model and the test data for evaluation.
    return model, X_test, y_test

def evaluate_model(model, X_test, y_test):
    """
    Evaluates the model on the test set and prints performance metrics.
    """
    print("Evaluating model performance on test data...")
    
    # Generate predictions on the unseen test data.
    y_pred = model.predict(X_test)

    # --- Generate the "Signal" Report ---
    print("\n--- Classification Report ---")
    print("This report shows the model's ability to distinguish the Signal from the Noise.")
    print(classification_report(y_test, y_pred, target_names=['Noise (0)', 'Signal (1)']))

    print("\n--- Confusion Matrix ---")
    print("This matrix shows the raw counts of correct and incorrect predictions.")
    cm = confusion_matrix(y_test, y_pred)
    
    # --- Readable Matrix ---
    print("\n--- Readable Confusion Matrix ---")
    print(f"                 PREDICTED")
    print(f"                 Noise (0)   Signal (1)")
    print(f"ACTUAL Noise (0)    {cm[0][0]:<10} {cm[0][1]:<10}")
    print(f"ACTUAL Signal (1)   {cm[1][0]:<10} {cm[1][1]:<10}")
    
    print("\n--- Model Evaluation Complete ---")
