"""
Life Expectancy Prediction API
FastAPI backend for predicting life expectancy based on health and economic indicators
"""
import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, validator
import joblib
import numpy as np
from typing import Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Life Expectancy Prediction API",
    description="Predict life expectancy based on health, economic, and social indicators",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

try:
    model = joblib.load(os.path.join(BASE_DIR, "best_life_expectancy_model.pkl"))
    scaler = joblib.load(os.path.join(BASE_DIR, "life_expectancy_scaler.pkl"))
    logger.info("Model and scaler loaded successfully")
except Exception as e:
    logger.error(f"Error loading model: {e}")
    model = None
    scaler = None


# Pydantic model for input validation
class LifeExpectancyInput(BaseModel):
    """
    Input data model for life expectancy prediction
    All values must be within realistic ranges
    """
    
    adult_mortality: float = Field(
        ..., 
        ge=1.0, 
        le=1000.0,
        description="Adult Mortality rate (deaths per 1000 adults aged 15-60)"
    )
    
    infant_deaths: float = Field(
        ..., 
        ge=0.0, 
        le=2000.0,
        description="Number of infant deaths per 1000 population"
    )
    
    alcohol: float = Field(
        ..., 
        ge=0.0, 
        le=20.0,
        description="Alcohol consumption in liters per capita (15+ years)"
    )
    
    percentage_expenditure: float = Field(
        ..., 
        ge=0.0, 
        le=20000.0,
        description="Health expenditure as % of GDP per capita"
    )
    
    hepatitis_b: float = Field(
        ..., 
        ge=0.0, 
        le=100.0,
        description="Hepatitis B immunization coverage (%)"
    )
    
    measles: float = Field(
        ..., 
        ge=0.0, 
        le=500000.0,
        description="Number of reported measles cases per 1000 population"
    )
    
    bmi: float = Field(
        ..., 
        ge=10.0, 
        le=80.0,
        description="Average Body Mass Index of entire population"
    )
    
    under_five_deaths: float = Field(
        ..., 
        ge=0.0, 
        le=3000.0,
        description="Number of under-five deaths per 1000 population"
    )
    
    polio: float = Field(
        ..., 
        ge=0.0, 
        le=100.0,
        description="Polio immunization coverage (%)"
    )
    
    total_expenditure: float = Field(
        ..., 
        ge=0.0, 
        le=20.0,
        description="General government expenditure on health as % of total government expenditure"
    )
    
    diphtheria: float = Field(
        ..., 
        ge=0.0, 
        le=100.0,
        description="Diphtheria immunization coverage (%)"
    )
    
    hiv_aids: float = Field(
        ..., 
        ge=0.0, 
        le=50.0,
        description="Deaths per 1000 live births due to HIV/AIDS (0-4 years)"
    )
    
    gdp: float = Field(
        ..., 
        ge=0.0, 
        le=150000.0,
        description="Gross Domestic Product per capita (in USD)"
    )
    
    population: float = Field(
        ..., 
        ge=1000.0, 
        le=1500000000.0,
        description="Population of the country"
    )
    
    thinness_1_19_years: float = Field(
        ..., 
        ge=0.0, 
        le=30.0,
        description="Prevalence of thinness among children and adolescents (10-19 years) %"
    )
    
    thinness_5_9_years: float = Field(
        ..., 
        ge=0.0, 
        le=30.0,
        description="Prevalence of thinness among children (5-9 years) %"
    )
    
    income_composition_of_resources: float = Field(
        ..., 
        ge=0.0, 
        le=1.0,
        description="Human Development Index in terms of income composition of resources (0 to 1)"
    )
    
    schooling: float = Field(
        ..., 
        ge=0.0, 
        le=25.0,
        description="Average number of years of schooling"
    )
    
    status_numeric: int = Field(
        ..., 
        ge=0, 
        le=1,
        description="Development status: 0 for Developing, 1 for Developed"
    )
    
    # Engineered features
    immunization_avg: Optional[float] = Field(
        None,
        ge=0.0,
        le=100.0,
        description="Average immunization coverage (auto-calculated if not provided)"
    )
    
    child_health_score: Optional[float] = Field(
        None,
        description="Child health score (auto-calculated if not provided)"
    )
    
    health_spending_ratio: Optional[float] = Field(
        None,
        description="Health spending ratio (auto-calculated if not provided)"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "adult_mortality": 150.0,
                "infant_deaths": 20.0,
                "alcohol": 5.0,
                "percentage_expenditure": 500.0,
                "hepatitis_b": 85.0,
                "measles": 100.0,
                "bmi": 30.0,
                "under_five_deaths": 25.0,
                "polio": 90.0,
                "total_expenditure": 6.5,
                "diphtheria": 88.0,
                "hiv_aids": 1.0,
                "gdp": 5000.0,
                "population": 10000000.0,
                "thinness_1_19_years": 5.0,
                "thinness_5_9_years": 5.0,
                "income_composition_of_resources": 0.65,
                "schooling": 12.0,
                "status_numeric": 0
            }
        }
    
    @validator('immunization_avg', always=True)
    def calculate_immunization_avg(cls, v, values):
        """Calculate average immunization if not provided"""
        if v is None:
            hep_b = values.get('hepatitis_b', 0)
            polio = values.get('polio', 0)
            diphtheria = values.get('diphtheria', 0)
            v = (hep_b + polio + diphtheria) / 3
        return v
    
    @validator('child_health_score', always=True)
    def calculate_child_health_score(cls, v, values):
        """Calculate child health score if not provided"""
        if v is None:
            infant = values.get('infant_deaths', 0)
            under_five = values.get('under_five_deaths', 0)
            v = 100 - ((infant + under_five) / 2)
        return v
    
    @validator('health_spending_ratio', always=True)
    def calculate_health_spending_ratio(cls, v, values):
        """Calculate health spending ratio if not provided"""
        if v is None:
            expenditure = values.get('percentage_expenditure', 0)
            gdp = values.get('gdp', 1)
            v = expenditure / (gdp + 1)
        return v


class PredictionResponse(BaseModel):
    """Response model for predictions"""
    predicted_life_expectancy: float = Field(..., description="Predicted life expectancy in years")
    message: str = Field(..., description="Status message")
    input_summary: dict = Field(..., description="Summary of key input values")


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    model_loaded: bool
    message: str


@app.get("/", tags=["Root"])
async def root():
    """Root endpoint"""
    return {
        "message": "Life Expectancy Prediction API",
        "docs": "/docs",
        "health": "/health",
        "prediction_endpoint": "/predict"
    }


@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy" if model is not None else "unhealthy",
        "model_loaded": model is not None,
        "message": "API is running. Model loaded successfully." if model else "Model not loaded"
    }


@app.post("/predict", response_model=PredictionResponse, tags=["Prediction"])
async def predict_life_expectancy(input_data: LifeExpectancyInput):
    """
    Predict life expectancy based on health and economic indicators
    
    Args:
        input_data: LifeExpectancyInput model containing all required features
    
    Returns:
        PredictionResponse with predicted life expectancy
    
    Raises:
        HTTPException: If model is not loaded or prediction fails
    """
    
    # Check if model is loaded
    if model is None or scaler is None:
        logger.error("Model or scaler not loaded")
        raise HTTPException(
            status_code=503,
            detail="Model not loaded. Please contact administrator."
        )
    
    try:
        # Convert input to dictionary
        input_dict = input_data.dict()
        
        # Create feature array in the correct order
        # This order MUST match the order used during training
        feature_order = [
            'adult_mortality', 'infant_deaths', 'alcohol', 'percentage_expenditure',
            'hepatitis_b', 'measles', 'bmi', 'under_five_deaths', 'polio',
            'total_expenditure', 'diphtheria', 'hiv_aids', 'gdp', 'population',
            'thinness_1_19_years', 'thinness_5_9_years', 
            'income_composition_of_resources', 'schooling', 'status_numeric',
            'immunization_avg', 'child_health_score', 'health_spending_ratio'
        ]
        
        # Create feature array
        features = np.array([[input_dict[key] for key in feature_order]])
        
        # Scale features
        features_scaled = scaler.transform(features)
        
        # Make prediction
        prediction = model.predict(features_scaled)[0]
        
        # Round to 2 decimal places
        prediction = round(float(prediction), 2)
        
        # Create input summary for response
        input_summary = {
            "development_status": "Developed" if input_data.status_numeric == 1 else "Developing",
            "schooling_years": input_data.schooling,
            "gdp_per_capita": input_data.gdp,
            "adult_mortality": input_data.adult_mortality,
            "income_composition": input_data.income_composition_of_resources
        }
        
        logger.info(f"Prediction successful: {prediction} years")
        
        return {
            "predicted_life_expectancy": prediction,
            "message": "Prediction successful",
            "input_summary": input_summary
        }
    
    except KeyError as e:
        logger.error(f"Missing feature: {e}")
        raise HTTPException(
            status_code=400,
            detail=f"Missing required feature: {str(e)}"
        )
    
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Prediction failed: {str(e)}"
        )


@app.get("/feature-info", tags=["Information"])
async def get_feature_info():
    """Get information about all features and their valid ranges"""
    return {
        "features": {
            "adult_mortality": {
                "description": "Adult Mortality rate (deaths per 1000 adults aged 15-60)",
                "range": "1.0 - 1000.0",
                "type": "float"
            },
            "infant_deaths": {
                "description": "Number of infant deaths per 1000 population",
                "range": "0.0 - 2000.0",
                "type": "float"
            },
            "alcohol": {
                "description": "Alcohol consumption in liters per capita (15+ years)",
                "range": "0.0 - 20.0",
                "type": "float"
            },
            "percentage_expenditure": {
                "description": "Health expenditure as % of GDP per capita",
                "range": "0.0 - 20000.0",
                "type": "float"
            },
            "hepatitis_b": {
                "description": "Hepatitis B immunization coverage (%)",
                "range": "0.0 - 100.0",
                "type": "float"
            },
            "measles": {
                "description": "Number of reported measles cases per 1000 population",
                "range": "0.0 - 500000.0",
                "type": "float"
            },
            "bmi": {
                "description": "Average Body Mass Index of entire population",
                "range": "10.0 - 80.0",
                "type": "float"
            },
            "under_five_deaths": {
                "description": "Number of under-five deaths per 1000 population",
                "range": "0.0 - 3000.0",
                "type": "float"
            },
            "polio": {
                "description": "Polio immunization coverage (%)",
                "range": "0.0 - 100.0",
                "type": "float"
            },
            "total_expenditure": {
                "description": "Government health expenditure as % of total expenditure",
                "range": "0.0 - 20.0",
                "type": "float"
            },
            "diphtheria": {
                "description": "Diphtheria immunization coverage (%)",
                "range": "0.0 - 100.0",
                "type": "float"
            },
            "hiv_aids": {
                "description": "Deaths per 1000 live births due to HIV/AIDS (0-4 years)",
                "range": "0.0 - 50.0",
                "type": "float"
            },
            "gdp": {
                "description": "Gross Domestic Product per capita (in USD)",
                "range": "0.0 - 150000.0",
                "type": "float"
            },
            "population": {
                "description": "Population of the country",
                "range": "1000.0 - 1500000000.0",
                "type": "float"
            },
            "thinness_1_19_years": {
                "description": "Prevalence of thinness among children and adolescents (10-19 years) %",
                "range": "0.0 - 30.0",
                "type": "float"
            },
            "thinness_5_9_years": {
                "description": "Prevalence of thinness among children (5-9 years) %",
                "range": "0.0 - 30.0",
                "type": "float"
            },
            "income_composition_of_resources": {
                "description": "Human Development Index (0 to 1)",
                "range": "0.0 - 1.0",
                "type": "float"
            },
            "schooling": {
                "description": "Average number of years of schooling",
                "range": "0.0 - 25.0",
                "type": "float"
            },
            "status_numeric": {
                "description": "Development status: 0 for Developing, 1 for Developed",
                "range": "0 - 1",
                "type": "integer"
            }
        },
        "note": "Some engineered features (immunization_avg, child_health_score, health_spending_ratio) are auto-calculated if not provided"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)