#!/bin/bash

# Script to convert DICOM files to NIfTI format using dcm2niix and run Python processing
# Usage: ./dcm2vr.sh <input_directory> <output_directory> <segmentation_output_directory> <mode>
# EX: bash dcm2vr.sh CT/ Outputs/CT Outputs/CT/Seg total

# Check if correct number of arguments provided
if [ $# -ne 4 ]; then
    echo "Error: Incorrect number of arguments"
    echo "Usage: $0 <input_directory> <output_directory> <segmentation_output_directory> <segmentation task>"
    exit 1
fi

# Assign arguments to variables
INPUT_DIR="$1"
OUTPUT_DIR="$2"
SEG_OUTPUT_DIR="$3"
TASK="$4"

# Check if input directory exists
if [ ! -d "$INPUT_DIR" ]; then
    echo "Error: Input directory '$INPUT_DIR' does not exist"
    exit 1
fi

# Check if input directory is readable
if [ ! -r "$INPUT_DIR" ]; then
    echo "Error: Input directory '$INPUT_DIR' is not readable"
    exit 1
fi

# Check if dcm2niix command is available
if ! command -v dcm2niix &> /dev/null; then
    echo "Error: dcm2niix command not found. Please install dcm2niix first."
    exit 1
fi

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "Error: python3 command not found. Please install Python 3 first."
    exit 1
fi

# Check if main.py exists
if [ ! -f "main.py" ]; then
    echo "Error: main.py not found in current directory"
    exit 1
fi

# Create output directory if it doesn't exist
if [ ! -d "$OUTPUT_DIR" ]; then
    echo "Output directory '$OUTPUT_DIR' does not exist. Creating it..."
    mkdir -p "$OUTPUT_DIR"
    if [ $? -ne 0 ]; then
        echo "Error: Failed to create output directory '$OUTPUT_DIR'"
        exit 1
    fi
    echo "Output directory created successfully"
else
    echo "Output directory '$OUTPUT_DIR' already exists"
fi

# Check if output directory is writable
if [ ! -w "$OUTPUT_DIR" ]; then
    echo "Error: Output directory '$OUTPUT_DIR' is not writable"
    exit 1
fi

# Run dcm2niix conversion
echo "Starting conversion from '$INPUT_DIR' to '$OUTPUT_DIR'..."
dcm2niix -o "$OUTPUT_DIR" "$INPUT_DIR"

# Check if conversion was successful
if [ $? -ne 0 ]; then
    echo "Error: Conversion failed"
    exit 1
fi

echo "Conversion completed successfully!"
echo ""

# Run Python script on dcm2niix outputs
echo "Running Python processing on NIfTI files..."
echo "Input directory: $OUTPUT_DIR"
echo "Output directory: $SEG_OUTPUT_DIR"
python3 main.py "$OUTPUT_DIR" "$SEG_OUTPUT_DIR" "$TASK"

# Check if Python script was successful
if [ $? -eq 0 ]; then
    echo "Python processing completed successfully!"
    exit 0
else
    echo "Error: Python processing failed"
    exit 1
fi