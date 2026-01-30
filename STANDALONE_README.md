# Metal Inventory Standalone

This is a standalone version of the Metal Inventory application.

## How to Run
Simply open **index.html** in any modern web browser (Edge, Chrome, Safari).

## Features
- **Voice Entry**: Uses built-in browser speech recognition (works best in Chrome/Edge/Safari).
- **Offline Capable**: Data is saved to your browser's LocalStorage.
- **Excel Database**: Includes embedded parts database.
- **Excel Export**: Exports counted inventory to an Excel file using `SheetJS` (requires internet connection for first load of library, or cache).

## Files
- `index.html`: The main user interface.
- `script.js`: Application logic and database.

## Troubleshooting
- If "Voice-to-text not supported" appears, try Chrome or Edge.
- If exports fail, ensure you have an internet connection to load the Excel library.
