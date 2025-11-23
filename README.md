#  Life Expectancy Prediction System
## AI-Powered Global Health Analytics
Demo video :  **[LOOM VIDEO DEMO](#)** *(https://www.loom.com/share/967f68c7eef54d1a8bc030468eeab39d)*
[![API Status](https://img.shields.io/badge/API-Live-success)](https://global-health-life-expectancy-1.onrender.com/docs)
[![Model Accuracy](https://img.shields.io/badge/R²-0.96-blue)](https://global-health-life-expectancy-1.onrender.com/docs)
[![Platform](https://img.shields.io/badge/Platform-Flutter-02569B?logo=flutter)](https://flutter.dev)
[![Deployed on](https://img.shields.io/badge/Deployed%20on-Render-46E3B7?logo=render)](https://render.com)



## Mission & Problem Statement

This system addresses the challenge of predicting life expectancy across countries using health, economic, and social indicators. By leveraging machine learning on WHO data (2,938 observations from 193 countries), this predict life expectancy with 96% accuracy (R² = 0.96), enabling health policymakers to identify key intervention points and the more imoprtantly which **feature attributes helps them increase the life of their population**. The Random Forest model analyzes 19 indicators including mortality rates, immunization coverage, GDP, and education to provide actionable insights for resource allocation and policy development.



##  Live API Endpoint

### **Interactive API Documentation (Swagger UI)**

 **[https://global-health-life-expectancy-1.onrender.com/docs](https://global-health-life-expectancy-1.onrender.com/docs)**

### **API Endpoints:**
| Root | GET | API information | [/](https://global-health-life-expectancy-1.onrender.com/) |
| Health Check | GET | Verify API & model status | [/health](https://global-health-life-expectancy-1.onrender.com/health) |
| Feature Info | GET | List all input features & ranges | [/feature-info](https://global-health-life-expectancy-1.onrender.com/feature-info) |

| **Predict** | **POST** | **Get life expectancy prediction** | [/predict](https://global-health-life-expectancy-1.onrender.com/predict) 

### **Quick API Test:**

**Health Check:**
```bash
curl https://global-health-life-expectancy-1.onrender.com/health
```


##  Video Demonstration

### ** YouTube Demo Video (10 Minutes)**

 **[LOOM VIDEO DEMO](#)** *(https://www.loom.com/share/967f68c7eef54d1a8bc030468eeab39d)*



## Mobile App - Setup & Usage Instructions

### **Prerequisites**

Before running the mobile app, ensure you have:

- **Flutter SDK** installed ([Installation Guide](https://docs.flutter.dev/get-started/install))
- **Android Studio** or **VS Code** with Flutter extension
- **Android device/emulator** or **iOS device/simulator** (Mac only)
- **Internet connection** (for API calls)

### **Installation Steps**

#### **Step 1: Verify Flutter Installation**

```bash
# Check Flutter installation
flutter doctor

# Expected output should show:
# ✓ Flutter SDK
# ✓ Android toolchain / Xcode (for iOS)
# ✓ Connected device
```

#### **Step 2: Create Flutter Project**

```bash
# Create new Flutter project
flutter create life_expectancy_predictor

# Navigate to project directory
cd life_expectancy_predictor
```

#### **Step 3: Replace Project Files**

Replace the following files with the provided ones:

**`lib/main.dart`** - Complete Flutter application code
```dart
// File location: flutter_app/lib/main.dart
// Copy contents from provided file
```

**`pubspec.yaml`** - Project dependencies
```yaml
# File location: flutter_app/pubspec.yaml
# Copy contents from provided file
```

#### **Step 4: Install Dependencies**

```bash
# Get all required packages
flutter pub get

# Verify no errors
# Expected: "Running 'flutter pub get' in life_expectancy_predictor... [time]"
```

#### **Step 5: Configure API Endpoint**

Open `lib/main.dart` and verify the API URL (line ~54):

```dart
final String apiUrl = 'https://global-health-life-expectancy-1.onrender.com/predict';
```

*** This is already configured!** No changes needed.

#### **Step 6: Run the Application**

**For Android:**
```bash
# List available devices
flutter devices

# Run on connected device
flutter run

# Or run on specific device
flutter run -d <device-id>
```

**For iOS (Mac only):**
```bash
# Open iOS simulator
open -a Simulator

# Run on simulator
flutter run
```


### **Using the Mobile App**

#### **Main Features:**

1. **19 Input Fields** - All health and economic indicators
2. **Development Status Selector** - Choose Developing or Developed
3. **Example Button** - Fills sample data for quick testing
4. **Clear Button** - Resets all fields
5. **Predict Button** - Makes prediction via API
6. **Result Display** - Shows predicted life expectancy or error messages

#### **Making a Prediction:**

**Method 1: Use Example Data (Recommended for Testing)**

1. Launch the app
2. Tap the **"Example"** button
3. All 19 fields fill with sample data
4. Tap the **"Predict"** button
5. Wait 30-60 seconds for first prediction (Render wake-up)
6. View result: "Predicted Life Expectancy: 68.5 years"

**Method 2: Manual Data Entry**

1. Select **Development Status** (Developing/Developed)
2. Fill in all 18 numeric fields:
   - Adult Mortality (1-1000)
   - Infant Deaths (0-2000)
   - Alcohol Consumption (0-20)
   - Health Expenditure (0-20000)
   - Hepatitis B Coverage (0-100)
   - Measles Cases (0-500000)
   - Average BMI (10-80)
   - Under-5 Deaths (0-3000)
   - Polio Coverage (0-100)
   - Total Health Expenditure (0-20)
   - Diphtheria Coverage (0-100)
   - HIV/AIDS Deaths (0-50)
   - GDP per Capita (0-150000)
   - Population (1000-1.5B)
   - Thinness 10-19 years (0-30)
   - Thinness 5-9 years (0-30)
   - Income Composition (0-1)
   - Schooling Years (0-25)
3. Tap **"Predict"**
4. View result



### **Input Validation**

The app validates all inputs before sending to API:

**Type Checking:** All fields must be valid numbers
**Range Validation:** Values must be within specified ranges
**Required Fields:** All 19 fields must be filled
**Clear Error Messages:** Specific feedback for validation failures

**Example Errors:**
- "Please fill in: Adult Mortality Rate"
- "Average BMI: Must be 10-80"
- "Invalid number format"




## Model Performance

### **Comparison of Models**

| Model | R² Score | MAE (years) | RMSE (years) | Selected |
|-------|----------|-------------|--------------|----------|
| Linear Regression | 0.82 | 2.9 | 3.8 | ❌ |
| Decision Tree | 0.93 | 1.8 | 2.1 | ❌ |
| **Random Forest** | **0.96** | **1.3** | **1.6** | ✅ |

### **Why Random Forest?**

1. **Superior Performance:** 96% accuracy vs 93% (Decision Tree) and 82% (Linear Regression)
2. **Handles Non-linearity:** Captures complex relationships in health data
3. **Robust to Overfitting:** Ensemble of 100 trees reduces variance
4. **Feature Importance:** Provides interpretable insights
5. **Production Ready:** Fast inference (<100ms) and handles missing values

### **Key Features by Importance:**

1. **Income Composition (HDI):** 28% - Strongest predictor
2. **Schooling Years:** 15% - Education's impact on health
3. **Adult Mortality:** 12% - Direct health indicator
4. **HIV/AIDS Deaths:** 10% - Disease burden
5. **Other indicators:** 35% - Combined effect



## Required Input Features (19 Total)

### **Health Indicators (11 fields):**

| Field | Range | Unit | Description |
|-------|-------|------|-------------|
| adult_mortality | 1-1000 | per 1000 | Deaths of adults (15-60 years) |
| infant_deaths | 0-2000 | per 1000 | Infant deaths per 1000 population |
| under_five_deaths | 0-3000 | per 1000 | Deaths of children under 5 |
| hepatitis_b | 0-100 | % | Hepatitis B immunization coverage |
| measles | 0-500000 | cases | Reported measles cases |
| polio | 0-100 | % | Polio immunization coverage |
| diphtheria | 0-100 | % | Diphtheria immunization coverage |
| hiv_aids | 0-50 | per 1000 | HIV/AIDS deaths (0-4 years) |
| bmi | 10-80 | kg/m² | Average Body Mass Index |
| thinness_1_19_years | 0-30 | % | Thinness prevalence (10-19 years) |
| thinness_5_9_years | 0-30 | % | Thinness prevalence (5-9 years) |

### **Economic Indicators (3 fields):**

| Field | Range | Unit | Description |
|-------|-------|------|-------------|
| percentage_expenditure | 0-20000 | % | Health expenditure as % of GDP per capita |
| total_expenditure | 0-20 | % | Government health expenditure |
| gdp | 0-150000 | USD | Gross Domestic Product per capita |

### **Social Indicators (4 fields):**

| Field | Range | Unit | Description |
|-------|-------|------|-------------|
| income_composition_of_resources | 0-1 | index | Human Development Index (HDI) |
| schooling | 0-25 | years | Average years of schooling |
| population | 1000-1.5B | count | Country population |
| alcohol | 0-20 | liters | Alcohol consumption per capita |

### **Development Status (1 field):**

| Field | Range | Description |
|-------|-------|-------------|
| status_numeric | 0-1 | 0 = Developing, 1 = Developed |






## Technologies Used

### **Backend:**
- **FastAPI** 0.104.1 - Modern Python web framework
- **Pydantic** 2.5.0 - Data validation
- **Uvicorn** 0.24.0 - ASGI server
- **Scikit-learn** 1.3.2 - Machine learning
- **Joblib** 1.3.2 - Model serialization
- **NumPy** 1.24.3 - Numerical computing

### **Frontend:**
- **Flutter** 3.x - Cross-platform framework
- **Dart** - Programming language
- **HTTP** 1.1.0 - API client
- **Material Design 3** - UI components

### **Deployment:**
- **Render** - Cloud platform (backend)
- **GitHub** - Version control
- **Docker** - Containerization (Render uses internally)

### **Data & ML:**
- **WHO Dataset** - 2,938 observations, 193 countries
- **Random Forest** - 100 trees, max_depth=20
- **StandardScaler** - Feature normalization
- **Train-Test Split** - 80-20 ratio


##  Dataset Information

### **Source:**
- **Organization:** World Health Organization (WHO)
- **Time Period:** 2000-2015
- **Countries:** 193 countries
- **Observations:** 2,938 records
- **Features:** 22 original features → 19 final features (after preprocessing)

### **Target Variable:**
- **Life Expectancy:** Range from 36 to 89 years

### **Preprocessing:**
-  Missing value imputation (median strategy)
-  Feature scaling (StandardScaler)
-  Feature engineering (3 new features)
-  Multicollinearity handling
-  Outlier detection and treatment



##  API Security & Features

### **Security:**
-  CORS enabled (configurable origins)
-  Input validation (Pydantic)
-  Type enforcement (strict types)
-  Range constraints (all inputs)
-  Error handling (comprehensive)

### **Features:**
-  Automatic API documentation (Swagger/ReDoc)
-  Health check endpoint
-  Feature information endpoint
-  Detailed error messages
-  Request/response logging
-  Model version tracking



##  Performance Benchmarks

### **API Response Times:**
- **First Request:** 30-60 seconds (Render wake-up)
- **Subsequent Requests:** <2 seconds
- **Model Inference:** <100ms
- **Validation:** <10ms

### **Model Metrics:**
- **Accuracy (R²):** 0.96 (96%)
- **Average Error (MAE):** 1.3 years
- **RMSE:** 1.6 years
- **Cross-Validation R²:** 0.95 ± 0.02

### **Scalability:**
- **Concurrent Requests:** Render handles load balancing
- **Model Size:** ~50MB (optimized)
- **Memory Usage:** ~200MB (runtime)



##  Documentation

### **API Documentation:**
- **Swagger UI:** [https://global-health-life-expectancy-1.onrender.com/docs](https://global-health-life-expectancy-1.onrender.com/docs)
- **ReDoc:** [https://global-health-life-expectancy-1.onrender.com/redoc](https://global-health-life-expectancy-1.onrender.com/redoc)

### **Additional Guides:**
- [Backend Deployment Guide](docs/DEPLOYMENT_GUIDE.md)
- [Flutter Integration Guide](docs/FLUTTER_INTEGRATION_GUIDE.md)
- [Video Demo Script](docs/VIDEO_DEMO_SCRIPT.md)
- [Model Comparison Details](docs/MODEL_COMPARISON_TALKING_POINTS.md)



##  Contributing

This is an academic project. For questions or suggestions:

1. **Issue Tracker:** Report bugs or request features
2. **Pull Requests:** Contributions welcome
3. **Documentation:** Help improve guides



##License

This project is for educational purposes. Dataset from WHO is publicly available.



## Author

**Kelvin Rwihimba**


## Acknowledgments

- **World Health Organization (WHO)** - Dataset provider
- **Scikit-learn** - Machine learning framework
- **FastAPI** - Modern web framework
- **Flutter** - Cross-platform mobile framework
- **Render** - Cloud deployment platform




