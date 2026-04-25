  Project: EV Charging Demand Prediction & Smart Energy Management                                                                                                                                                                                                                                                                                                      
                 
  Project Overview                                                                                                                                                                                                   
                                                                                                                                                                                                                     
    This project involves the design and implementation of an AI-powered EV charging analytics system that predicts energy consumption and enables smart charging decisions for electric vehicle users and station
    operators.
  
    - Milestone 1: Classical machine learning techniques applied to historical charging session data to predict energy demand and identify key consumption drivers.
    ---
    Constraints & Requirements
  
    - Team Size: 4 Student
    - API Budget: None (Local ML Inference)
    - Framework: Scikit-learn, Streamlit
    - Hosting:Streamlit Cloud 

  ---
  Technology Stack

       Component        │              Technology               
    ML Models           │ Random Forest Regressor, Scikit-Learn 
        Data Processing │ Pandas, NumPy               
    UI Framework        │ Streamlit  
    Model Serialization │ Joblib                                
  ---
  Project Structure

    GenAi_capstone/
    ├── app.py                    # Streamlit web application
    ├── src/
    │   └── train_model.py        # Model training script
    ├── data/
    │   └── Raw_Dataset.csv       # Training data
    ├── models/
    │   └── ev_demand_model.pkl   # Trained ML model
    ├── notebooks/
    │   └── ev_charging_eda.ipynb # EDA & model development
    ├── requirements.txt          # Python dependencies
    └── runtime.txt               # Python version specification

  ---
  Quick Start

    # Clone repository
    git clone <repository-url>
  
    # Install dependencies
    pip install -r requirements.txt
  
    # Train model
    python src/train_model.py
  
    # Run application
    streamlit run app.py

  ---
  Model Performance


    Metric   │  Value 
    R² Score │ 0.96 
    MAE      │ 3.76 kWh 
    RMSE     │ 6.08 kWh 

  ---
  Key Features

    1. Custom Data Pre-processing Pipeline - Missing value imputation, feature engineering, and categorical encoding
    2. Real-time Model Inference - Instant predictions using scikit-learn Pipeline architecture
    3. Interactive Web Interface - Streamlit-based dashboard with intuitive controls and validation
  
