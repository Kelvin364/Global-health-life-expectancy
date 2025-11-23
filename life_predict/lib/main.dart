import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'dart:convert';
import 'package:http/http.dart' as http;

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Life Expectancy Predictor',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(
          seedColor: Colors.teal,
          brightness: Brightness.light,
        ),
        useMaterial3: true,
        inputDecorationTheme: InputDecorationTheme(
          filled: true,
          fillColor: Colors.grey[100],
          border: OutlineInputBorder(
            borderRadius: BorderRadius.circular(12),
            borderSide: BorderSide.none,
          ),
          enabledBorder: OutlineInputBorder(
            borderRadius: BorderRadius.circular(12),
            borderSide: BorderSide(color: Colors.grey[300]!),
          ),
          focusedBorder: OutlineInputBorder(
            borderRadius: BorderRadius.circular(12),
            borderSide: const BorderSide(color: Colors.teal, width: 2),
          ),
          errorBorder: OutlineInputBorder(
            borderRadius: BorderRadius.circular(12),
            borderSide: const BorderSide(color: Colors.red),
          ),
        ),
        elevatedButtonTheme: ElevatedButtonThemeData(
          style: ElevatedButton.styleFrom(
            padding: const EdgeInsets.symmetric(horizontal: 40, vertical: 16),
            shape: RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(12),
            ),
            textStyle:
                const TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
          ),
        ),
      ),
      home: const PredictionPage(),
    );
  }
}

class PredictionPage extends StatefulWidget {
  const PredictionPage({super.key});

  @override
  State<PredictionPage> createState() => _PredictionPageState();
}

class _PredictionPageState extends State<PredictionPage> {

  final String apiUrl =
      'https://global-health-life-expectancy-1.onrender.com/predict';

  // Controllers for all REQUIRED input fields (19 fields total)
  final Map<String, TextEditingController> controllers = {
    'adult_mortality': TextEditingController(),
    'infant_deaths': TextEditingController(),
    'alcohol': TextEditingController(),
    'percentage_expenditure': TextEditingController(),
    'hepatitis_b': TextEditingController(),
    'measles': TextEditingController(),
    'bmi': TextEditingController(),
    'under_five_deaths': TextEditingController(),
    'polio': TextEditingController(),
    'total_expenditure': TextEditingController(),
    'diphtheria': TextEditingController(),
    'hiv_aids': TextEditingController(),
    'gdp': TextEditingController(),
    'population': TextEditingController(),
    'thinness_1_19_years': TextEditingController(),
    'thinness_5_9_years': TextEditingController(),
    'income_composition_of_resources': TextEditingController(),
    'schooling': TextEditingController(),
  };

  int statusNumeric = 0; // 0 for Developing, 1 for Developed
  String? predictionResult;
  String? errorMessage;
  bool isLoading = false;

  @override
  void dispose() {
    controllers.forEach((key, controller) {
      controller.dispose();
    });
    super.dispose();
  }

  // Field configurations with labels, hints, and valid ranges
  final Map<String, Map<String, dynamic>> fieldConfig = {
    'adult_mortality': {
      'label': 'Adult Mortality Rate',
      'hint': 'Deaths per 1000 adults (1-1000)',
      'min': 1.0,
      'max': 1000.0,
      'icon': Icons.person_off,
    },
    'infant_deaths': {
      'label': 'Infant Deaths',
      'hint': 'Per 1000 population (0-2000)',
      'min': 0.0,
      'max': 2000.0,
      'icon': Icons.child_care,
    },
    'alcohol': {
      'label': 'Alcohol Consumption',
      'hint': 'Liters per capita (0-20)',
      'min': 0.0,
      'max': 20.0,
      'icon': Icons.local_bar,
    },
    'percentage_expenditure': {
      'label': 'Health Expenditure',
      'hint': '% of GDP per capita (0-20000)',
      'min': 0.0,
      'max': 20000.0,
      'icon': Icons.monetization_on,
    },
    'hepatitis_b': {
      'label': 'Hepatitis B Coverage',
      'hint': 'Immunization % (0-100)',
      'min': 0.0,
      'max': 100.0,
      'icon': Icons.vaccines,
    },
    'measles': {
      'label': 'Measles Cases',
      'hint': 'Reported cases (0-500000)',
      'min': 0.0,
      'max': 500000.0,
      'icon': Icons.sick,
    },
    'bmi': {
      'label': 'Average BMI',
      'hint': 'Body Mass Index (10-80)',
      'min': 10.0,
      'max': 80.0,
      'icon': Icons.monitor_weight,
    },
    'under_five_deaths': {
      'label': 'Under-5 Deaths',
      'hint': 'Per 1000 population (0-3000)',
      'min': 0.0,
      'max': 3000.0,
      'icon': Icons.child_friendly,
    },
    'polio': {
      'label': 'Polio Coverage',
      'hint': 'Immunization % (0-100)',
      'min': 0.0,
      'max': 100.0,
      'icon': Icons.vaccines,
    },
    'total_expenditure': {
      'label': 'Total Health Expenditure',
      'hint': '% of govt spending (0-20)',
      'min': 0.0,
      'max': 20.0,
      'icon': Icons.account_balance,
    },
    'diphtheria': {
      'label': 'Diphtheria Coverage',
      'hint': 'Immunization % (0-100)',
      'min': 0.0,
      'max': 100.0,
      'icon': Icons.vaccines,
    },
    'hiv_aids': {
      'label': 'HIV/AIDS Deaths',
      'hint': 'Per 1000 births (0-50)',
      'min': 0.0,
      'max': 50.0,
      'icon': Icons.medical_services,
    },
    'gdp': {
      'label': 'GDP per Capita',
      'hint': 'In USD (0-150000)',
      'min': 0.0,
      'max': 150000.0,
      'icon': Icons.attach_money,
    },
    'population': {
      'label': 'Population',
      'hint': 'Country population (1000-1.5B)',
      'min': 1000.0,
      'max': 1500000000.0,
      'icon': Icons.people,
    },
    'thinness_1_19_years': {
      'label': 'Thinness (10-19 years)',
      'hint': 'Prevalence % (0-30)',
      'min': 0.0,
      'max': 30.0,
      'icon': Icons.fitness_center,
    },
    'thinness_5_9_years': {
      'label': 'Thinness (5-9 years)',
      'hint': 'Prevalence % (0-30)',
      'min': 0.0,
      'max': 30.0,
      'icon': Icons.fitness_center,
    },
    'income_composition_of_resources': {
      'label': 'Income Composition (HDI)',
      'hint': 'Value between 0-1',
      'min': 0.0,
      'max': 1.0,
      'icon': Icons.trending_up,
    },
    'schooling': {
      'label': 'Schooling Years',
      'hint': 'Average years (0-25)',
      'min': 0.0,
      'max': 25.0,
      'icon': Icons.school,
    },
  };

  // Validate all fields
  bool validateFields() {
    for (var entry in fieldConfig.entries) {
      String key = entry.key;
      var config = entry.value;
      String? text = controllers[key]?.text;

      if (text == null || text.isEmpty) {
        setState(() {
          errorMessage = 'Please fill in: ${config['label']}';
        });
        return false;
      }

      double? value = double.tryParse(text);
      if (value == null) {
        setState(() {
          errorMessage = '${config['label']}: Invalid number format';
        });
        return false;
      }

      if (value < config['min'] || value > config['max']) {
        setState(() {
          errorMessage =
              '${config['label']}: Must be ${config['min']}-${config['max']}';
        });
        return false;
      }
    }
    return true;
  }

  // Make prediction
  Future<void> makePrediction() async {
    setState(() {
      errorMessage = null;
      predictionResult = null;
      isLoading = true;
    });

    if (!validateFields()) {
      setState(() {
        isLoading = false;
      });
      return;
    }

    try {
      // Prepare request body
      Map<String, dynamic> requestBody = {
        'status_numeric': statusNumeric,
      };

      // Add all field values
      controllers.forEach((key, controller) {
        requestBody[key] = double.parse(controller.text);
      });

      print('Sending request to: $apiUrl');
      print('Request body: ${jsonEncode(requestBody)}');

      // Make API call
      final response = await http
          .post(
        Uri.parse(apiUrl),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode(requestBody),
      )
          .timeout(
        const Duration(seconds: 60), // Render may take time to wake up
        onTimeout: () {
          throw Exception(
              'Request timeout - Render may be waking up. Please try again in 30 seconds.');
        },
      );

      print('Response status: ${response.statusCode}');
      print('Response body: ${response.body}');

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        setState(() {
          predictionResult =
              'Predicted Life Expectancy: ${data['predicted_life_expectancy']} years';
          errorMessage = null;
        });
      } else {
        final data = jsonDecode(response.body);
        setState(() {
          errorMessage = 'Error: ${data['detail'] ?? 'Unknown error'}';
          predictionResult = null;
        });
      }
    } catch (e) {
      setState(() {
        errorMessage = 'Error: ${e.toString()}';
        predictionResult = null;
      });
      print('Exception: $e');
    } finally {
      setState(() {
        isLoading = false;
      });
    }
  }

  // Fill with example data (for testing)
  void fillExampleData() {
    controllers['adult_mortality']!.text = '150';
    controllers['infant_deaths']!.text = '20';
    controllers['alcohol']!.text = '5';
    controllers['percentage_expenditure']!.text = '500';
    controllers['hepatitis_b']!.text = '85';
    controllers['measles']!.text = '100';
    controllers['bmi']!.text = '30';
    controllers['under_five_deaths']!.text = '25';
    controllers['polio']!.text = '90';
    controllers['total_expenditure']!.text = '6.5';
    controllers['diphtheria']!.text = '88';
    controllers['hiv_aids']!.text = '1';
    controllers['gdp']!.text = '5000';
    controllers['population']!.text = '10000000';
    controllers['thinness_1_19_years']!.text = '5';
    controllers['thinness_5_9_years']!.text = '5';
    controllers['income_composition_of_resources']!.text = '0.65';
    controllers['schooling']!.text = '12';
    setState(() {
      statusNumeric = 0;
    });
  }

  // Clear all fields
  void clearFields() {
    controllers.forEach((key, controller) {
      controller.clear();
    });
    setState(() {
      statusNumeric = 0;
      predictionResult = null;
      errorMessage = null;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.grey[50],
      appBar: AppBar(
        title: const Text(
          'Life Expectancy Predictor',
          style: TextStyle(fontWeight: FontWeight.bold),
        ),
        centerTitle: true,
        backgroundColor: Colors.teal,
        foregroundColor: Colors.white,
        elevation: 0,
      ),
      body: SafeArea(
        child: Column(
          children: [
            // Header card
            Container(
              width: double.infinity,
              padding: const EdgeInsets.all(20),
              decoration: const BoxDecoration(
                color: Colors.teal,
                borderRadius: BorderRadius.only(
                  bottomLeft: Radius.circular(30),
                  bottomRight: Radius.circular(30),
                ),
              ),
              child: Column(
                children: [
                  const Icon(Icons.favorite, size: 40, color: Colors.white),
                  const SizedBox(height: 8),
                  Text(
                    'Global Health Prediction',
                    style: Theme.of(context).textTheme.titleLarge?.copyWith(
                          color: Colors.white,
                          fontWeight: FontWeight.bold,
                        ),
                  ),
                  const SizedBox(height: 4),
                  Text(
                    'Enter 19 health indicators',
                    style: TextStyle(color: Colors.white.withOpacity(0.9)),
                  ),
                ],
              ),
            ),

            // Scrollable form
            Expanded(
              child: SingleChildScrollView(
                padding: const EdgeInsets.all(20),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.stretch,
                  children: [
                    // Development Status Card
                    Card(
                      elevation: 2,
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(12),
                      ),
                      child: Padding(
                        padding: const EdgeInsets.all(16),
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            const Text(
                              'Development Status',
                              style: TextStyle(
                                fontSize: 16,
                                fontWeight: FontWeight.bold,
                              ),
                            ),
                            const SizedBox(height: 8),
                            SegmentedButton<int>(
                              segments: const [
                                ButtonSegment(
                                  value: 0,
                                  label: Text('Developing'),
                                  icon: Icon(Icons.trending_up),
                                ),
                                ButtonSegment(
                                  value: 1,
                                  label: Text('Developed'),
                                  icon: Icon(Icons.check_circle),
                                ),
                              ],
                              selected: {statusNumeric},
                              onSelectionChanged: (Set<int> newSelection) {
                                setState(() {
                                  statusNumeric = newSelection.first;
                                });
                              },
                            ),
                          ],
                        ),
                      ),
                    ),

                    const SizedBox(height: 20),

                    // Input fields (All 18 fields)
                    ...fieldConfig.entries.map((entry) {
                      return Padding(
                        padding: const EdgeInsets.only(bottom: 16),
                        child: TextField(
                          controller: controllers[entry.key],
                          keyboardType: const TextInputType.numberWithOptions(
                            decimal: true,
                          ),
                          decoration: InputDecoration(
                            labelText: entry.value['label'],
                            hintText: entry.value['hint'],
                            prefixIcon:
                                Icon(entry.value['icon'], color: Colors.teal),
                          ),
                        ),
                      );
                    }).toList(),

                    const SizedBox(height: 20),

                    // Action buttons
                    Row(
                      children: [
                        Expanded(
                          child: OutlinedButton.icon(
                            onPressed: fillExampleData,
                            icon: const Icon(Icons.lightbulb_outline),
                            label: const Text('Example'),
                            style: OutlinedButton.styleFrom(
                              padding: const EdgeInsets.symmetric(vertical: 16),
                              shape: RoundedRectangleBorder(
                                borderRadius: BorderRadius.circular(12),
                              ),
                            ),
                          ),
                        ),
                        const SizedBox(width: 10),
                        Expanded(
                          child: OutlinedButton.icon(
                            onPressed: clearFields,
                            icon: const Icon(Icons.clear_all),
                            label: const Text('Clear'),
                            style: OutlinedButton.styleFrom(
                              padding: const EdgeInsets.symmetric(vertical: 16),
                              shape: RoundedRectangleBorder(
                                borderRadius: BorderRadius.circular(12),
                              ),
                            ),
                          ),
                        ),
                      ],
                    ),

                    const SizedBox(height: 16),

                    // Predict button
                    ElevatedButton.icon(
                      onPressed: isLoading ? null : makePrediction,
                      icon: isLoading
                          ? const SizedBox(
                              width: 20,
                              height: 20,
                              child: CircularProgressIndicator(
                                strokeWidth: 2,
                                color: Colors.white,
                              ),
                            )
                          : const Icon(Icons.analytics),
                      label: Text(isLoading
                          ? 'Predicting...'
                          : 'Predict Life Expectancy'),
                      style: ElevatedButton.styleFrom(
                        backgroundColor: Colors.teal,
                        foregroundColor: Colors.white,
                      ),
                    ),

                    const SizedBox(height: 20),

                    // Result display
                    if (predictionResult != null)
                      Card(
                        elevation: 4,
                        color: Colors.green[50],
                        shape: RoundedRectangleBorder(
                          borderRadius: BorderRadius.circular(12),
                          side: BorderSide(color: Colors.green[300]!, width: 2),
                        ),
                        child: Padding(
                          padding: const EdgeInsets.all(20),
                          child: Column(
                            children: [
                              const Icon(
                                Icons.check_circle,
                                color: Colors.green,
                                size: 48,
                              ),
                              const SizedBox(height: 12),
                              Text(
                                predictionResult!,
                                style: const TextStyle(
                                  fontSize: 20,
                                  fontWeight: FontWeight.bold,
                                  color: Colors.green,
                                ),
                                textAlign: TextAlign.center,
                              ),
                            ],
                          ),
                        ),
                      ),

                    // Error display
                    if (errorMessage != null)
                      Card(
                        elevation: 4,
                        color: Colors.red[50],
                        shape: RoundedRectangleBorder(
                          borderRadius: BorderRadius.circular(12),
                          side: BorderSide(color: Colors.red[300]!, width: 2),
                        ),
                        child: Padding(
                          padding: const EdgeInsets.all(20),
                          child: Column(
                            children: [
                              const Icon(
                                Icons.error,
                                color: Colors.red,
                                size: 48,
                              ),
                              const SizedBox(height: 12),
                              Text(
                                errorMessage!,
                                style: const TextStyle(
                                  fontSize: 16,
                                  fontWeight: FontWeight.bold,
                                  color: Colors.red,
                                ),
                                textAlign: TextAlign.center,
                              ),
                            ],
                          ),
                        ),
                      ),

                    const SizedBox(height: 20),
                  ],
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
