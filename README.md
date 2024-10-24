
# Feature Extraction from Images - Amazon ML Challenge 2024

## Overview

This repository contains the code and solutions developed for the Amazon ML Challenge 2024. The task was to create a machine learning model capable of extracting entity values from images. This functionality is crucial for industries such as healthcare, e-commerce, and content moderation, where detailed product information directly from images can improve digital catalogs and customer experience.

The project involves building models that can accurately extract critical product information (like weight, volume, dimensions, voltage, wattage, etc.) from images. Such features are essential for managing digital stores where text-based product descriptions may not always be sufficient.

## Problem Statement

The goal of the challenge is to extract entity values directly from product images, which helps in providing detailed descriptions in digital marketplaces. The dataset consists of product images and information including category (`group_id`) and entity names. The task is to predict the `entity_value` from the images provided in the test set and submit the results in the required format.

### Dataset Description

- **index**: A unique identifier for each data sample.
- **image_link**: URL where the product image is available for download.
- **group_id**: Category code of the product.
- **entity name**: Name of the entity to be extracted (e.g., weight, dimensions).

### Output Format

The solution should generate a CSV with the following columns:
1. `index`: The unique identifier for the test data sample.
2. `prediction`: A string formatted as "x unit" (e.g., "2 gram", "12.5 centimetre").

### Constraints

- Only allowed units as specified in `constants.py` can be used.
- Predictions using invalid units will be disqualified.
- The output should match the sample output format exactly, and pass through the provided `sanity.py` script for validation.

## Solution Approach

### Approach I - OCR-Based Model

1. **Data Preprocessing**: 
   - Used techniques like binarization, noise removal, resizing, and contrast enhancement to improve image quality for OCR.
2. **Optical Character Recognition (OCR)**:
   - Experimented with different OCR tools including Easy_OCR, Paddle_OCR, and Tesseract.
   - While OCR could extract text from images, it struggled with images lacking clear text or structured formats.

### Approach II - Vision-Language Models

1. **Vision-Language Models**:
   - We experimented with Vision-supported Large Language Models, specifically LLaVA and Qwen2.
2. **Fine-Tuning**:
   - Fine-tuned the LLaVA-1.6 model and Qwen2 on a subset of the training dataset. Due to computational constraints, only a limited number of epochs were executed.
3. **Results**:
   - Qwen2 performed better, yielding the highest F1 scores and most accurate predictions.

### Post-Processing

The model outputs were processed to ensure they matched the required format:
- **Cleaning Predictions**: A Python script was used to clean and reformat predictions, ensuring the units were standardized and invalid entries were corrected or removed.
- **Validation**: The output was checked using `sanity.py` to ensure compliance with submission requirements.

## File Descriptions

### Source Files
- `src/sanity.py`: Script to check if the final output file passes all formatting checks.
- `src/utils.py`: Helper functions, including tools for downloading images from URLs.
- `src/constants.py`: Contains allowed units for each entity type.
- `sample_code.py`: Sample code to generate an output file.

### Dataset Files
- `dataset/train.csv`: Training file with labels (`entity_value`).
- `dataset/test.csv`: Test file for which predictions are required.
- `dataset/sample_test.csv`: Sample input for testing.
- `dataset/sample_test_out.csv`: Sample output in the required format.

## Evaluation

The solution will be evaluated based on the F1 score, calculated as:
- **Precision** = True Positives / (True Positives + False Positives)
- **Recall** = True Positives / (True Positives + False Negatives)
- **F1 Score** = 2 * Precision * Recall / (Precision + Recall)

## Running the Code

1. **Install Dependencies**: 
   ```bash
   pip install -r requirements.txt
   ```
2. **Download Images**:
   Use the function from `src/utils.py` to download images based on the `image_link` column in the dataset.
3. **Train the Model**:
   Follow the scripts provided in the `src` folder to train and evaluate the model.
4. **Generate Predictions**:
   Run the prediction script and save the output as `test_out.csv`.
5. **Validate Output**:
   Use `src/sanity.py` to ensure the file passes all checks:
   ```bash
   python src/sanity.py --file test_out.csv
   ```

## Contributors

- Shantanu Yadav - Department of Biotechnology, IIT Kharagpur
- Yash Lanjewar - Department of Architecture & Regional Planning, IIT Kharagpur
- Indrajit Chaudhuri - Department of Mechanical Engineering, IIT Kharagpur

## License

This project is licensed under the MIT License.
