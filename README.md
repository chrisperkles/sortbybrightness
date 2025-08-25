# Sort by Brightness

A Python script that analyzes photos by brightness levels and copies only those meeting specified criteria to organized output folders. Perfect for sorting large collections of camera trap images, security camera footage, timelapse sequences, or any photo archive where you want to separate daylight shots from nighttime images.

## Features

- **Recursive folder scanning** - Processes all images in subdirectories
- **Multiple image formats** - Supports JPG, JPEG, PNG, WebP, TIF, TIFF
- **Brightness-based filtering** - Uses histogram analysis for accurate brightness calculation
- **Flexible thresholds** - Customizable brightness cutoff points
- **Batch processing** - Handles thousands of images efficiently  
- **Error resilience** - Continues processing even with corrupted files
- **Preserve folder structure** - Maintains relative paths in destination

## Installation

1. Clone this repository:
```bash
git clone https://github.com/chrisperkles/sortbybrightness.git
cd sortbybrightness
```

2. Install required dependencies:
```bash
pip install pillow pillow-heif
```

## Usage

```bash
python3 select_by_brightness.py SOURCE_DIR DESTINATION_DIR --threshold BRIGHTNESS_VALUE [--invert]
```

### Parameters

- `SOURCE_DIR` - Path to folder containing images to analyze
- `DESTINATION_DIR` - Path where selected images will be copied
- `--threshold` - Brightness threshold value (0-255)
- `--invert` - Optional: Invert selection (select darker images instead)

### Understanding Brightness Thresholds

The brightness calculation uses histogram analysis where **higher threshold values select brighter images**:

- **140+**: Very bright daylight shots only
- **110-120**: Good daylight images  
- **90-100**: Overcast/indoor lighting included
- **70-80**: Dim lighting/dusk included
- **60-**: Includes dark/nighttime images

### Examples

**Select bright daylight photos only:**
```bash
python3 select_by_brightness.py /path/to/camera_trap /path/to/daylight_only --threshold 110
```

**Select nighttime/dark images:**
```bash
python3 select_by_brightness.py /path/to/photos /path/to/night_images --threshold 110 --invert
```

**Process with very strict bright daylight filter:**
```bash
python3 select_by_brightness.py /path/to/images /path/to/bright_only --threshold 140
```

**Extract daylight frames from timelapse sequence:**
```bash
python3 select_by_brightness.py /path/to/timelapse_frames /path/to/daylight_frames --threshold 110
```

## Real-World Usage

This script was developed for processing large camera trap image collections:

- **Part 1**: 6,384 files → 1,158 daylight images (threshold 110)
- **Part 2**: 9,312 files → 2,399 daylight images (threshold 110)  
- **Part 3**: 8,809 files → 2,420 daylight images (threshold 110)

The script efficiently handles corrupted files, continuing processing while logging warnings for any problematic images.

## How It Works

1. **Image Loading**: Opens each image and applies EXIF rotation correction
2. **Grayscale Conversion**: Converts to grayscale for brightness analysis
3. **Histogram Analysis**: Calculates weighted average brightness from pixel histogram
4. **Threshold Comparison**: Compares calculated brightness against threshold
5. **Selective Copying**: Copies matching images while preserving folder structure

## Supported Formats

- JPEG (.jpg, .jpeg)
- PNG (.png)
- WebP (.webp)
- TIFF (.tif, .tiff)

## Error Handling

The script gracefully handles:
- Corrupted image files
- Truncated downloads
- Unsupported formats
- Missing directories (creates them automatically)
- Permission issues

## Performance

- Processes thousands of images per minute
- Memory efficient (processes one image at a time)
- Handles large image collections without memory issues
- Progress reporting with file counts

## Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.

## License

MIT License - see LICENSE file for details.

## Author

Created for efficiently sorting camera trap and security camera image archives.